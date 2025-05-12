import streamlit as st
import json
import pandas as pd
import os
import altair as alt  # Import Altair

def get_all_contest_names(folder_path):
    """
    Extracts all unique contest names from JSON files in a folder.

    Args:
        folder_path (str): The path to the folder containing JSON files.

    Returns:
        list: A list of unique contest names.
    """

    all_contest_names = set()
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'national' in data:
                        for contest in data['national']:
                            all_contest_names.add(contest['contestName'])
                    if 'local' in data:
                        for contest in data['local']:
                            all_contest_names.add(contest['contestName'])
    except FileNotFoundError:
        st.error(f"Error: Folder '{folder_path}' not found.")
        return []  # Return an empty list if the folder is not found
    except json.JSONDecodeError:
        st.error(f"Error: Invalid JSON in files within '{folder_path}'.")
        return []
    except KeyError as e:
        st.error(f"Error: Key '{e}' not found in JSON data.")
        return []
    return list(all_contest_names)


def load_data_from_folder(folder_path):
    """Loads data from all JSON files in a folder into a list of dictionaries."""
    data = []
    city = None
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as f:
                    entry = json.load(f)
                    data.append(entry)
                    if city is None and 'information' in entry and 'location' in entry['information']:
                        location_parts = entry['information']['location'].split(',')
                        if len(location_parts) >= 3:
                            city = location_parts[2].strip()
    except FileNotFoundError:
        st.error(f"Error: Folder '{folder_path}' not found.")
        return None, None
    except json.JSONDecodeError:
        st.error(f"Error: Invalid JSON in files within '{folder_path}'.")
        return None, None
    return data, city


def calculate_vote_counts(data, contest_names):
    """Calculates total vote counts for each candidate across all files for given contests."""

    all_candidates = {contest_name: {} for contest_name in contest_names}
    if data:
        for entry in data:
            if 'national' in entry or 'local' in entry:
                for area_type in ['national', 'local']:
                    if area_type in entry:
                        for contest in entry[area_type]:
                            if contest['contestName'] in contest_names:
                                for candidate in contest['candidates']['candidates']:
                                    if candidate['name'] not in all_candidates[contest['contestName']]:
                                        all_candidates[contest['contestName']][candidate['name']] = 0
                                    all_candidates[contest['contestName']][candidate['name']] += candidate['votes']

        result_dataframes = {}
        for contest_name, candidates in all_candidates.items():
            candidate_list = [{"Candidate": k, "Votes": v} for k, v in candidates.items()]
            result_dataframes[contest_name] = pd.DataFrame(candidate_list)
        return result_dataframes
    else:
        return {contest_name: pd.DataFrame() for contest_name in contest_names}


def create_summary_page(vote_counts_dfs, city):
    """Creates a summary page showing total vote counts for specified contests."""

    st.title(f"Election Results Summary - City of {city}" if city else "Election Results Summary")

    # Adapt contest names display based on available data
    contest_names_display = {
        contest_name: contest_name for contest_name in vote_counts_dfs.keys()
    }  # Default: use original name

    # Customize display names (optional -  you can expand this as needed)
    common_names = {
        "PROVINCIAL GOVERNOR": "Governor",
        "PROVINCIAL VICE-GOVERNOR": "Vice Governor",
        "MAYOR": "Mayor",
        "VICE-MAYOR": "Vice Mayor",
        "MEMBER, HOUSE OF REPRESENTATIVES": "Congressman",
        "PARTY LIST": "Party List",
        "SENATOR": "Senator"
    }

    for original_name, display_name in common_names.items():
        for contest_name in contest_names_display:
            if original_name in contest_name:
                contest_names_display[contest_name] = display_name
                break # Avoid multiple replacements


    for contest_name, df in vote_counts_dfs.items():
        if not df.empty:
            st.subheader(contest_names_display.get(contest_name, contest_name))
            st.dataframe(df)

            # Create a bar chart for visualization
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Candidate', sort='-y'),
                y='Votes',
                tooltip=['Candidate', 'Votes']
            ).properties(
                title=contest_names_display.get(contest_name, contest_name)
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning(f"No data available to display vote counts for {contest_names_display.get(contest_name, contest_name)}.")


def main():
    st.set_page_config(page_title="Election Results Dashboard", layout="wide")
    st.sidebar.title("Election Results")

    folder_path = st.sidebar.text_input("Enter Folder Path Containing JSON Files")

    if folder_path:
        data, city = load_data_from_folder(folder_path)
        if data is not None:
            contest_names = get_all_contest_names(folder_path) # Get contest names dynamically
            if contest_names: # Only proceed if contest_names is not empty
                vote_counts_dfs = calculate_vote_counts(data, contest_names)
                create_summary_page(vote_counts_dfs, city)
            else:
                st.error("Could not determine contest names. Please check the JSON files.")

    else:
        st.sidebar.info("Please enter the path to the folder containing JSON files.")
        st.info("Enter a folder path in the sidebar to analyze election results from JSON files.")


if __name__ == "__main__":
    main()
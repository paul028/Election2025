import streamlit as st
import json
import pandas as pd
import os

def load_data_from_folder(folder_path):
    """Loads data from all JSON files in a folder into a list of dictionaries."""
    data = []
    city = None  # Initialize city to None
    try:
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as f:
                    entry = json.load(f)
                    data.append(entry)
                    # Extract city from the first file (assuming it's consistent)
                    if city is None and 'information' in entry and 'location' in entry['information']:
                        location_parts = entry['information']['location'].split(',')
                        if len(location_parts) >= 3:  # Ensure there are enough parts
                            city = location_parts[2].strip()  # Extract the city
    except FileNotFoundError:
        st.error(f"Error: Folder '{folder_path}' not found.")
        return None, None
    return data, city


def calculate_vote_counts(data, contest_names):
    """Calculates total vote counts for each candidate across all files for given contests."""

    all_candidates = {contest_name: {} for contest_name in contest_names}
    if data:  # Only proceed if data is not empty
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

        # Convert to list of dicts for easier DataFrame creation
        result_dataframes = {}
        for contest_name, candidates in all_candidates.items():
            candidate_list = [{"Candidate": k, "Votes": v} for k, v in candidates.items()]
            result_dataframes[contest_name] = pd.DataFrame(candidate_list)
        return result_dataframes
    else:
        return {contest_name: pd.DataFrame() for contest_name in contest_names}  # Return empty DataFrames


def create_summary_page(vote_counts_dfs, city):
    """Creates a summary page showing total vote counts for specified contests."""

    st.title(f"Election Results Summary - City of {city}" if city else "Election Results Summary")

    contest_names_display = {
        "PROVINCIAL GOVERNOR of BULACAN": "Governor",
        "PROVINCIAL VICE-GOVERNOR of BULACAN": "Vice Governor",
        "MAYOR of BULACAN - CITY OF SAN JOSE DEL MONTE": "Mayor",
        "VICE-MAYOR of BULACAN - CITY OF SAN JOSE DEL MONTE": "Vice Mayor",
        "MEMBER, HOUSE OF REPRESENTATIVES of BULACAN - CITY OF SAN JOSE DEL MONTE - LONE LEGDIST": "Congressman",
        "PARTY LIST of PHILIPPINES": "Party List",
        "SENATOR of PHILIPPINES": "Senator"  # Added Senator
    }

    for contest_name, df in vote_counts_dfs.items():
        if not df.empty:
            st.subheader(contest_names_display.get(contest_name, contest_name))  # Use display name or original
            st.dataframe(df)

            # Create a bar chart for visualization
            import altair as alt
            chart = alt.Chart(df).mark_bar().encode(
                x=alt.X('Candidate', sort='-y'),  # Sort by votes descending
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
        if data is not None:  # Check if data loading was successful
            contest_names = [
                "PROVINCIAL GOVERNOR of BULACAN",
                "PROVINCIAL VICE-GOVERNOR of BULACAN",
                "MAYOR of BULACAN - CITY OF SAN JOSE DEL MONTE",
                "VICE-MAYOR of BULACAN - CITY OF SAN JOSE DEL MONTE",
                "MEMBER, HOUSE OF REPRESENTATIVES of BULACAN - CITY OF SAN JOSE DEL MONTE - LONE LEGDIST",
                "PARTY LIST of PHILIPPINES",
                "SENATOR of PHILIPPINES" # Added Senator
            ]
            vote_counts_dfs = calculate_vote_counts(data, contest_names)
            create_summary_page(vote_counts_dfs, city)

    else:
        st.sidebar.info("Please enter the path to the folder containing JSON files.")
        st.info("Enter a folder path in the sidebar to analyze election results from JSON files.")


if __name__ == "__main__":
    main()
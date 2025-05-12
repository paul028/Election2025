# Election Data Tools

This repository contains two Python scripts for downloading and visualizing election results data in JSON format from the COMELEC (Commission on Elections) website.

## `election_download.py`

This script is used to download JSON files containing election results for a specific location and precinct range.

### Prerequisites

- Python 3.x
- `requests` library

You can install the `requests` library using pip:

```bash
pip install requests

Usage
Modify Configuration (within the script):
Open election_download.py and adjust the following variables in the if __name__ == "__main__": block:

base_url: Set this to the base URL of the JSON files you want to download. In the provided example, it's set to "https://2025electionresults.comelec.gov.ph/data/er/142/" for the City of San Jose Del Monte, Bulacan.
start_number: Set the starting number for the filename iteration. The example uses 14200000.
end_number: Set the ending number for the filename iteration. The example uses 14299999.
save_directory: Optionally, change "comelec_data" to the name of the folder where you want to save the downloaded JSON files. If the directory doesn't exist, the script will attempt to create it.
Run the script:
Open your terminal or command prompt, navigate to the directory where you saved election_download.py, and run:

Bash

python election_download.py
Functionality
Iterates through a range of numbers specified by start_number and end_number.
Constructs a URL for each number by appending an 8-digit zero-padded number with the .json extension to the base_url.
Sends an HTTP GET request to each URL.
If the request is successful (status code 200), it saves the JSON content to a file in the specified save_directory. The filename will correspond to the number in the URL (e.g., 00000001.json).
If a "File not found" error (status code 404) occurs, it prints a corresponding message.
For other HTTP errors, it prints the error status code and the URL.
Includes a 0.1-second delay between requests to be respectful to the server.
Prints informative messages about the download process.
result_dashboard.py
This script is a Streamlit application that allows you to visualize the election results from the JSON files downloaded using election_download.py.

Prerequisites
Python 3.x
streamlit
pandas
altair
You can install these libraries using pip:

Bash

pip install streamlit pandas altair
Usage
Ensure JSON files are downloaded: Make sure you have run election_download.py and have JSON files in the specified save_directory (or a directory of your choice).

Run the Streamlit application:
Open your terminal or command prompt, navigate to the directory where you saved result_dashboard.py, and run:

Bash

streamlit run result_dashboard.py
This will open a new tab in your web browser displaying the Election Results Dashboard.

Enter Folder Path: In the sidebar of the Streamlit application, you will see a text input field labeled "Enter Folder Path Containing JSON Files". Enter the path to the directory where your downloaded JSON files are located (e.g., comelec_data).

View Results: Once you enter the folder path, the application will:

Load the data from all .json files in the specified folder.
Extract the city name from the location information in the JSON files (assuming the format is consistent).
Calculate the total vote counts for specified election contests (Governor, Vice Governor, Mayor, Vice Mayor, Congressman, Party List, and Senator).
Display a summary page with tables and bar charts showing the vote counts for each candidate in each contest.
Functionality
load_data_from_folder(folder_path): Reads all JSON files from the given folder and loads the data into a list of dictionaries. It also attempts to extract the city name from the "location" field in the JSON data.
calculate_vote_counts(data, contest_names): Takes the loaded data and a list of contest names as input. It iterates through the data to calculate the total number of votes for each candidate in the specified contests. It returns a dictionary where keys are contest names and values are Pandas DataFrames with "Candidate" and "Votes" columns.
create_summary_page(vote_counts_dfs, city): Takes a dictionary of vote count DataFrames and the city name as input. It creates a Streamlit page displaying the results for each contest in a tabular format and as a bar chart for better visualization.
main(): Sets up the Streamlit application interface, including the sidebar for folder path input and the main area to display the results.
Notes
The result_dashboard.py script assumes a specific structure in the JSON files, particularly for extracting the city name and the vote counts for candidates within the "national" and "local" sections of each entry.
The list of contest_names in result_dashboard.py can be modified to analyze different election contests present in the JSON data.
The script uses Altair for creating interactive bar charts for the vote counts.
Error handling is included to manage cases where the specified folder is not found or if there are issues loading the JSON data.

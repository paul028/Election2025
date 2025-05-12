import requests
import os
import time

def download_json_files(start_number, end_number, base_url, directory="."):
    """
    Downloads JSON files from a given base URL, iterating through a range of numbers.

    Args:
        start_number (int): The starting number for the filename.
        end_number (int): The ending number for the filename.
        base_url (str): The base URL of the JSON files (without the filename).
        directory (str, optional): The directory to save the downloaded files. Defaults to the current directory.

    Returns:
        None: The function downloads and saves files; it doesn't return a value.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            return  # Stop if directory creation fails

    # Loop through the numbers
    for i in range(start_number, end_number + 1):
        # Format the filename
        filename = f"{i:08d}.json"  # Ensure 8 digits with leading zeros
        url = f"{base_url}{filename}"

        try:
            # Send a GET request to the URL
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Construct the full file path
                filepath = os.path.join(directory, filename)

                # Write the content to a file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"Downloaded: {url} to {filepath}")
            elif response.status_code == 404:
                print(f"File not found: {url}") # Print 404 error
            else:
                print(f"Error {response.status_code} downloading {url}")

            # Add a delay to be respectful to the server (optional, but recommended)
            time.sleep(0.1)  # 0.1 second delay

        except requests.exceptions.RequestException as e:
            print(f"Error downloading {url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {url}: {e}")

if __name__ == "__main__":
    # Define the base URL and the range of numbers
    base_url = "https://2025electionresults.comelec.gov.ph/data/er/142/"
    #142 = City of San Jose Delmonte Bulacan
    #pricint number
    start_number = 14200000
    end_number = 14299999

    # Specify the directory to save the files (optional)
    save_directory = "comelec_data"  # Create a folder named "comelec_data"

    # Call the function to download the files
    download_json_files(start_number, end_number, base_url, save_directory)
    print("Download process complete.")

import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor

def download_file(number, base_url, directory):
    """Downloads a single JSON file."""
    filename = f"{number:08d}.json"
    url = f"{base_url}{filename}"
    filepath = os.path.join(directory, filename)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Downloaded: {url} to {filepath}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing {url}: {e}")
    finally:
        time.sleep(0.1)  # Add a delay after each request

def download_json_files_parallel(start_number, end_number, base_url, directory=".", max_workers=5):
    """
    Downloads JSON files in parallel from a given base URL, iterating through a range of numbers.

    Args:
        start_number (int): The starting number for the filename.
        end_number (int): The ending number for the filename.
        base_url (str): The base URL of the JSON files (without the filename).
        directory (str, optional): The directory to save the downloaded files. Defaults to the current directory.
        max_workers (int, optional): The maximum number of concurrent threads. Defaults to 5.

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

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, i, base_url, directory)
                   for i in range(start_number, end_number + 1)]
        # Optionally, you can wait for all tasks to complete and handle exceptions
        # for future in futures:
        #     try:
        #         future.result()
        #     except Exception as e:
        #         print(f"A thread raised an exception: {e}")

if __name__ == "__main__":
    # Define the base URL and the range of numbers
    base_url = "https://2025electionresults.comelec.gov.ph/data/er/740/"
    #740 = City of Marikina
    #precinct number
    start_number = 74020000
    end_number = 74029999

    # Specify the directory to save the files (optional)
    save_directory = "marikina_city"  # Create a folder named "marikina_city"

    # Call the function to download the files in parallel
    download_json_files_parallel(start_number, end_number, base_url, save_directory, max_workers=10) # Increased max_workers
    print("Download process complete.")
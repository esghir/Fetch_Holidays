import requests
import json, os
import logging
import pandas as pd

api_key = "c0+QTQ9YuVrs0iasHPLU3A==HQqtCYpj2bNBEW7O"
year = 2023
country = "US"


def fetch_holidays(year, country, api_key):
    api_call_count = 0  # Initialize the API call count variable

    base_url = "https://date.nager.at/api/v3"

    response = requests.get(
        f"{base_url}/PublicHolidays/{year}/{country}", headers={"X-Api-Key": api_key}
    )

    if response.status_code == 200:
        holidays = response.json()
        logging.info(f"Successfully fetched holidays for {country} {year}")
        return holidays
    else:
        logging.error(
            f"Failed to fetch holidays for {country} {year}. Status code: {response.status_code}"
        )
        return []


holidays = fetch_holidays(year, country, api_key)

# Convert holidays list to pandas DataFrame
holidays_df = pd.DataFrame(holidays)

# Convert date strings to datetime objects
holidays_df["date"] = pd.to_datetime(holidays_df["date"])

# Sort holidays by date
holidays_df = holidays_df.sort_values("date")

print("US Holidays for 2023:")
# Save the DataFrame to a CSV file
output_file = country + "_holidays_" + str(year) + ".csv"
output_file_path = f"../reports/{output_file}"
if os.path.exists(output_file_path):
    # Modify the file if it exists
    holidays_df.to_csv(output_file_path, index=False, mode="a")  # Append mode
    print(f"\nThe file has already existed. Please check the file.")
else:
    # Create the file if it doesn't exist
    holidays_df.to_csv(output_file_path, index=False, mode="w")  # Write mode
    print(f"\nHolidays data saved to {output_file}")
# Check if the file exists

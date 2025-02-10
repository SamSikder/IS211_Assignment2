import argparse
import urllib.request
import logging
import csv
from datetime import datetime
def downloadData(url):
    '''Download CSV file from a URL and return its contents as a string.'''
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def processData(data):
    """Processes CSV data and logs errors for invalid dates."""

    # Configure logging
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    logger.addHandler(handler)

    personData = {}
    lines = data.split("\n")
    reader = csv.reader(lines)
    next(reader)  # Skip header row

    for lineno, row in enumerate(reader, start=1):
        if len(row) < 3:
            continue  # Skip empty lines

        try:
            person_id = int(row[0])  # Convert ID to integer
            name = row[1]
            birthday = datetime.strptime(row[2], "%d/%m/%Y").date()  # Convert birthday
            personData[person_id] = (name, birthday)
        except (ValueError, IndexError):
            logger.error(f"Error processing line #{lineno} for ID #{row[0] if row else 'Unknown'}")

    return personData
def displayPerson(person_id, personData):
    """Displays person's information based on ID."""
    if person_id in personData:
        name, birthday = personData[person_id]
        print(f"Person #{person_id} is {name} with a birthday of {birthday}")
    else:
        print("No user found with that id.")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="URL of the CSV file")
    args = parser.parse_args()

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    personData = processData(csvData)

    while True:
        try:
            person_id = int(input("Enter an ID to lookup (0 or negative to exit): "))
            if person_id <= 0:
                break
            displayPerson(person_id, personData)
        except ValueError:
            print("Please enter a valid integer ID.")

if __name__ == "__main__":
    main()

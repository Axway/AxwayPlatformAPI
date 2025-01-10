import json
import os
import logging
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import requests
import dotenv
from funcsession import Authenticate

def main():
    # Load environment variables
    dotenv_path = "conf/.env"
    dotenv.load_dotenv(dotenv_path)

    # Constants
    URL = "https://platform.axway.com/api/v1/"
    URL_TOKEN = 'https://login.axway.com/auth/realms/Broker/protocol/openid-connect/token'
    ORG_ID = os.getenv("ORG_ID")
    PLATFORM_CLIENT = os.getenv("PLATFORM_CLIENT")
    PLATFORM_KEY = os.getenv("PLATFORM_KEY")

    # Get current date
    today = date.today()

    # Get first and last day of the previous month
    first_day = today.replace(day=1) - relativedelta(months=1)
    last_day = today.replace(day=1) - timedelta(days=1)

    # Format dates
    start = first_day.strftime('%d/%m/%Y')
    end = last_day.strftime('%d/%m/%Y')

    # Get access token
    data = {
        "grant_type": "client_credentials",
        "client_id": PLATFORM_CLIENT,
        "client_secret": PLATFORM_KEY
    }

    # Authenticate and generate report
    s, urlST = Authenticate('USER_GROUP')

    response = requests.post(URL_TOKEN, data=data, timeout=10)
    response.raise_for_status()  # Check for request errors
    token_payload = response.json()

    # Set headers and parameters
    headers = {
        'Authorization': f"Bearer {token_payload['access_token']}",
        "Content-Type": "application/json"
    }
    params = {'org_id': ORG_ID}

    # Fetch usage data
    resource = 'usage/'
    response = requests.get(URL + resource, headers=headers, params=params, timeout=10)
    response.raise_for_status()  # Check for request errors
    if response.ok:
        logging.info("Got current stats: %s", response.json())

    report_filename = f"usage-report-last-month-{today}.json"
    resource = "statisticsSummary/generateReport/"
    params = {
        'startDate': start,
        'endDate': end,
        'includeTransfersIn': True,
        'includeActiveUsersCount': True,
        'includeIncomingFileVolume': True
    }

    response = s.get(urlST + resource, params=params)
    response.raise_for_status()  # Check for request errors

    # Save report to file
    os.makedirs("Reports", exist_ok=True)
    with open(f"Reports/{report_filename}", "w", encoding="utf8") as report:
        json.dump(response.json(), report, indent=4)

    # Upload report
    resource = 'usage/'
    payload = {'uploadMethod': 'automatic'}
    with open(f'Reports/{report_filename}', encoding="utf8") as my_report:
        contents = my_report.read()
    files = [
        ('file', (report_filename, contents, 'application/json'))
    ]
    headers.pop('Content-Type', None)  # Remove Content-Type header for file upload

    response = requests.post(URL + resource, headers=headers, data=payload, files=files, timeout=10)
    if response.ok:
        logging.info("Successfully submitted report to the Axway Platform")
    else:
        logging.error("Error submitting report: %s", response.text)

if __name__ == "__main__":
    main()

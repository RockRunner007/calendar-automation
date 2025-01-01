from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from datetime import datetime, timedelta, timezone

import os.path
import pickle
import logging

def get_creds():
    # If modifying these SCOPES, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def configure_logging():
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )

def main():
    """Shows basic usage of the Google Calendar API.
    Lists the next 10 events on the user's calendar.
    """
    
    configure_logging()

    service = build('calendar', 'v3', credentials=get_creds())
    calendar_id = None

    #List all calendars
    logging.info("Fetching all calendars:")
    calendar_list = service.calendarList().list().execute().get('items', [])
    for calendar in calendar_list:
        if calendar['summary'] == 'Carlson Cycling':
            calendar_id = calendar['id']
            logging.info(f'Calendar ID is {calendar['id']} for {calendar['summary']}')
    
    #List one event per specific calendar
    logging.info('Getting the upcoming 1 event from a specific calendar')
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=1, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    if not events:
        logging.error('No upcoming events found.')
    
    for event in events:
        logging.info(f'{event['summary']}')

    #Insert an event
    new_date = datetime.now(timezone.utc) + timedelta(days=0, hours=1)
    event = {
        'summary': 'Python Meeting',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A meeting to discuss Python projects.',
        'start': {
            'dateTime': datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': new_date.isoformat().replace("+00:00", "Z"),
            'timeZone': 'America/Chicago',
        },
    }
    # created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    # print(f"Created event: {created_event['id']}")

if __name__ == '__main__':
    main()
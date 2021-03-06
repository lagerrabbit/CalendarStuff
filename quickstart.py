from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import dateutil.parser

from jinja2 import Environment, FileSystemLoader

import datetime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API P ython Quickstart'

def df(value):
    key = ""
    key = 'dateTime' if 'dateTime' in value else ""
    key = 'date' if key == "" and "date" in value else key
    if key == "":
        print(value)
        return ""
    format="%I:%M" if key == 'dateTime' else "%d %b " 
    
    dv = value[key]
    d = dateutil.parser.parse(dv)
    o = d.strftime(format)
    return o

def ed(value):
    key = ""
    key = 'dateTime' if 'dateTime' in value else ""
    key = 'date' if key == "" and "date" in value else key
    if key == "":
        print(value)
        return ("", "")
    return (key, dateutil.parser.parse(value[key]))
   

   
def dd(event):
    start = ed(event['start'])
    end = ed(event['end'])
    
    o = ""
    if start[0] == "date":
        o = start[1].strftime("%d %b")
 
    if start[0] == "dateTime":
        o = start[1].strftime("%I:%M")

    if end[0] == "date":
        o = o + " - " + end[1].strftime("%d %b")
 
    if end[0] == "dateTime":
        o = o + " - " + end[1].strftime("%I:%M %d %b")        
    return o


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=100, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
	
    default = 'Details Coming Soon'
    if not events:
        print('No upcoming events found.')
        # GET https://www.googleapis.com/calendar/v3/calendars/primary/events/n6arcebcdv2b28ds4u8dr14pis?fields=description&key={YOUR_API_KEY}
    
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    j2_env.filters['datetime'] = df
    j2_env.filters['dd'] = dd

                         
    print(j2_env.get_template('eventsByName.html').render(events=events))
    
#    for event in events:
    
        
#        description = event.get('description', default)

#        start = event['start'].get('dateTime', event['start'].get('date'))
		
#        print ("Time: %s Event: %s Description: %s"%(start, event['summary'], description))


if __name__ == '__main__':
    main()
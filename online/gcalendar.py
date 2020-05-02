# Connection to 12B class calendar, using Google Calendar API
import datetime
import os.path
import pickle
from datetime import date
from datetime import timedelta
from typing import Tuple, Union

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from helpers.logger import logger


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class CalendarEventManager(object):
    def __init__(self, name: str, _date: datetime.date = None) -> None:
        """

        :param name: Name of the person's whose birthday it is
        :param _date: Date of that person's birthday

        """

        self.name = name
        self.date = _date

        # self.formatted = formatter(self.date)
        self.event = {
            'summary': f"{self.name.capitalize()}'s birthday!",

            'start': {'date': f"{formatter(self.date)}",
                      'timezone': "Asia/Dubai"},

            'end': {'date': f"{formatter(self.date, days=1)}",
                    'timezone': "Asia/Dubai"},

            'recurrence': ["RRULE:FREQ=YEARLY"],

            'reminders': {'useDefault': False,
                          'overrides': [
                              {'method': 'email', 'minutes': 3540}  # Reminds 3 days before at 1pm by email
                          ]},

            'colorId': '11'

        }

    def add_event(self) -> None:
        """
        Adds event to Google Calendar. Name and date must be specified in the class instance.
        """
        if self.date is None:
            raise ValueError("Date must be specified!")

        event = service.events().insert(calendarId='primary', body=self.event).execute()
        logger(message=f"{self.event['summary']} was added.")

    def update_event(self, new_date: datetime.datetime):
        """
        Updates the event in Google Calendar. Parameter 'new_date' must be specified, 'date' need not be specified in
        class instance.
        """
        # Get event id of the event to be modified
        events = service.events().list(calendarId='primary').execute()

        for event in events['items']:
            if self.name in event['summary']:
                print(f"Match: {event['summary']}")
                self.event['start']['date'] = f"{formatter(new_date)}"
                self.event['end']['date'] = f"{formatter(new_date + timedelta(days=1))}"

                updated_event = service.events().update(calendarId='primary', eventId=event['id'],
                                                        body=self.event).execute()

                logger(f"Successfully updated {self.name}'s birthday: {updated_event['start']['date']}.")

                break
        else:
            raise ValueError("Event not found")


def formatter(today: datetime.date, days: int = 0, format_style: str = "") -> Union[str, None]:
    """
    Formats the date and returns it in the form used in the Google Calendar API. Adds 'days' no. of days to the date
    if 'days' parameter is specified.

    Args:
        :param format_style: If specified, type 'DD/MM' to format it in that way.
        :param days: Number of days to add to the date.
        :param today: A datetime object

    """

    if isinstance(today, datetime.datetime):
        if days != 0:
            today += timedelta(days=days)

        if format_style == "DD/MM":
            return today.strftime("%d/%m")

        return today.strftime("%Y-%m-%d")
    return


def get_next_bday() -> Tuple[int, str]:
    """
    Fetches a birthday from google calendar (12B only) and returns the number of days till the next birthday of a
    person along with their name.

    :returns tuple(int, string)
    """

    bday_list = []

    events = service.events().list(calendarId='primary').execute()

    for event in events['items']:
        if 'birthday' in event['summary']:
            index = event['summary'].find("'")  # Find index of "'" so we can get name from event.
            bday_list.append(  # Parse string to datetime object, and append that along with name of the person
                (datetime.datetime.strptime(event['start']['date'], "%Y-%m-%d"), event['summary'][:index]))

    today = date.today()
    today = datetime.datetime.strptime(str(today), "%Y-%m-%d")  # Parses today's date (time object) into datetime object

    diff = []

    for bday_date in bday_list:
        day_diff = bday_date[0] - today  # Finds diff from today to birthday
        diff.append((day_diff.days, bday_date[1]))

    print(diff, '\n')
    next_bday = min(lowest for lowest in diff if lowest[0] >= 0)
    print(f"Next birthday: {next_bday}\n")
    return next_bday  # Returns lowest (i.e. next bday) in the calendar


def main() -> None:
    """
    Sets up the Google Calendar API for easy use.
    """

    global service
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(r'./creds/token.pickle'):
        with open('./creds/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./creds/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


if __name__ == '__main__':
    main()
    get_next_bday()
    # Commented out just in case we need it again-
    # bdays = [("Ruchika", datetime.datetime(2021, 1, 17)),
    #          ("Nikil", datetime.datetime(2021, 1, 26)),
    #          ("Samir", datetime.datetime(2021, 2, 2)),
    #          ("Sakshi", datetime.datetime(2020, 3, 13)),
    #          ("Ann", datetime.datetime(2020, 3, 25)),
    #          ("Ronit", datetime.datetime(2020, 3, 28)),
    #          ("Sahil", datetime.datetime(2020, 4, 3)),
    #          ("Joel", datetime.datetime(2020, 4, 16)),
    #          ("Ali", datetime.datetime(2020, 5, 4)),
    #          ("Sahel", datetime.datetime(2020, 5, 13)),
    #          ("Areeb", datetime.datetime(2020, 5, 31)),
    #          ("Ashwin", datetime.datetime(2020, 6, 3)),
    #          ("Antony", datetime.datetime(2020, 7, 25)),
    #          ("Adeep", datetime.datetime(2020, 8, 4)),
    #          ("Angelia", datetime.datetime(2020, 8, 15)),
    #          ("Jaden", datetime.datetime(2020, 9, 4)),
    #          ("Shweta", datetime.datetime(2020, 9, 24)),
    #          ("Raghunath", datetime.datetime(2020, 10, 21)),
    #          ("Juanita", datetime.datetime(2020, 10, 31)),
    #          ("Samrin", datetime.datetime(2020, 10, 31)),
    #          ("Uma", datetime.datetime(2020, 11, 1)),
    #          ("Mathew", datetime.datetime(2020, 12, 30)),
    #          ("Rithima", datetime.datetime(2020, 12, 31))]
    #
    # for bday in bdays:
    #     add_event(*bday)
    # add_event("Harshil", datetime.datetime(2020, 11, 25))

    # e = CalendarEventManager("Harshil")
    # # e.add_event()
    # e.update_event(datetime.datetime(2020, 11, 26))

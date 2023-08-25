from google.oauth2.service_account import Credentials
from googleapiclient import discovery


class GoogleCalendar:
    """Настройка ."""

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    CRED_FILE = "recruitment-process-395710-2cefd3ed6bc8.json"

    def __init__(self):
        """."""
        credentials = Credentials.from_service_account_file(
            filename=self.CRED_FILE, scopes=self.SCOPES
        )
        self.service = discovery.build("calendar", "v3", credentials=credentials)
        # return service, credentials


obj = GoogleCalendar()

cal_list = calendar_list = obj.service.calendarList().list().execute()

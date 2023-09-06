import datetime
import os

TOKEN = os.environ.get("TOKEN")
TIMETABLE_URL = os.environ.get("TIMETABLE_URL")
TIMETABLE_CHANGES_URL = os.environ.get("TIMETABLE_CHANGES_URL")
FIRST_DAY = datetime.datetime(2023, 9, 4)
GROUP_NAME = os.environ.get("GROUP_NAME")

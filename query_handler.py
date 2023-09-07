import bs4
import aiohttp
from bs4 import BeautifulSoup
from telebot.formatting import hbold

from config import *
from timetable_changes_handler import get_timetable_changes
from weekdays_utils import WeekType, get_week_type, get_weekday_name
from timetable_utils import Class, DayTimetable


async def get_timetable(query_date: datetime.datetime):
    async with aiohttp.ClientSession() as session:
        async with session.get(TIMETABLE_URL) as session_response:
            response = session_response

            if response.status != 200:
                print(f"Error while getting timetable. Status code - {response.status}")
                return "Ошибка! Уже исправляем!"

            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    tables: list[bs4.Tag] = soup.find_all(attrs={"class": "customized timetable"})
    week_type = get_week_type(query_date)
    if week_type == WeekType.ODD:
        current_week_table = tables[0]
    else:
        current_week_table = tables[1]

    # Added 2 to this because there are two columns in table before the actual classes columns
    weekday_index_in_table = query_date.weekday() + 2
    classes: list[Class] = list()

    for tr in current_week_table.findChild("tbody").find_all("tr"):
        row: bs4.Tag = tr
        columns = row.find_all("td")
        class_number = columns[0].get_text().strip()
        class_time = fix_timetable_time(columns[1].get_text().strip())
        class_info = fix_class_info(columns[weekday_index_in_table].get_text())
        classes.append(Class(class_number, class_time, class_info))

    weekday_index = query_date.weekday()
    weekday_name = get_weekday_name(weekday_index, week_type)
    weekday_name = hbold(weekday_name)
    timetable = DayTimetable(weekday_name, classes)
    result = str(timetable)

    if timetable.is_weekend:
        result += "Выходной!"
        return result

    changes = await get_timetable_changes(query_date)
    result += "\n\n"
    result += changes
    return result


def fix_timetable_time(raw_timetable_time: str):
    lines = raw_timetable_time.split("\n")
    result = " - ".join(map(lambda line: line.strip(), lines))
    return result


def fix_class_info(raw_class_info: str):
    lines = filter(lambda line: line != "", raw_class_info.split("\n"))
    fixed_lines = list(map(lambda line: line.strip(), lines))
    result = list()
    for i in range(0, len(fixed_lines), 3):
        result.append(f"Предмет: {fixed_lines[i]}")
        result.append(f"Преподаватель: {fixed_lines[i + 1]}")
        result.append(f"Кабинет: {fixed_lines[i + 2]}")
    return "\n".join(result)

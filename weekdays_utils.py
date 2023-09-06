from enum import Enum
from config import *


class WeekType(Enum):
    ODD = 1
    EVEN = 2


class Gender(Enum):
    MASCULINE = 0
    FEMININE = 1
    NEUTER = 2


class Weekday:
    def __init__(self, name: str, gender: Gender):
        self.name = name
        self.gender = gender


weekdays = {
    0: Weekday("понедельник", Gender.MASCULINE),
    1: Weekday("вторник", Gender.MASCULINE),
    2: Weekday("среда", Gender.FEMININE),
    3: Weekday("четверг", Gender.MASCULINE),
    4: Weekday("пятница", Gender.FEMININE),
    5: Weekday("суббота", Gender.FEMININE),
    6: Weekday("воскресенье", Gender.NEUTER)
}


def get_week_type(date: datetime.datetime) -> WeekType:
    delta = date - FIRST_DAY
    day_num = delta.days
    if day_num % 14 < 7:
        return WeekType.ODD
    return WeekType.EVEN


def get_weekday_name(weekday_index: int, week_type: WeekType) -> str:
    weekday = weekdays[weekday_index]

    match weekday.gender:
        case Gender.MASCULINE if week_type == WeekType.ODD:
            weekday_type = "Первый"
        case Gender.MASCULINE if week_type == WeekType.EVEN:
            weekday_type = "Второй"
        case Gender.FEMININE if week_type == WeekType.ODD:
            weekday_type = "Первая"
        case Gender.FEMININE if week_type == WeekType.EVEN:
            weekday_type = "Вторая"
        case Gender.NEUTER if week_type == WeekType.ODD:
            weekday_type = "Первое"
        case Gender.NEUTER if week_type == WeekType.EVEN:
            weekday_type = "Второе"
        case _:
            weekday_type = ""

    return f"{weekday_type} {weekday.name}"
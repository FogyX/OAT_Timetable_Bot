from telebot import formatting
from telebot.formatting import hbold


class Class:
    def __init__(self, number_of_class, class_time, class_info):
        self.number_of_class = number_of_class
        self.class_time = class_time
        self.class_info = class_info

    def is_empty(self):
        return self.class_info == ""


class DayTimetable:
    def __init__(self, weekday_name: str, classes: list[Class]):
        self.weekday_name = weekday_name
        self.classes = classes

        if all([class_data.is_empty() for class_data in classes]):
            self.is_weekend = True
        else:
            self.is_weekend = False

    def __str__(self):
        classes_info: list[str] = list()
        classes_info.append(self.weekday_name)

        for class_data in self.classes:
            if class_data.class_info == "":
                continue

            class_primary_info = formatting.hbold(f"{class_data.class_time} - {class_data.number_of_class} пара:")
            class_info_line = f"{class_primary_info}\n{class_data.class_info}"
            classes_info.append(class_info_line)

        result = "\n\n".join(classes_info)

        if self.is_weekend:
            result += "\n\n"

        return result


class ChangedClass:
    def __init__(self, class_number_was, class_room_was, class_subject_was, class_teacher_was,
                 class_number_became, class_room_became, class_subject_became, class_teacher_became):
        self.class_number_was: str = class_number_was
        self.class_room_was: str = class_room_was
        self.class_subject_was: str = class_subject_was
        self.class_teacher_was: str = class_teacher_was
        self.class_number_became: str = class_number_became
        self.class_room_became: str = class_room_became
        self.class_subject_became: str = class_subject_became
        self.class_teacher_became: str = class_teacher_became

    def __str__(self):
        result = ""
        result += hbold("Было:\n")
        result += f"{self.class_number_was} пара\n"

        if self.class_subject_was is None:
            result += "Нет пары\n\n"
        else:
            result += f"Предмет: {self.class_subject_was}\n"
            result += f"Преподаватель: {self.class_teacher_was}\n"
            result += f"Кабинет: {self.class_room_was}\n\n"

        if self.class_subject_became.lower() == "отмена":
            result += "Пара отменена.\n"
            return result

        result += hbold("Стало:\n")
        result += f"{self.class_number_became} пара\n"
        result += f"Предмет: {self.class_subject_became}\n"
        result += f"Преподаватель: {self.class_teacher_became}\n"
        result += f"Кабинет: {self.class_room_became}\n"
        return result

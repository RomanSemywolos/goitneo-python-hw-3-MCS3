import pickle
from collections import UserDict
from datetime import datetime


class PhoneException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class BirthdayException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if self.validate(value):
            self.value = value
        else:
            raise PhoneException("Invalid phone number.")

    @staticmethod
    def validate(value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        if self.validate(value):
            self.value = value
        else:
            raise BirthdayException("Invalid birthday date.")

    @staticmethod
    def validate(value):
        today = datetime.today().date()
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            if birthday > today:
                return False
        except Exception:
            return False
        return True


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_number):
        for i, phone in enumerate(self.phones):
            if phone.value == phone_number:
                del self.phones[i]
                return "Phone removed."
        raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return "Phone changed."
        raise ValueError("Phone not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birthday added"

    def __str__(self):
        return f"Contact name: {self.name.value},\
        phones: {'; '.join(p.value for p in self.phones)}, \
        birthday: {self.birthday.value if self.birthday else 'Uknown date'}"


class AddressBook(UserDict):
    file_name = "data.bin"

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        del self.data[name]

    def get_birthdays_per_week(self):
        week = {"Monday": [], "Tuersday": [], "Wednesday": [], "Thursday": [], "Friday": []}
        today = datetime.today().date()
        birthday_info = []
        for name, record in self.data.items():
            if not record.birthday:
                continue
            birthday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            birthday_this_year = birthday_date.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)
            delta_days = (birthday_this_year - today).days

            if delta_days < 7:
                weekday = birthday_this_year.weekday()
                if weekday in [0, 5, 6]:
                    week["Monday"].append(name)
                elif weekday == 1:
                    week["Tuersday"].append(name)
                elif weekday == 2:
                    week["Wednesday"].append(name)
                elif weekday == 3:
                    week["Thursday"].append(name)
                elif weekday == 4:
                    week["Friday"].append(name)

        for key, value in week.items():
            if value != []:
                birthday_info.append(f"{key}: {', '.join(value)}\n")
        if birthday_info:
            return birthday_info
        else:
            return "No birthays next week ("


if __name__ == "__main__":
    print("Hello. This is not the main file.")
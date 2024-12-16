import csv
import re
from datetime import datetime

class HelperFunctions:
    def __init__(self, filename):
        self.filename = filename
        self.phonebook = self.load_phonebook()

    # print phonebook
    def print_phonebook(self):
        """Print phonebook."""
        for record in self.phonebook:
            print(record)

    def isExitingPerson (self, name, surname):
        """Check if person is in phonebook"""
        check = next((r for r in self.phonebook if r["Имя"] == name and r["Фамилия"] == surname), None)
        return check

    def appendRecord (self, record):
        self.phonebook.append(record)

    def changeRecord (self, record_update):
        for record in self.phonebook:
            if record["Имя"] == record_update["Имя"] and record["Фамилия"] == record_update["Фамилия"]:
                record["Номер телефона"] = record_update["Номер телефона"]
                record["Дата рождения"] = record_update["Дата рождения"]
                break
        self.save_phonebook()

    # function find records for field and value (if num_of_elems = 1) or for name and surname (if num_of_elems = 2)
    # num_of_elems  - it's the number of values for search
    def searchRecord (self,field_for_search,  elem_for_search, num_of_elems):
        if num_of_elems == 1:
            records = [r for r in self.phonebook if r[field_for_search] == elem_for_search]
            return records
        else: # num_of_elems = 2
            name = field_for_search
            surname = elem_for_search
            records = [record for record in self.phonebook if record["Имя"] == name and record["Фамилия"] == surname]
            return records

    def deleteRecord (self, name, surname):
        self.phonebook = [r for r in self.phonebook if r["Имя"] != name or r["Фамилия"] != surname]
        self.save_phonebook()



    # Helper functions
    def load_phonebook(self):
        """Load phonebook from file."""
        try:
            with open(self.filename, mode="r", newline='', encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            return []

    def save_phonebook(self):
        """Save phonebook to file."""
        try:
            with open(self.filename, "w", newline='', encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=["Имя", "Фамилия", "Номер телефона", "Дата рождения"])
                writer.writeheader()
                writer.writerows(self.phonebook)
            print(f"Телефонный справочник успешно сохранен в {self.filename}.")
        except PermissionError:
            print(f"Ошибка: Не удается сохранить данные. Закройте файл {self.filename} и попробуйте снова.")
        except Exception as e:
            print(f"Неизвестная ошибка при сохранении файла: {e}")

    def validate_name(self, name):
        """Validate name or surname."""
        return re.match(r"^[A-ZА-Я][a-zа-яA-ZА-Я0-9 ]*$", name)

    def validate_phone(self, phone):
        """Validate and normalize phone number."""
        if len(phone) == 12 and phone.startswith("+7"):
            return "8" + phone[2:]
        return phone if len(phone) == 11 and phone.startswith("8") else None

    def validate_date(self, date_str):
        """Validate date of birth."""
        try:
            return datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            return None

    def calculate_age(self, record):
        """Calculate age based on birth date."""
        name = record["Имя"]
        surname = record["Фамилия"]
        birth_date = [r for r in self.phonebook if r["Имя"] == name and r["Фамилия"] == surname]
        birth_date = birth_date[0]["Дата рождения"]
        birth_date = datetime.strptime(birth_date, "%d.%m.%Y").date()
        today = datetime.now().date()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def writeEnding (self, years):
        last_two_digits = years % 100
        last_digit = years % 10

        if 11 <= last_two_digits <= 14:
            return "лет"
        elif last_digit == 1:
            return "год"
        elif 2 <= last_digit <= 4:
            return "года"
        else:
            return "лет"

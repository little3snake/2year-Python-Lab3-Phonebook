import csv
import re
from datetime import datetime

from HelperFunctions import *
from Actions import *

# Constants
FILENAME = "phonebook.csv"

def main():

    print ("Запуск программы Телефонный справочник...")
    print("Вы хотите изменить имя файла для справочника? Сейчас дефолтное имя phonebook.csv")
    command = input("Введите 1 (Да) или 0 (Нет): ").strip()
    if command == "1":
        name_book = input("Введите имя (.csv) ").strip()
        phonebook = HelperFunctions(name_book)
    else:
        phonebook = HelperFunctions(FILENAME)

    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Просмотреть все записи.")
        print("2. Добавить запись.")
        print("3. Поиск в справочнике.")
        print("4. Удалить запись.")
        print("5. Редактировать запись.")
        print("6. Получить возраст человека в справочнике.")
        print("7. Завершить работу.\n")
        command = input("Введите номер вашего выбора: ").strip()

        if command == "1":
            # list
            print("\nТелефонный справочник:")
            phonebook.print_phonebook()

        elif command == "2":
            # add
            name = input("Введите имя: ").strip().capitalize()
            if not name:
                print("Некорректное имя (вы его не ввели).")
                continue
            surname = input("Введите фамилию: ").strip().capitalize()
            if not surname:
                print("Некорректная фамилия (вы её не ввели).")
                continue

            # проверяем, существует ли запись с таким именем и фамилией
            existing_record = phonebook.isExitingPerson(name, surname)
            # если существует
            if existing_record:
                print(f"Запись с именем {name} и фамилией {surname} уже существует.")
                print("Существующая запись:", existing_record)

                # предлагаем пользователю три варианта
                print("\nЧто вы хотите сделать?")
                print("1. Изменить существующую запись.")
                print("2. Изменить Имя и Фамилию для новой записи.")
                print("3. Вернуться к выбору команды.\n")
                choice = input("Введите номер вашего выбора: ").strip()

                if choice == "1":
                    # Изменяем существующую запись
                    print("\nВы редактируете запись.")
                    print("\nКакое поле вы хотите изменить (имя и фамилия как уникальный идентификатор не редактируются)?")
                    print("1. Номер телефона.")
                    print("2. Дата рождения.\n")
                    field = input("Введите номер вашего выбора: ").strip()

                    if field == "1":
                        field_name = "Номер телефона"
                        new_value = phonebook.validate_phone(input("Введите новое значение для номера телефона: ").strip())
                        if not new_value:
                            print("Некорректный номер телефона. Возврат к выбору команды.")
                            continue

                    elif field == "2":
                        field_name = "Дата рождения"
                        new_value = phonebook.validate_date(input("Введите новое значение для даты рождения: ").strip())
                        if not new_value:
                            print("Некорректная дата. Возврат к выбору команды.")
                            continue
                        new_value = new_value.strftime("%d.%m.%Y")
                    else:
                        print("Неверный выбор. Возврат к выбору команды.")
                        continue

                    existing_record[field_name] = new_value
                    phonebook.changeRecord(existing_record)
                    print("Запись успешно изменена.")

                elif choice == "2":
                    # Изменяем Имя и Фамилию для новой записи
                    name = input("Введите новое имя: ").strip().capitalize()
                    if not name:
                        print("Некорректное имя (вы его не ввели).")
                        continue
                    surname = input("Введите новую фамилию: ").strip().capitalize()
                    if not surname:
                        print("Некорректная фамилия (вы её не ввели).")
                        continue
                    phone = phonebook.validate_phone(input("Введите номер телефона: ").strip())
                    if not phone:
                       print("Некорректный номер телефона.")
                       continue
                    dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
                    if dob:
                        dob = phonebook.validate_date(dob)
                        if not dob:
                            print("Некорректная дата. Возврат к выбору команды.")
                            continue
                    else:
                        dob = None

                    phonebook.appendRecord({
                        "Имя": name,
                        "Фамилия": surname,
                        "Номер телефона": phone,
                        "Дата рождения": dob.strftime("%d.%m.%Y") if dob else ""
                    })
                    phonebook.save_phonebook()
                    print("Новая запись успешно добавлена.")

                elif choice == "3":
                    print("Возврат к выбору команды.")
                    continue

                else:
                    print("Неверный выбор. Возврат к выбору команды.")
                    continue

            else:
                # Если записи не существует -- добавляем новую
                phone = phonebook.validate_phone(input("Введите номер телефона (работает только для российского региона +7 или 8): ").strip())
                if not phone:
                    print("Некорректный номер телефона.")
                    continue
                dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
                if dob:
                    dob = phonebook.validate_date(dob)
                    if not dob:
                        print("Некорректная дата. Возврат к выбору команды.")
                        continue
                else:
                    dob = None

                phonebook.appendRecord({
                    "Имя": name,
                    "Фамилия": surname,
                    "Номер телефона": phone,
                    "Дата рождения": dob.strftime("%d.%m.%Y") if dob else ""
                })
                phonebook.save_phonebook()
                print("Запись добавлена.")

        elif command == "3":
            # search
            print("\nПо какому полю вы хотите сделать поиск?")
            print("1. Имя.")
            print("2. Фамилия.")
            print("3. Номер телефона.")
            print("4. Дата рождения.")
            print("5. Имя и фамилия\n") # остальные комбинации полей нет смысла делать, потому что ими оочень редко пользуются


            field = input("Введите номер вашего выбора: ").strip()
            field_name = (lambda f: {
                "1": "Имя",
                "2": "Фамилия",
                "3": "Номер телефона",
                "4": "Дата рождения",
                "5": "Имя и фамилия"
            }.get(f, None))(field)
            if field_name is None:
                print("Некорректный ввод данных. Возврат к выбору команды.")
                continue
            if field_name in ("1", "2", "3", "4"):
                value = input(f"Введите значение для поиска в поле {field_name}: ").strip()
                if not value: # error
                    print("Некорректный ввод значения (вы его не ввели).")
                    continue
                if field == "1" or field == "2":
                    value = value.capitalize()
                results = phonebook.searchRecord(field_name, value, num_of_elems=1)
            else: # "5"
                name = input("Введите имя: ").strip().capitalize()
                if not name: # error
                    print("Некорректное имя (вы его не ввели).")
                    continue
                surname = input("Введите фамилию: ").strip().capitalize()
                if not surname: # error
                    print("Некорректная фамилия (вы её не ввели).")
                    continue
                results = phonebook.searchRecord(name, surname, num_of_elems=2)

            if results != []:
                print("\nНайденные записи:")
                for record in results:
                    print(record)
            else:
                print("\nНайденные записи: отсутствуют")


        elif command == "4":
            # delete
            name = input("Введите имя: ").strip().capitalize()
            if not name:
                print("Некорректное имя (вы его не ввели).")
                continue
            surname = input("Введите фамилию: ").strip().capitalize()
            if not surname:
                print("Некорректная фамилия (вы её не ввели).")
                continue
            #check if record is in phonebook
            results = phonebook.searchRecord(name, surname, num_of_elems=2)
            if results != []:
                phonebook.deleteRecord(name, surname)
                print("Запись удалена.")
            else:
                print("Такой записи не существует.")

        elif command == "5":
            # edit
            name = input("Введите имя: ").strip().capitalize()
            if not name:
                print("Некорректное имя (вы его не ввели).")
                continue
            surname = input("Введите фамилию: ").strip().capitalize()
            if not surname:
                print("Некорректная фамилия (вы её не ввели).")
                continue
            results = phonebook.searchRecord(name, surname, num_of_elems=2)
            if results != []:
                record = results[0]
                print("Текущая запись:", record)
                print("\nКакое поле вы хотите изменить?")
                print("1. Номер телефона.")
                print("2. Дата рождения.\n")
                field = input(
                    "Введите номер поля для изменения (имя и фамилию изменять нельзя тк это уникальный идентификатор): ").strip()
                field_name = (lambda f: {
                    "1": "Номер телефона",
                    "2": "Дата рождения"
                }.get(f, None))(field)
                if field_name is None:
                    print("Некорректный ввод данных.")
                    continue

                new_value = input(f"Введите новое значение для {field_name}: ").strip()
                if field_name == "Номер телефона":
                    new_value = phonebook.validate_phone(new_value)
                    if not new_value:
                        print("Некорректный номер телефона. Возврат к выбору команды.")
                        continue

                elif field_name == "Дата рождения":
                    new_value = phonebook.validate_date(input("Введите новое значение для даты рождения: ").strip())
                    if not new_value:
                        print("Некорректный ввод даты (она должна быть в формате дд.мм.гггг). Возврат к выбору команды.")
                        continue
                    new_value = new_value.strftime("%d.%m.%Y")

                record[field_name] = new_value
                phonebook.changeRecord(record)
                print("Данные успешно изменены.")
            else:
                print("Такой записи не существует.")


        elif command == "6":
            # age
            name = input("Введите имя: ").strip().capitalize()
            if not name:
                print("Некорректное имя (вы его не ввели).")
                continue
            surname = input("Введите фамилию: ").strip().capitalize()
            if not surname:
                print("Некорректная фамилия (вы её не ввели).")
                continue

            results = phonebook.searchRecord(name, surname, num_of_elems=2)
            if results is not None and results[0]["Дата рождения"] != "":
                record = results[0]
                rec_name = record["Имя"]
                rec_surname = record["Фамилия"]
                years = phonebook.calculate_age(record)
                ending = phonebook.writeEnding (int(years))
                print (f"Возраст {rec_surname} {rec_name} : {years} {ending}")
            else:
                print("Дата рождения отсутствует или запись не найдена.")

        elif command == "7":
            # quit
            break

        else:
            print("Неверная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()

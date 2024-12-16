# 1
def printList (phonebook):
    """Logic of 1step in main menu. Print phonebook in console"""
    print("\nТелефонный справочник:")
    phonebook.print_phonebook()

#2
# return in case "wrong input" return to main menu
def addRecord (phonebook):
    """Logic of 2step in main menu. Check and add record (or change) in phonebook"""
    name = phonebook.checker_name(phonebook.validate_name(input("Введите имя: ").strip().capitalize()))
    if not name: return
    surname = phonebook.checker_name(phonebook.validate_name(input("Введите фамилию: ").strip().capitalize()))
    if not surname: return
    # check is this record (name + surname) in phonebook
    existing_record = [phonebook.isExitingPerson(name, surname)]
    # if record exist
    if existing_record != [None]:
        print(f"Запись с именем {name} и фамилией {surname} уже существует.")
        print("Существующая запись:")
        phonebook.printSomeRecords(existing_record)
        # write 3 cases to user
        print("\nЧто вы хотите сделать?")
        print("1. Изменить существующую запись.")
        print("2. Изменить Имя и Фамилию для новой записи.")
        print("3. Вернуться к выбору команды.\n")
        choice = input("Введите номер вашего выбора: ").strip()

        if choice == "1":
            # Edit exiting record
            print("\nВы редактируете запись.")
            print("\nКакое поле вы хотите изменить (имя и фамилия как уникальный идентификатор не редактируются)?")
            print("1. Номер телефона.")
            print("2. Дата рождения.\n")
            field = input("Введите номер вашего выбора: ").strip()
            if field == "1":
                field_name = "Номер телефона"
                new_value = phonebook.validate_phone(input("Введите новое значение для номера телефона: ").strip())
                if not new_value: # error
                    print("Некорректный номер телефона (он должен начинаться с 8/+7 и быть с нужным количеством символов). Возврат к выбору команды.")
                    return
            elif field == "2":
                field_name = "Дата рождения"
                new_value = phonebook.validate_date(input("Введите новое значение для даты рождения (дд.мм.гггг): ").strip())
                if not new_value: # error
                    print("Некорректная дата (должна быть в формате дд.мм.гггг). Возврат к выбору команды.")
                    return
                new_value = new_value.strftime("%d.%m.%Y")
            else: # error
                print("Неверный выбор. Возврат к выбору команды.")
                return

            existing_record[0][field_name] = new_value
            phonebook.changeRecord(existing_record[0])
            phonebook.printSomeRecords(existing_record)
            print("Запись успешно изменена.")

        elif choice == "2":
            # Change name and surname for new record
            name = phonebook.checker_name(phonebook.validate_name(input("Введите имя: ").strip().capitalize()))
            if not name: return
            surname = phonebook.checker_name(
                phonebook.validate_name(input("Введите фамилию: ").strip().capitalize()))
            if not surname: return
            phone = phonebook.validate_phone(input("Введите номер телефона: ").strip())
            if not phone: # error
                print("Некорректный номер телефона (он должен начинаться с 8\+7 и быть с нужным количеством символов). Возврат к выбору команды.")
                return
            dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
            if dob:
                dob = phonebook.validate_date(dob)
                if not dob: # error
                    print("Некорректная дата (должна быть в формате дд.мм.гггг). Возврат к выбору команды.")
                    return
            else:
                dob = None

            record = {
                "Имя": name,
                "Фамилия": surname,
                "Номер телефона": phone,
                "Дата рождения": dob.strftime("%d.%m.%Y") if dob else ""
            }
            phonebook.appendRecord(record)
            phonebook.printSomeRecords([record])
            print("Новая запись успешно добавлена.")
        elif choice == "3":
            print("Возврат к выбору команды.")
            return
        else:
            print("Неверный выбор. Возврат к выбору команды.")
            return

    else:
        # if record doesn't exist -- add new record
        phone = phonebook.validate_phone(
            input("Введите номер телефона (работает только для российского региона +7 или 8): ").strip())
        if not phone: # error
            print("Некорректный номер телефона (он должен начинаться с 8\+7 и быть с нужным количеством символов). Возврат к выбору команды.")
            return
        dob = input("Введите дату рождения (дд.мм.гггг) или оставьте пустым: ").strip()
        if dob:
            dob = phonebook.validate_date(dob)
            if not dob: # error
                print("Некорректная дата (должна быть в формате дд.мм.гггг). Возврат к выбору команды.")
                return
        else:
            dob = None

        record = {
            "Имя": name,
            "Фамилия": surname,
            "Номер телефона": phone,
            "Дата рождения": dob.strftime("%d.%m.%Y") if dob else ""
        }
        phonebook.appendRecord(record)
        phonebook.printSomeRecords([record])
        print("Запись добавлена.")

#3
def searchRecord(phonebook):
    """Logic of 3step in main menu. Search record in phonebook"""
    print("\nПо какому полю вы хотите сделать поиск?")
    print("1. Имя.")
    print("2. Фамилия.")
    print("3. Номер телефона.")
    print("4. Дата рождения.")
    print("5. Имя и фамилия\n")  # combination of name and surname
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
        return

    if field in ("1", "2", "3", "4"):
        value = input(f"Введите значение для поиска в поле {field_name}: ").strip()
        if not value:  # error
            print("Некорректный ввод значения (вы его не ввели). Возврат к выбору команды.")
            return
        if field == "1" or field == "2":
            value = phonebook.checker_name(
                phonebook.validate_name(value.capitalize()))
            if not value: return
        elif field == "3":
            value = phonebook.validate_phone(value)
            if not value:  # error
                print("Некорректный номер телефона (он должен начинаться с 8\+7 и быть с нужным количеством символов). Возврат к выбору команды.")
                return
        else:
            value = phonebook.validate_date(value)
            if value:
                value = value.strftime("%d.%m.%Y")
            else: #error
                print("Некорректная дата (должна быть в формате дд.мм.гггг). Возврат к выбору команды.")
                return

        results = phonebook.searchRecord(field_name, value, num_of_elems=1)
    else:  # "5"
        name = phonebook.checker_name(phonebook.validate_name(input("Введите имя: ").strip().capitalize()))
        if not name: return
        surname = phonebook.checker_name(phonebook.validate_name(input("Введите фамилию: ").strip().capitalize()))
        if not surname: return

        results = phonebook.searchRecord(name, surname, num_of_elems=2)
    if results != []:
        print("\nНайденные записи:")
        phonebook.printSomeRecords(results)
    else:
        print("\nНайденные записи: отсутствуют")


#4
def deleteRecord(phonebook):
    """Logic of 4step in main menu. Check and delete record in phonebook"""
    name = phonebook.checker_name(phonebook.validate_name(input("Введите имя: ").strip().capitalize()))
    if not name: return
    surname = phonebook.checker_name(phonebook.validate_name(input("Введите фамилию: ").strip().capitalize()))
    if not surname: return
    # check if record is in phonebook
    results = phonebook.searchRecord(name, surname, num_of_elems=2)

    if results != []:
        phonebook.deleteRecord(name, surname)
        print("Запись успешно удалена.")
    else:
        print("Такой записи не существует.")

#5
def editRecord(phonebook):
    """Logic of 5step in main menu. Edit record in phonebook"""
    name = phonebook.checker_name(phonebook.validate_name(input("Введите имя: ").strip().capitalize()))
    if not name: return
    surname = phonebook.checker_name(phonebook.validate_name(input("Введите фамилию: ").strip().capitalize()))
    if not surname: return
    results = phonebook.searchRecord(name, surname, num_of_elems=2)

    if results != []:
        record = results[0]
        print("Текущая запись:")
        phonebook.printSomeRecords(results)
        print("\nКакое поле вы хотите изменить?")
        print("1. Номер телефона.")
        print("2. Дата рождения.\n")
        field = input(
            "Введите номер поля для изменения (имя и фамилию изменять нельзя тк это уникальный идентификатор): ").strip()
        field_name = (lambda f: {
            "1": "Номер телефона",
            "2": "Дата рождения"
        }.get(f, None))(field)
        if field_name is None: # error
            print("Некорректный ввод данных. Возврат к выбору команды.")
            return
        new_value = input(f"Введите новое значение для {field_name}: ").strip()

        if field_name == "Номер телефона":
            new_value = phonebook.validate_phone(new_value)
            if not new_value: # error
                print("Некорректный номер телефона (он должен начинаться с 8\+7 и быть с нужным количеством символов). Возврат к выбору команды.")
                return
        elif field_name == "Дата рождения":
            new_value = phonebook.validate_date(new_value)
            if not new_value: # error
                print("Некорректный ввод даты (должна быть в формате дд.мм.гггг). Возврат к выбору команды.")
                return
            new_value = new_value.strftime("%d.%m.%Y")

        record[field_name] = new_value
        phonebook.changeRecord(record)
        print("Данные успешно изменены.")
    else:
        print("Такой записи не существует.")

#6
def findAgeRecord (phonebook):
    """Logic of 6step in main menu. Print age of record (from birthdate) in phonebook"""
    name = phonebook.checker_name(phonebook.validate_name(input("Введите имя: ").strip().capitalize()))
    if not name: return
    surname = phonebook.checker_name(phonebook.validate_name(input("Введите фамилию: ").strip().capitalize()))
    if not surname: return
    results = phonebook.searchRecord(name, surname, num_of_elems=2)
    if results == []:
        print("Такой записи в справочнике нет. Возврат к выбору команды.")
        return
    if results[0]["Дата рождения"] != "":
        record = results[0]
        rec_name = record["Имя"]
        rec_surname = record["Фамилия"]
        years = phonebook.calculate_age(record)
        ending = phonebook.writeEnding(int(years))
        print(f"Возраст {rec_surname} {rec_name} : {years} {ending}")
    else:
        print("Дата рождения отсутствует, поэтому невозможно посчитать возраст. Возврат к выбору команды.")
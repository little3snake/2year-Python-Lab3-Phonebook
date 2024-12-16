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
            printList(phonebook)

        elif command == "2":
            # add
            addRecord(phonebook)

        elif command == "3":
            # search
            searchRecord(phonebook)

        elif command == "4":
            # delete
            deleteRecord(phonebook)

        elif command == "5":
            # edit
            editRecord(phonebook)

        elif command == "6":
            # age
            findAgeRecord(phonebook)

        elif command == "7":
            # quit
            break

        else:
            print("Неверная команда. Попробуйте снова.")

if __name__ == "__main__":
    main()

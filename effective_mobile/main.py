import json
import re
from rapidfuzz import fuzz, process


class Contact:
    """класс описывающий контакт"""

    surname: str
    name: str
    patronymic: str
    organization: str
    work_phone: str
    personal_phone: str

    def get_data(self):
        self.surname = input("Введите фамилию: ")
        self.name = input("Введите имя: ")
        self.patronymic = input("Введите отчество: ")
        self.organization = input("Введите название организации: ")
        self.work_phone = self.get_phone_number("Введите новый рабочий телефон: ")
        self.personal_phone = self.get_phone_number("Введите новый личный телефон: ")

    def to_dict(self):
        return {
            "Фамилия": self.surname,
            "Имя": self.name,
            "Отчество": self.patronymic,
            "Название организации": self.organization,
            "Рабочий телефон": self.work_phone,
            "Личный телефон": self.personal_phone,
        }

    @staticmethod
    def check_phone_number(number: str) -> bool:
        """Функция проверки номера телефона

        Args:
            number (str): введенный номер телефона

        Returns:
            bool: True | False
        """
        pattern = r"^\+?[\d-]+(?:\([\d-]+\))?$"
        if re.match(pattern, number):
            return True
        else:
            print("Номере должен быть в формате +7-333-333-4444")
        return False

    def get_phone_number(self, phone_type: str) -> str:
        """Функция предлагающая повторно ввести номер если он введен не верно

        Args:
            phone_type (str): наименование требуемого телефона

        Returns:
            str: номер телефона, соответствующий требованиям 10 цифр, дефисы, пробелы или скобки
        """
        check_num: bool = True
        while check_num:
            phone_num: str = input(f"{phone_type}")
            check_num = not self.check_phone_number(phone_num)
            if phone_num == "q":
                return None
        return phone_num


class PhoneBook:
    """класс описывающий телефонную книгу"""

    def __init__(self, filename: str):
        self.filename = filename
        self.phonebook = self.load_phonebook()

    def load_phonebook(self):
        """Загрузка данных телефонной книги с диска

        Args:
            filename (str): имя файла с данными

        Returns:
            list[dict]: телефонная книга
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                phonebook = json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден")
            phonebook = []
        return phonebook

    def save_phonebook(self):
        """Запись файла на диск"""
        print(self.phonebook)
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.phonebook, file, indent=4, ensure_ascii=False)

    def add_contact(self, contact: Contact):
        """Добавление записи в телефонную книгу

        Args:
            contact (Contact): данные нового контакта
        """
        self.phonebook.append(contact)
        self.save_phonebook()

    def edit_contact(self, index: int, contact: Contact):
        """Обновление данных контакта

        Args:
            index (int): индекс контакта в списке
            contact (dict): новые данные контакта
        """
        try:
            item_index = int(input("Введите индекс записи для редактирования: "))
            self.phonebook[index] = contact
            self.save_phonebook()
        except Exception as err:
            print("Не верный ввод")

    def search_contact(self, query):
        """Поиск записей в телефонном справочнике по одной или нескольким характеристикам,
        с неточным совпадение значений"""
        search_result = []
        for item in self.phonebook:
            i_match = True
            for key, value in query.items():
                result = process.extractOne(
                    key,
                    list(item.keys()),
                    scorer=fuzz.token_set_ratio,
                )
                if result[1] > 40:
                    if fuzz.token_set_ratio(value, item[result[0]]) < 30:
                        i_match = False
                        break
            if i_match:
                print(item)
                search_result.append(item)

        if len(search_result) < 1:
            print("ничего не найдено")

    @staticmethod
    def get_query():
        search_key = input("Введите название поля: ")
        search_value = input("Введите значение: ")
        return {search_key: search_value}

    def print_page(self):
        """Функция печати страницы с заданного номера страницы с заданным количеством записей на странице"""
        try:
            page_num = int(input("Введите номер страницы: "))
            page_size = int(input("Введите количество записей на странице: "))

            if page_num < 1 or page_size < 0:
                print("Не верный ввод")
                return

            start_index: int = (page_num - 1) * page_size
            end_index: int = start_index + page_size

            for item in self.phonebook[start_index:end_index]:
                print(f"{self.phonebook.index(item)}: {item}")
        except Exception as err:
            print("Не верный ввод")


class MainMenu:
    """класс описывающий главное меню"""

    menu_options = {
        "1": "Постраничный вывод записей.",
        "2": "Добавление новой записи.",
        "3": "Редактирование записи.",
        "4": "Поиск записей.",
        "q": "Выход",
    }

    def display_menu(self):
        """Функция отображения меню"""
        print("\nТелефонный справочник")
        print("=" * 20)
        for key, value in self.menu_options.items():
            print(f"{key}. {value}")
        print("-" * 20)


def main_menu() -> None:
    phonebook_file = "phonebook.txt"
    menu = MainMenu()
    phone_book = PhoneBook(phonebook_file)

    while True:
        phone_book.load_phonebook()
        menu.display_menu()

        choice = input("Выберите действие: ")

        match choice:
            case "1":
                phone_book.print_page()

            case "2":
                new_contact = Contact()
                new_contact.get_data()
                phone_book.add_contact(new_contact.to_dict())

            case "3":
                item_index = int(input("Введите индекс записи для редактирования: "))
                update_contact = Contact()
                update_contact.get_data()
                phone_book.edit_contact(item_index, update_contact.to_dict())

            case "4":
                query = phone_book.get_query()
                phone_book.search_contact(query)

            case "q":
                break

            case _:
                print("не верный ввод")


if __name__ == "__main__":
    main_menu()

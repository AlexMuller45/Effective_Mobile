import json
import re
from rapidfuzz import fuzz, process


def save_phonebook(
    phonebook: list[dict],
    filename: str,
) -> None:
    """Запись файла на диск

    Args:
        phonebook (list[dict]): телефонная книга
        filename (str): имя файла с данными
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(phonebook, file, indent=4, ensure_ascii=False)


def load_phonebook(filename: str) -> list[dict]:
    """Загрузка данных с диска

    Args:
        filename (str): имя файла с данными

    Returns:
        list[dict]: телефонная книга
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            phonebook = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        phonebook = []

    return phonebook


def add_contact(
    phonebook: list[dict],
    contact: dict,
) -> None:
    """Добавление записи в телефонную книгу

    Args:
        phonebook (list[dict]): телефонная книга
        contact (dict): данные нового контакта
    """
    phonebook.append(contact)


def edit_contact(
    phonebook: list[dict],
    index: int,
    contact: dict,
) -> None:
    """Обновление данных контакта

    Args:
        phonebook (list[dict]): телефонная книга
        index (int): индекс контакта в списке
        contact (dict): новые данные контакта
    """
    phonebook[index] = contact


def search_contact(
    phonebook: list[dict],
    **kwarg,
) -> list[dict]:
    """Поиск записей в телефонном справочнике по одной или нескольким характеристикам, с неточным совпадение значений

    Args:
        phonebook (list[dict]): _description_

    Returns:
        list[dict]: _description_
    """
    search_result = []
    for item in phonebook:
        i_match = True
        for key, value in kwarg.items():
            result = process.extractOne(
                key,
                list(item.keys()),
                scorer=fuzz.token_set_ratio,
            )
            if result[1] > 50:
                if fuzz.token_set_ratio(value, item[result[0]]) < 50:
                    i_match = False
                    break
        if i_match:
            search_result.append(item)

    return search_result


def print_page(phonebook: list[dict], page_num: int, page_size: int) -> None:
    """Функция печати страницы с заданного номера страницы с заданным количеством записей на странице

    Args:
        phonebook (list[dict]): телефонная книга
        page_num (int): номер страницы
        page_size (int): количество записей на странице
    """
    if page_num < 1 or page_size < 0:
        print("Не верный ввод")
        return

    start_index: int = (page_num - 1) * page_size
    end_index: int = start_index + page_size

    for item in phonebook[start_index:end_index]:
        print(f"{phonebook.index(item)}: {item}")


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


def get_phone_number(phone_type: str) -> str:
    """Функция предлагающая повторно ввести номер если он введен не верно

    Args:
        phone_type (str): наименование требуемого телефона

    Returns:
        str: номер телефона, соответствующий требованиям 10 цифр, дефисы, пробелы или скобки
    """
    check_num: bool = True
    while check_num:
        phone_num: str = input(f"{phone_type}")
        check_num = not check_phone_number(phone_num)
        if phone_num == "q":
            return None

    return phone_num


def main() -> None:
    """
    Главное меню
    """
    phonebook_file = "phonebook.txt"
    phonebook = load_phonebook(phonebook_file)

    while True:
        print("Телефонный справочник")
        print("=" * 20)
        print(
            "1. Постраничный вывод записей.\n"
            "2. Добавление новой записи.\n"
            "3. редактирование записи.\n"
            "4. Поиск записей.\n"
            "q. Выход\n"
        )
        choice = input("Выберите действие: ")

        match choice:
            case "1":
                page_num = int(input("Введите номер страницы: "))
                page_size = int(input("Введите количество записей на странице: "))
                print_page(
                    phonebook=phonebook,
                    page_num=page_num,
                    page_size=page_size,
                )

            case "2":
                new_contact = {
                    "Фамилия": input("Введите фамилию: "),
                    "Имя": input("Введите имя: "),
                    "Отчество": input("Введите отчество: "),
                    "Название организации": input("Введите название организации: "),
                }
                new_contact["Рабочий телефон"] = get_phone_number(
                    "Введите новый рабочий телефон: "
                )
                new_contact["Личный телефон"] = get_phone_number(
                    "Введите новый личный телефон: "
                )

                add_contact(
                    phonebook=phonebook,
                    contact=new_contact,
                )

                save_phonebook(
                    phonebook=phonebook,
                    filename=phonebook_file,
                )

            case "3":
                item_index = int(input("Введите индекс записи для редактирования: "))
                new_contact = {
                    "Фамилия": input("Введите новую фамилию: "),
                    "Имя": input("Введите новое имя: "),
                    "Отчество": input("Введите новое отчество: "),
                    "Название организации": input(
                        "Введите новое название организации: "
                    ),
                }
                new_contact["Рабочий телефон"] = get_phone_number(
                    "Введите новый рабочий телефон: "
                )
                new_contact["Личный телефон"] = get_phone_number(
                    "Введите новый личный телефон: "
                )

                edit_contact(
                    phonebook=phonebook,
                    index=item_index,
                    contact=new_contact,
                )
                save_phonebook(
                    phonebook=phonebook,
                    filename=phonebook_file,
                )

            case "4":
                search_criteria = {}
                search_key = input("Введите название поля: ")
                search_value = input("Введите значение: ")
                search_criteria[search_key] = search_value
                result = search_contact(phonebook=phonebook, **search_criteria)

                for item in result:
                    print(item)

            case "q":
                break

            case _:
                print("не верный ввод")


if __name__ == "__main__":
    main()

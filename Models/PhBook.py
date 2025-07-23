import json

from dataclasses import dataclass
from typing import Optional
from View import text, press_enter


# Определение класса Contact, представляет один контакт
@dataclass
class Contact:
    """
    Класс абонента телефонной книги.

    name (str): Имя абонента.
    phone (Optional[str]): Номер телефона (необязательный).
    address (Optional[str]): Адрес абонента (необязательный).
    """
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None


    def to_dict(self) -> dict:
        """Преобразует объект Contact в словарь для JSON

        :return: -> Dict
        """
        return {
            "name": self.name,
            "phone": self.phone,
            "address": self.address
        }


    def to_tuple(self) -> tuple:
        """
        Преобразует объект Contact в список для поиска значений

        :return: -> tuple
        """
        return (self.name, self.phone, self.address)


    @classmethod
    def from_dict(cls, data: dict) -> object:
        """Создаёт объект Contact из словаря

        :param data: Словарь с данными контакта
        :return: Объект Contact
        :rtype: Contact
        """
        return cls(
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address")
        )


    def __str__(self) -> str:
        """Возвращает строковое представление контакта

        :return: Строковое представление контакта
        :rtype: str
        """
        return f'{text.name}:\t\t\t{self.name}\n{text.phone}:\t{self.phone}\n{text.address}:\t\t\t{self.address}'



class PhoneBook:
    """Класс телефонной книги формата .json"""
    def __init__(self) -> None:
        """Инициализация класса

        :return: -> None
        """
        self._filename = ""
        # Телефонная книга в виде списка
        self._ph_book = []


    def clear_all(self) -> None:
        """Удаление всех записей из телефонной книги

        :return: None
        """
        self._ph_book.clear()


    def set_filename(self, filename: str) -> None:
        """Сеттер имени файла телефонной книги

        :param filename: Имя файла телефонной книги
        :type filename: str
        :return: -> None
        """
        self._filename = filename


    def get_filename(self) -> str:
        """Геттер имени файла телефонной книги с которой работаем

        :return: имя файла телефонной книги с которой работаем
        :rtype: str
        """
        return self._filename


    def get_size(self) -> int:
        """Геттер числа контактов в телефонной книге

        :return: число контактов в телефонной книге
        :rtype: int
        """
        return len(self._ph_book)


    def get_contact(self, idx: int) -> (Contact, None):
        """Геттер записи из телефонной книги

        :param idx: индекс записи в телефонной книге
        :type idx: int

        :return: словарь с записью
        :rtype: (Contact, None)
        """
        if 0 <= idx <= len(self._ph_book):
            return self._ph_book[idx]
        else:
            return None


    def del_contact(self, idx: int) -> None:
        """Удаляет запись из телефонной книги

        :param idx: индекс удаляемой записи в телефонной книге
        :type idx: int
        :return: -> None
        """
        if 0 <= idx <= len(self._ph_book):
            del self._ph_book[idx]


    def set_contact(self, idx: int, contact: Contact) -> None:
        """Записывает по существующему ID данные контакта

        :param idx:
        :type idx: int
        :param contact:
        :type contact: {}
        :return: -> None
        """
        if idx < self.get_size():
            self._ph_book[idx] = contact


    def open(self) -> None:
        """Открываем файл телефонной книги и читаем его

        :return: -> None
        """
        try:
            with open(self._filename, 'r', encoding='utf-8') as ph_book_file:
                # self._ph_book = json.load(ph_book_file)
                data = json.load(ph_book_file)
                self._ph_book = [Contact.from_dict(contact_data) for contact_data in data]
        except OSError as err:
            print(f"{text.file_open_error} {err}")
            press_enter()
        except json.JSONDecodeError as err:
            print(f"{text.json_data_error} {err}")
            press_enter()


    def save(self) -> None:
        """Сохраняем телефонную книгу в формате json

        :return: -> None
        """
        try:
            #data = [contact.to_dict() for contact in self._ph_book]
            #with open(self._filename, 'w', encoding='utf-8') as ph_book_file:
            #    json.dump(self._ph_book, ph_book_file, indent=4, ensure_ascii=False)
            with open(self._filename, 'w', encoding='utf-8') as ph_book_file:
                json.dump([c.__dict__ for c in self._ph_book], ph_book_file, indent=4, ensure_ascii=False)
        except OSError as err:
            print(f"{text.file_save_error} {err}")
            press_enter()


    def add(self, contact: Contact) -> None:
        """Добавление нового контакта в телефонную книгу

        :param contact: словарь с новым контактом
        :type contact: Contact
        :return: -> None
        """
        self._ph_book.append(contact)


    def search(self, search_str: str) -> [int]:
        """Поиск в записях по строке по всем полям телефонной книги

        :param search_str: строка для поиска
        :type search_str: str

        :return: список индексов контактов, где найдено совпадение
        :rtype: [int]
        """
        # Список индексов записи с результатами поиска
        contacts = []

        if len(search_str):
            # Строка для поиска не пустая
            for idx, contact in enumerate(self._ph_book):
                # Перебираем все контакты в телефонной книге
                for i, element in enumerate(contact.to_tuple()):
                    # Ищем совпадение строки поиска во всех элементах записи
                    if element.find(search_str) >= 0:
                        # Найдено совпадение, добавим в список индекс
                        contacts.append(idx)
                        break

        return contacts

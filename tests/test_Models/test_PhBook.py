from Models import PhoneBook, Contact
from unittest import TestCase

# import json
#
# from dataclasses import dataclass
# from typing import Optional
# from View import text, press_enter


# Определение класса Contact, представляет один контакт
# @dataclass
# class Contact:
#     """
#     Класс абонента телефонной книги.
#
#     name (str): Имя абонента.
#     phone (Optional[str]): Номер телефона (необязательный).
#     address (Optional[str]): Адрес абонента (необязательный).
#     """
#     name: str
#     phone: Optional[str] = None
#     address: Optional[str] = None
#
#
#     def to_dict(self) -> dict:
#         """Преобразует объект Contact в словарь для JSON
#
#         :return: -> Dict
#         """
#         return {
#             "name": self.name,
#             "phone": self.phone,
#             "address": self.address
#         }
#
#
#     def to_tuple(self) -> tuple:
#         """
#         Преобразует объект Contact в список для поиска значений
#
#         :return: -> tuple
#         """
#         return (self.name, self.phone, self.address)
#
#
#     @classmethod
#     def from_dict(cls, data: dict) -> object:
#         """Создаёт объект Contact из словаря
#
#         :param data: Словарь с данными контакта
#         :return: Объект Contact
#         :rtype: Contact
#         """
#         return cls(
#             name=data.get("name"),
#             phone=data.get("phone"),
#             address=data.get("address")
#         )
#
#
#     def __str__(self) -> str:
#         """Возвращает строковое представление контакта
#
#         :return: Строковое представление контакта
#         :rtype: str
#         """
#         return f'{text.name}:\t\t\t{self.name}\n{text.phone}:\t{self.phone}\n{text.address}:\t\t\t{self.address}'



class PhoneBookTestCase(TestCase):
    """
    Тест класса телефонной книги
    """
    def setUp(self):
        """
        Заполнение телефонной книги данными
        :return: None
        """
        self.book = PhoneBook()
        self.book.add_contact(
            Contact('Иванов Иван Иванович', 'г. Иваново, ул. Ивановская, д. 1, кв. 11', '+7(111)-111-11-11'))
        self.book.add_contact(
            Contact('Петров Пётр Петрович', 'г. Санкт-Петербург, ул. Петроградская, д. 2, кв. 22', '+7(222)-222-22-22'))
        self.book.add_contact(
            Contact('Сидоров Сидор Сидорович', 'Московская область, деревня Сидорово, . дом 33', '+7(333)-333-33-33'))
        self.book.add_contact(Contact('Семёнов Семён Семёнович', 'г. Семёнов, ул. Большая Семёновская, д. 4, кв. 44',
                                      '+7(444)-444-44-44'))


    def tearDown(self):
        """
        Очистка телефонной книги
        """
        self.book.clear_all()


    # def clear_all(self):
    #     """
    #     Удаление всех записей из телефонной книги
    #     """
    #     self._ph_book.clear()


    def test_set_filename(self):
        """
        Проверка установки имени файла телефонной книги
        """
        self.assertEqual(self.book._filename, "",
                         f'Проверка инициализации имени файла. Имя файла: "{self.book._filename}", ожидалось ""')

        self.book.set_filename('test.json')
        self.assertEqual(self.book.get_filename(), 'test.json',
                         f'Проверка установки имени файла. Имя файла: "{self.book._filename}", ожидалось "test.json"')


    def test_get_size(self):
        """
        Тест геттера числа контактов, записи в книгу, удаление из книги и очистки в телефонной книги.
        """
        self.assertEqual(self.book.get_size(), 4,
                         f'Проверка количества записей в телефонной книге. Число записей: {self.book.get_size()}, ожидалось: 4')
        self.book.add_contact(Contact("Урицкий Моисей Соломонович", "г. Ветлуга, ул. Урицкого, дом 31", ""))
        self.assertEqual(self.book.get_size(), 5,
                         f'Проверка количества записей в телефонной книге после добавления. Число записей: {self.book.get_size()}, ожидалось: 5')
        self.book.del_contact(4)
        self.assertEqual(self.book.get_size(), 4,
                         f'Проверка количества записей в телефонной книге после удаления. Число записей: {self.book.get_size()}, ожидалось: 4')
        self.book.clear_all()
        self.assertEqual(self.book.get_size(), 0,
                         f'Проверка количества записей в телефонной книге после очистки. Число записей: {self.book.get_size()}, ожидалось: 0')


    def test_get_contact(self):
        """
        Тест геттера записи из телефонной книги
        """
        self.assertEqual(self.book.get_contact(0),
                         Contact('Иванов Иван Иванович', 'г. Иваново, ул. Ивановская, д. 1, кв. 11',
                                 '+7(111)-111-11-11'),f'Ошибка получения контакта из телефонной книги.')
        self.assertEqual(self.book.get_contact(3),
                         Contact('Семёнов Семён Семёнович', 'г. Семёнов, ул. Большая Семёновская, д. 4, кв. 44',
                                  '+7(444)-444-44-44'),f'Ошибка получения контакта из телефонной книги.')
        self.assertEqual(self.book.get_contact(4),None,
                         f'Ошибка получения несуществующего контакта из телефонной книги.')
        self.book.clear_all()
        self.assertEqual(self.book.get_contact(0), None,
                         f'Ошибка получения контакта из пустой телефонной книги.')


    def test_set_contact(self):
        """
        Проверка записи по существующему ID данных контакта
        """
        self.book.set_contact(2, Contact("Жданов Андрей Александрович", "Московская область, деревня Ждановское, дом 81"))
        self.assertEqual(self.book.get_contact(2),
                         Contact("Жданов Андрей Александрович", "Московская область, деревня Ждановское, дом 81"),
                         f'Ошибка замены контакта в телефонной книге.')
        self.book.set_contact(4, Contact("Жданов Андрей Александрович", "Московская область, деревня Ждановское, дом 81"))
        self.assertEqual(self.book.get_contact(4),None,f'Ошибка замены контакта в телефонной книге.')


    # def open(self) -> None:
    #     """Открываем файл телефонной книги и читаем его
    #
    #     :return: -> None
    #     """
    #     try:
    #         with open(self._filename, 'r', encoding='utf-8') as ph_book_file:
    #             # self._ph_book = json.load(ph_book_file)
    #             data = json.load(ph_book_file)
    #             self._ph_book = [Contact.from_dict(contact_data) for contact_data in data]
    #     except OSError as err:
    #         print(f"{text.file_open_error} {err}")
    #         press_enter()
    #     except json.JSONDecodeError as err:
    #         print(f"{text.json_data_error} {err}")
    #         press_enter()
    #
    #
    # def save(self) -> None:
    #     """Сохраняем телефонную книгу в формате json
    #
    #     :return: -> None
    #     """
    #     try:
    #         #data = [contact.to_dict() for contact in self._ph_book]
    #         #with open(self._filename, 'w', encoding='utf-8') as ph_book_file:
    #         #    json.dump(self._ph_book, ph_book_file, indent=4, ensure_ascii=False)
    #         with open(self._filename, 'w', encoding='utf-8') as ph_book_file:
    #             json.dump([c.__dict__ for c in self._ph_book], ph_book_file, indent=4, ensure_ascii=False)
    #     except OSError as err:
    #         print(f"{text.file_save_error} {err}")
    #         press_enter()
    #
    #
    # def add(self, contact: Contact) -> None:
    #     """Добавление нового контакта в телефонную книгу
    #
    #     :param contact: словарь с новым контактом
    #     :type contact: Contact
    #     :return: -> None
    #     """
    #     self._ph_book.append(contact)
    #
    #
    # def search(self, search_str: str) -> [int]:
    #     """Поиск в записях по строке по всем полям телефонной книги
    #
    #     :param search_str: строка для поиска
    #     :type search_str: str
    #
    #     :return: список индексов контактов, где найдено совпадение
    #     :rtype: [int]
    #     """
    #     # Список индексов записи с результатами поиска
    #     contacts = []
    #
    #     if len(search_str):
    #         # Строка для поиска не пустая
    #         for idx, contact in enumerate(self._ph_book):
    #             # Перебираем все контакты в телефонной книге
    #             for i, element in enumerate(contact.to_tuple()):
    #                 # Ищем совпадение строки поиска во всех элементах записи
    #                 if element.find(search_str) >= 0:
    #                     # Найдено совпадение, добавим в список индекс
    #                     contacts.append(idx)
    #                     break
    #
    #     return contacts

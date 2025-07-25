from Models import PhoneBook, Contact
from unittest import TestCase
from unittest.mock import mock_open, patch
import json as json_lib


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
            Contact('Иванов Иван Иванович', '+7(111)-111-11-11', 'г. Иваново, ул. Ивановская, д. 1, кв. 11'))
        self.book.add_contact(
            Contact('Петров Пётр Петрович', '+7(222)-222-22-22', 'г. Санкт-Петербург, ул. Петроградская, д. 2, кв. 22'))
        self.book.add_contact(
            Contact('Сидоров Сидор Сидорович', '+7(333)-333-33-33', 'Московская область, деревня Сидорово, . дом 33'))
        self.book.add_contact(
            Contact('Семёнов Семён Семёнович', '+7(444)-444-44-44', 'г. Семёнов, ул. Большая Семёновская, д. 4, кв. 44'))


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
        self.assertEqual(self.book.get_filename(), "",
                         f'Проверка инициализации имени файла. Имя файла: "{self.book.get_filename()}", ожидалось ""')

        self.book.set_filename('test.json')
        self.assertEqual(self.book.get_filename(), 'test.json',
                         f'Проверка установки имени файла. Имя файла: "{self.book.get_filename()}", ожидалось "test.json"')


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
                         Contact('Иванов Иван Иванович', '+7(111)-111-11-11', 'г. Иваново, ул. Ивановская, д. 1, кв. 11'),
                         f'Ошибка получения контакта из телефонной книги.')
        self.assertEqual(self.book.get_contact(3),
                         Contact('Семёнов Семён Семёнович', '+7(444)-444-44-44', 'г. Семёнов, ул. Большая Семёновская, д. 4, кв. 44'),
                         f'Ошибка получения контакта из телефонной книги.')
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
        self.assertEqual(self.book.get_contact(4),None,f'Ошибка замены несуществующего контакта в телефонной книге.')

    test_data = '[' + \
        '{ "name": "Иванов Иван Иванович", "phone": "+7(111)222-33-44", "address": "Москва, ул. Строителей, дом 1, кв. 15" },' + \
        '{ "name": "Петров Пётр Петрович", "phone": "+7(999)212-46-46", "address": "Москва, ул. Строителей, дом 3, кв. 1" },' + \
        '{ "name": "Егоров Егор Сергеевич", "phone": "+7(555)722-63-77", "address": "Москва, ул. Строителей, дом 5, кв. 789" }' +\
    ']'

    @patch("builtins.open", new_callable=mock_open, read_data=test_data)
    def test_load(self, mock_file):
        """
        Тестирование открытия файла телефонной книги
        """
        # Вызываем метод загрузки файла "test.json"
        self.book.set_filename("test.json")
        self.book.load()
        # Проверяем, что open был вызван с нужными аргументами
        mock_file.assert_called_once_with("test.json", "r", encoding='utf-8')
        # Проверяем, что контакты загрузились правильно
        self.assertEqual(self.book.get_size(), 3,
                         f'Несовпадение числа загруженных контактов. Загружено {self.book.get_size()}, ожидалось 3.')
        self.assertEqual(self.book.get_contact(0),
                         Contact("Иванов Иван Иванович", "+7(111)222-33-44", "Москва, ул. Строителей, дом 1, кв. 15"),
                         'Ошибка сравнения загруженного контакта.')
        self.assertEqual(self.book.get_contact(1),
                         Contact("Петров Пётр Петрович", "+7(999)212-46-46", "Москва, ул. Строителей, дом 3, кв. 1"),
                         'Ошибка сравнения загруженного контакта.')
        self.assertEqual(self.book.get_contact(2),
                         Contact("Егоров Егор Сергеевич", "+7(555)722-63-77", "Москва, ул. Строителей, дом 5, кв. 789"),
                         'Ошибка сравнения загруженного контакта.')


    @patch("builtins.open", new_callable=mock_open)
    def test_save(self, mock_file):
        """
        Тест метода сохранения телефонной книги
        """
        # Вызываем метод сохранения телефонной книги
        self.book.set_filename("test.json")
        self.book.save()

        # Проверяем, что open был вызван с нужными аргументами
        mock_file.assert_called_once_with("test.json", 'w', encoding='utf-8')

        # Получаем, что было записано в файл
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)

        # Проверяем, что записанные данные — это JSON с нужными полями
        expected_data = '[' + \
            '{"name": "Иванов Иван Иванович", "phone": "+7(111)-111-11-11", "address": "г. Иваново, ул. Ивановская, д. 1, кв. 11"},' + \
            '{"name": "Петров Пётр Петрович", "phone": "+7(222)-222-22-22", "address": "г. Санкт-Петербург, ул. Петроградская, д. 2, кв. 22"},' + \
            '{"name": "Сидоров Сидор Сидорович", "phone": "+7(333)-333-33-33", "address": "Московская область, деревня Сидорово, . дом 33"},' + \
            '{"name": "Семёнов Семён Семёнович", "phone": "+7(444)-444-44-44", "address": "г. Семёнов, ул. Большая Семёновская, д. 4, кв. 44"}' + \
        ']'
        #import json as json_lib

        actual_data_list = json_lib.loads(written_data)
        expected_data_list = json_lib.loads(expected_data)

        self.assertEqual(actual_data_list, expected_data_list, 'Ошибка сравнения сохранения содержимого телефонной книги в файл.')

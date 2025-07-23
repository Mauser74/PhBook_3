from os import system, name
from View import text


def clearscreen() -> None:
    """Очистка экрана в консоли в зависимости от операционной системы

    :return: -> None
    """
    if name == 'nt':                    # Для windows
        _ = system('cls')
    else:                               # Для mac и linux
        _ = system('clear')


def print_caption(menu: (), f_pointer) -> None:
    """Получив указатель на функцию и список с пунктами меню печатает название меню относящегося к этой функции как заголовок

    :param menu:
    :param f_pointer: указатель на функцию
    :return: -> None
    """
    caption = menu[menu.index(f_pointer) - 1]
    print(f'{caption}\n' + '-' * len(caption))


def press_enter() -> None:
    """Ожидание нажатия на клавишу Enter

    :return: None
    """
    input(f'{text.press_enter}')

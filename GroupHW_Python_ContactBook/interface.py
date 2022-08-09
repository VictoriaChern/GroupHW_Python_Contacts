import os
# TODO: импортировать контролер когда он будет готов
# import controller

def open_contacts(menu: dict):
    clear()
    # TODO: Открыть и распечатать справочник с помощью модуля controller
    print('Здесь будет список контактов из справочника')
    open_menu(menu, False)

def add_contact():
    clear()
    first_name = input('\33[96mИмя:\33[0m ')
    last_name = input('\33[96mФамилия:\33[0m ')
    father_name = input('\33[96mОтчество:\33[0m ')
    phone_number = input('\33[96mНомер телефона:\33[0m ')
    description = input('\33[96mКомментарий:\33[0m ')
    # TODO: Запустить сохранение контакта с помощью модуля controller
    open_contacts(open_contacts_menu)

def delete_contact():
    input('Введите id контакта: ')
    # TODO: Дать возможность удалить контакт
    open_contacts(open_contacts_menu)

def find_by_name():
    clear()
    # TODO: Запустить поиск по ФИО с помощью модуля controller
    print('Здесь будет поиск контактов по ФИО')
    open_menu(search_menu, False)

def find_by_phone():
    clear()
    # TODO: Запустить поиск по номеру телефона с помощью модуля controller
    print('Здесь будет поиск контактов по номеру телефона')
    open_menu(search_menu, False)    

def export_csv():
    clear()
    # TODO: Запуск экспорта с помощью модуля controller
    print('Здесь будет экспорт контактов в формате csv')
    open_menu(export_menu, False)

def export_txt():
    clear()
    # TODO: Запуск экспорта с помощью модуля controller
    print('Здесь будет экспорт контактов в формате txt')
    open_menu(export_menu, False)

def export_json():
    clear()
    # TODO: Запуск экспорта с помощью модуля controller
    print('Здесь будет экспорт контактов в формате json')
    open_menu(export_menu, False)

def import_csv():
    clear()
    # TODO: Запуск испорта с помощью модуля controller
    print('Здесь будет импорт контактов в формате csv')
    open_menu(import_menu, False)

def import_txt():
    clear()
    # TODO: Запуск испорта с помощью модуля controller
    print('Здесь будет импорт контактов в формате txt')
    open_menu(import_menu, False)

def import_json():
    clear()
    # TODO: Запуск испорта с помощью модуля controller
    print('Здесь будет импорт контактов в формате json')
    open_menu(import_menu, False)

def open_menu(menu: dict, is_clear: bool = True):
    if(is_clear):
        clear()
    enum_menu = list(enumerate(menu.keys(), 1))
    print_menu(enum_menu)
    choice = input('\33[93mВведите пункт меню: ')
    print('\33[0m', end='')
    for (i,v) in enum_menu:
        if(choice == str(i)):
            action = menu.get(v)
            if(action == None):
                return
            action()

def print_menu(enum_menu: enumerate):
    for i, v in enum_menu:
        print(f'\33[96m{i}:\33[0m \33[92m{v}\33[0m')

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

open_contacts_menu = {
    'Добавить новый контакт' : lambda: add_contact(),
    'Удалить контакт': lambda: delete_contact(),
    'Назад' : lambda: open_menu(main_menu),
}
search_menu = {
    'По ФИО' : lambda: find_by_name(),
    'По номеру телефона' : lambda: find_by_phone(),
    'Назад' : lambda: open_menu(main_menu),
}
export_menu = {
    'csv': lambda: export_csv(),
    'txt': lambda: export_txt(),
    'json': lambda: export_json(),
    'Назад': lambda: open_menu(main_menu)
}
import_menu = {
    'csv': lambda: import_csv(),
    'txt': lambda: import_txt(),
    'json': lambda: import_json(),
    'Назад': lambda: open_menu(main_menu)
}
main_menu = {
    'Открыть' : lambda: open_contacts(open_contacts_menu),
    'Поиск' : lambda: open_menu(search_menu),
    'Экспорт' : lambda: open_menu(export_menu),
    'Импорт' : lambda: open_menu(import_menu),
    'Выход' : None
}
open_menu(main_menu)
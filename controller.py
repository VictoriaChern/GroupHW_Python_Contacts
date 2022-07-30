# from statistics import mode
# import  model_mult as model
# import view

# def button_click():
#     value_a = view.get_value()
#     value_b = view.get_value()
#     model.init(value_a, value_b)
#     result = model.do_it()
#     view.view_data(result, "resul")
from pprint import pprint
import export
import import
import interface
import change
filename = "phonebook.json"

formatted_result = pformat(result)
print(formatted_result)

phonebook = load_phonebook(filename) # скачивание телефонной книги
pretty_print(phonebook)


search_res = search_by_name(phonebook, 'введите ФИО контакта') # поиск по ФИО
pretty_print(search_res)
assert len(search_res) == 3

search_res = search_by_phone(phonebook, 'введите номер целиком или часть номера') # поиск по номеру телефона или его части (если не будем делать поиск по части номера, то !!! поменять текст)
pretty_print(search_res)
assert len(search_res) == 2

assert len(search_by_name(phonebook, 'ввдеите ФИО')) == 0
phonebook = add_record(phonebook, 'введите телефон с описанием', [
    {
        'описание': 'мобильный',
        'номер': '+79119222446'
    }
])
assert len(search_by_name(phonebook, 'ФИО')) == 1

phonebook = add_record(phonebook, 'ФИО', [ #добавление
    {
        'описание': 'мобильный',
        'номер': '+79219222446'
    },
    
])
assert len(search_by_name(phonebook, 'ФИО')) == 1

phonebook = replace_record(phonebook, 'ФИО', [ #замена реализую в двух вариантах по ФИО, номеру телефона без описания и типа телефона
    {
        'описание': 'мобильный',
        'номер': '+79219222446'
    },
    
])
assert len(search_by_name(phonebook, 'ФИО')) == 1
assert len(search_by_phone(phonebook, '+79219222446')) == 1

phonebook = remove_phone(phonebook, 'введите номер') # удаление
assert len(search_by_phone(phonebook, '+79119222446')) == 0
assert len(search_by_phone(phonebook, '+79219222446')) == 0

phonebook = remove_name(phonebook, 'ФИО')
assert len(search_by_name(phonebook, 'ФИО')) == 0

pretty_print(phonebook)

save_phonebook(filename, phonebook)




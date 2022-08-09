import csv
import json


'''
import guide_export
далее, для запуска модуля конвертации в csv пишем: 
guide_export.convert_to_csv(<путь к файлу>)
для конвертации в json - guide_export.convert_to_json
'''
#*****************CSV******************************************************************************************   

def convert_to_csv(file_path: str):
    '''
    Принимает путь к txt файлу с данными, построчно считывает файл, 
    после считывания каждой строки вызывается функция конвертации в csv формат.
    '''
    with open(file_path, 'r', encoding='utf-8') as file:
        data = file.read()
        to_csv(data)


def to_csv(text: str):
    '''
    Принимает строки, создает csv файл именуемый phones_csv.csv и записывает в него данные
    '''
    file = open('phones_csv.csv', 'w', encoding='utf-16')
    with file:
        writer = csv.writer(file, dialect = 'excel', delimiter = ' ', quotechar='|')
        writer.writerow(text)
        

 #*****************JSON******************************************************************************************       
        
def convert_to_json(file_path: str):
    '''
    Принимает путь к txt файлу с данными.
    Первая строка преобразовывается в ключи: "фамилия", "имя", "отчество", "телефон", "комментарий"
    Затем считываются остальные строки и в цикле вызывается to_dictionary - формируются словари для приведения данных
    к формату json, после формирования словаря вызывается функция записи в json файл.
    '''
    f = open('phones_json.json', 'w') #предварительная очистка файла json
    f.close()

    with open(file_path, 'r', encoding='utf-8') as file:
        keys = []
        people = []
        keys = file.readline()
        keys = keys.split()


        lines = file.readlines()
        for line in lines:
            line = line.split()
            data = to_dictionary(keys, line)
            people.append(data)
        to_json(people)
      

def to_dictionary(keys: list, lst):
    '''
    Принимает список ключей и список данных, возвращает словарь по типу: "ключ": "данные" для приведения к формату json
    '''
    dict = {}
    #конструкция объединяет строки комментария в одну, иначе, если комментарий больше одного слова записывается только первое
    if len(keys) < len(lst):
        for i in range(6,len(lst)):
            lst[5] += ' ' + lst[i]
    #===================================================================
    for i in range(len(keys)):
        dict[keys[i]] = lst[i]
    return dict



def to_json(text: list):
    '''
    Запись данных в json файл
    '''
    with open('phones_json.json', 'a', encoding = 'utf-8') as file:
        json.dump(text, file, ensure_ascii = False, indent = 1)

convert_to_csv('C:\study\Python\PythonHomeWorks\GroupHW_Python_Contacts\phones.txt') #тестовая строка - убрать
convert_to_json('C:\study\Python\PythonHomeWorks\GroupHW_Python_Contacts\phones.txt') #тестовая строка - убрать

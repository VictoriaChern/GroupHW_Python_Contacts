import csv, json
from functools import reduce

def convert_from_csv(file_path_csv: str, file_path_txt: str):
    '''
    Метод, отвечающий за импорт из формата csv
    file_path_csv - исходный файл для импорта
    file_path_txt - куда импортируем
    '''
    with open(file_path_csv, "r", encoding='utf-16') as data:
        reader = csv.reader(data, dialect = "excel", delimiter = ' ', quotechar = '|')
        with open(file_path_txt, 'w', encoding='utf-16') as file:
            for row in reader:
                temp_str = ""
                if len(row) >= 1:
                    temp_str = str(reduce(lambda x,y: x + y, row))
                file.write(temp_str)
    return ("Успех")

def convert_from_json(file_path_json: str, file_path_txt: str):
    '''
    Метод, отвечающий за импорт из формата json
    file_path_json - исходный файл для импорта
    file_path_txt - куда импортируем
    '''
    with open(file_path_json, 'r', encoding="utf-8") as data:
        list_obj = json.load(data)

    temp_str = ""
    if len(list_obj) > 0:
        temp_str += first_line(list_obj[0])
    temp_str += "\n"

    for item in list_obj:
        for key in item.keys():
            temp_str += item[key] + "\t"
        temp_str += "\n"
    
    with open(file_path_txt, 'w', encoding='utf-8') as file:
        file.write(temp_str)
    return "Успех"

def first_line(dictionary: dict):
    '''
    Метод, создающий первую строку в телефонной книге
    '''
    temp_str = ""
    for i in dictionary.keys():
        temp_str += i + "\t"
    return temp_str

#convert_from_csv("E:\Desktop\Projects\Python\GroupHW_Python_Contacts\phones_csv.csv", 
#"E:\Desktop\Projects\Python\GroupHW_Python_Contacts\\test_phones.txt")

# convert_from_json("E:\Desktop\Projects\Python\GroupHW_Python_Contacts\\test_file.json", 
# "E:\Desktop\Projects\Python\GroupHW_Python_Contacts\\test_phones.txt")

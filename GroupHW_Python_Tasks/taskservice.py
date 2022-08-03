import dbcontroller
from datetime import datetime 

def ask_date():
    '''
    Метод, запрашивающий дату у пользователя
    '''
    date = input('Введите дату (YYYY-MM-DD): ')
    try:
        date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print('Неверный формат даты')
        return ask_date()
    return date

def ask_id():
    '''
    Метод, запрашивающий ID задачи у пользователя
    '''
    id = input('Введите ID: ')
    if(not id.isdigit()):
        print('Ошибка: вы ввели не ID! Повторите ввод')
        return ask_id()
    return int(id)

def find_task_by_id():
    '''
    Метод, отвечающий за поиск задачи по ID
    '''
    id = ask_id()
    task = dbcontroller.find_by_id(id)
    return task

def find_tasks():
    '''
    Метод, отвечающий за поиск задачи по всем колонкам
    '''
    search = input('Введите строку для поиска: ')
    tasks = dbcontroller.find_obj(search)
    return tasks

def create_task():
    '''
    Метод, отвечающий за создание новой задачи
    '''
    description = input('Введите описание задачи: ')
    date = ask_date()
    status = 'to do'
    result = dbcontroller.create_obj([description, date, status])
    print(result)

def update_task_description():
    '''
    Метод, отвечающий за обновление описания задачи
    '''
    task = find_task_by_id()
    if (task == None):
        print('Задача не найдена')
        return
    print(f'Текущее описание задачи: {task[1]}')
    new_description = input('Введите описание задачи: ')
    result = dbcontroller.update_obj(task[0], 'description', new_description)
    print(result)

def update_task_date():
    '''
    Метод, отвечающий за обновление даты задачи
    '''
    task = find_task_by_id()
    if (task == None):
        print('Задача не найдена')
        return
    print(f'Текущее значение даты: {task[2]}')
    new_date = ask_date()
    result = dbcontroller.update_obj(task[0], 'date', new_date)
    print(result)

def delete_task():
    '''
    Метод, отвечающий за удаление задачи
    '''
    id = ask_id()
    result = dbcontroller.delete_obj(id)
    print(result)
 
#create_task()
#tasks = find_tasks()
#print(tasks)
#update_task_date()
#update_task_description()
#task = find_task_by_id()
#print(task)
#delete_task()
#task = find_task_by_id()
#print(task)
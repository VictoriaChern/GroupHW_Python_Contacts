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
    return find_task_by_id(id)

def find_task_by_id(id: int):
    '''
    Метод, отвечающий за поиск задачи по ID
    '''
    return dbcontroller.find_by_id(id)

def find_tasks_cmd():
    '''
    Метод, отвечающий за поиск задачи по всем колонкам
    '''
    search = input('Введите строку для поиска: ')
    return find_tasks(search)

def find_tasks(search: str):
    '''
    Метод, отвечающий за поиск задачи по всем колонкам
    '''
    tasks = dbcontroller.find_obj(search)
    return tasks

def create_task():
    '''
    Метод, отвечающий за создание новой задачи
    '''
    description = input('Введите описание задачи: ')
    date = ask_date()
    result = create_task(description, date)
    print(result)

def create_task(description: str, date):
    '''
    Метод, отвечающий за создание новой задачи
    '''
    status = 'to do'
    return dbcontroller.create_obj([description, date, status])

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
    result = update_task_description(task[0], new_description)
    print(result)

def update_task_description(id: int, new_description: str):
    '''
    Метод, отвечающий за обновление описания задачи
    '''
    return dbcontroller.update_obj(id, 'description', new_description)

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
    result = update_task_date(task[0], new_date)
    print(result)

def update_task_date(id: int, new_date):
    '''
    Метод, отвечающий за обновление даты задачи
    '''
    return dbcontroller.update_obj(id, 'date', new_date)

def delete_task():
    '''
    Метод, отвечающий за удаление задачи
    '''
    id = ask_id()
    result = delete_task(id)
    print(result)

def delete_task(id: int):
    '''
    Метод, отвечающий за удаление задачи
    '''
    return dbcontroller.delete_obj(id)
 
#create_task()
#tasks = find_tasks_cmd()
#print(tasks)
#update_task_date()
#update_task_description()
#task = find_task_by_id()
#print(task)
#delete_task()
#task = find_task_by_id()
#print(task)

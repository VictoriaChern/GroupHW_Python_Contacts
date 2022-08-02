import dbcontroller
import datetime

def ask_date():
    date = input('Введите дату (YYYY-MM-DD): ')
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print('Неверный формат даты')
        return ask_date()
    return date

def ask_id():
    id = input('Введите ID: ')
    if(not id.isdigit()):
        print('Ошибка: вы ввели не ID! Повторите ввод')
        return ask_id()
    return int(id)

def get_task():
    id = ask_id()
    # TODO: использовать специальный метод поиска по ID
    tasks = dbcontroller.find_obj(id)
    task = tasks[0]
    return task

def create_task():
    description = input('Введите описание задачи: ')
    date = ask_date()
    status = 'to do'
    result = dbcontroller.create_obj([description, date, status])
    print(result)

def update_task_description():
    task = get_task()
    print(f'Текущее описание задачи: {task[1]}')
    new_description = input('Введите описание задачи: ')
    result = dbcontroller.update_obj(str(id), 'description', new_description)
    print(result)

def update_task_date():
    task = get_task()
    print(f'Текущее значение даты: {task[2]}')
    new_date = ask_date()
    result = dbcontroller.update_obj(str(id), 'date', new_date)
    print(result)

def delete_task():
    id = ask_id()
    result = dbcontroller.delete_obj(id)
    print(result)
 


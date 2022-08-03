#Модуль, реализующий взаимодейсвтие с БД
import sqlite3
import turtle

def __init__():
    global conn
    global cur
    conn = sqlite3.connect("dbTasks.db")
    cur = conn.cursor()

def find_obj(search: str) -> list:
    '''
    Метод, отвечающий за поиск по всем столбцам
    search - текст/дата, по которой ищем
    '''
    cur.execute(f"select * from Tasks where id like '%{search}%'\
        or description like '%{search}%'\
        or date like '%{search}%'\
        or status like '%{search}%'")
    result = cur.fetchall()
    return result

def find_by_id(id) -> tuple:
    '''
    Метод, отвечающий за поиск по id
    id - айди записи
    '''
    cur.execute(f"select * from Tasks where id == {id}")
    result = cur.fetchone()
    return result

def create_obj(data: list):
    '''
    Метод, создающий "задачу"
    data - список [Описание задачи, дата, статус]
    '''
    cur.execute(f"""insert into tasks (description, date, status) values\
        (?,?,?)""", (data[0],data[1],data[2]))
    conn.commit()
    return "Запись создана"

def update_obj(id, column, data):
    '''
    Метод, изменяющий "задачу"
    id - id задачи в БД
    column - изменяемый столбец
    data - новые данные
    '''
    cur.execute(f"""update Tasks set {column} = ? where id == ?""", (data, id))
    conn.commit()
    return "Запись изменена"

def delete_obj(id):
    '''
    Метод, удаляющий задачу
    id - id задачи в БД
    '''
    cur.execute(f"delete from tasks where id == {id}")
    conn.commit()
    return "Запись удалена"

__init__()

print(find_by_id(1))
#print(create_obj(["test", "2022-01-24", "to do"]))
#print(update_obj(1, "description", "test"))
#print(delete_obj(3))
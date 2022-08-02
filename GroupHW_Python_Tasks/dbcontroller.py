#Модуль, реализующий взаимодейсвтие с БД
import sqlite3

def __init__():
    global conn
    global cur
    conn = sqlite3.connect("GroupHW_Python_Tasks\dbTasks.db")
    cur = conn.cursor()

def find_obj(search: str) -> list:
    cur.execute(f"select * from Tasks where id like '%{search}%'\
        or description like '%{search}%'\
        or date like '%{search}%'\
        or status like '%{search}%'")
    result = cur.fetchall()
    return result

def create_obj(data: list):
    cur.execute(f"insert into tasks (description, date, status) values\
        ({data[0]}, {data[1]}, {data[2]})")
    conn.commit()

def update_obj(id, column, data):
    cur.execute(f"update Tasks set {column} = {data} where id == {id}")

def delete_obj(id):
    cur.execute(f"delete from tasks where id == {id}")
    conn.commit()
    return "Запись удалена"

__init__()

find_obj("te")
import datetime
import pandas as pd
import dbcontroller as dbTasks # написано под проект
# jsonarray = [
#     {
#     'name':'print text for TG',
#     'datetime':"2022-08-02 05:00:00",
#     'length':90,
#     'description':'text to TG about antisanctions'
#     },
#     {
#     'name':'call to KPR',
#     'datetime':"2022-08-02 06:00:00",
#     'length':70,
#     'description':'about legalization'
#     },    
#   {
    # 'name':'email',
    # 'datetime':"2022-08-03 06:00:00",
    # 'length':70,
    # 'description':'answer'
    # }      
# ]
# df = pd.DataFrame(jsonarray) # строки с 4 по 24 из изначального кода
df =  pd.DataFrame(dbTasks.db) # написано под проект
df.datetime = pd.to_datetime(df.datetime)
dbcontroller.find_obj() # написано под проект

printformat = """
Task Name: {}
Start time: {}
End time: {}
Description: {}
"""

def print_tasks(maskby):
    mask = df[df['datetime'].dt.date.astype(str) == maskby].sort_values(by='datetime')
    s = ['These are your tasks for {}:\n'.format(maskby)]
    for row in mask.iterrows():
        name = row["name"]
        stime = row["datetime"].strftime("%H:%M")
        etime = (row["datetime"] + datetime.timedelta(minutes=row["length"])).strftime("%H:%M")
        desc = row["description"]
        s.append(printformat.format(name,stime,etime,desc))
    return ''.join(s)

print(print_tasks("2022-08-02")) # !!!! need help, что сюда нужно прописать, чтобы он выводил данные по дате, которую ввел пользователь. 


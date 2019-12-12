# 开发人员：wushiwang
# 开发时间：2019/12/12 20:49
# 文件名称：monitor.py
# 开发工具：PyCharm

import psutil
import sqlite3
import time

db_name='mydb.db'

def create_db():
    conn=sqlite3.connect(db_name)
    c=conn.cursor()

    c.execute('''DROP TABLE IF EXISTS cpu''')
    c.execute('''CREATE TABLE cpu (id INTEGER PRIMARY KEY AUTOINCREMENT, insert_time text,cpu1 float, cpu2 float, cpu3 float, cpu4 float)''')

    conn.close()

def save_to_db(data):
    conn=sqlite3.connect(db_name)
    c=conn.cursor()
    c.execute('INSERT INTO cpu(insert_time,cpu1,cpu2,cpu3,cpu4) VALUES (?,?,?,?,?)', data)
    conn.commit()
    conn.close()

create_db()
while True:
    cpus=psutil.cpu_percent(interval=1, percpu=True)
    t = time.strftime('%M:%S', time.localtime())
    save_to_db((t,*cpus))
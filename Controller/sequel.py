import sqlite3 as sql
import pandas as pd


# connect to database
con = sql.connect("best.db",check_same_thread=False)

# create table


def create():
    con.execute(
        '''CREATE TABLE IF NOT EXISTS clg(Time DATE, Name TEXT, Count INT)''')
    con.commit()

# add data to the table


def Insert(date, text, count):
    con.execute('''INSERT INTO clg VALUES(?,?,?)''',
                 (date, text, count))
    con.commit()


# read contents of the data
def read():
    l1=[]
    pic =con.execute('''SELECT * FROM clg''')
    da = pic.fetchall()
    for i in da:
        l1.append(i)
    df=pd.DataFrame(l1,columns=['date','name','count'])
    return df

def read():
    l2 = []
    count = con.execute(
        '''Select  name,sum(count) from clg group by name''')
    d2 = count.fetchall()
    for i in d2:
        l2.append(i)
    d2 = pd.DataFrame(l2, columns=[" ", "count"])
    return d2


# truncate table


def _delete():
    con.execute('''DELETE FROM ITEMS''')
    con.commit()


if __name__ == '__main__':
    create()

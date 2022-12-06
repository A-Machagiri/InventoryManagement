import streamlit as st
import sqlite3
import os
import pandas as pd
con=sqlite3.connect("data.db",check_same_thread=False)
cur=con.cursor()
def form():
    # with to add elements to object we use "with" notation
    st.write("This is a form")
    # A string that identifies the form. Each form must have its own key. (This key is not displayed to the user in the interface.)
    with st.form(key="information form"):
        date = st.date_input("Enter the date: ")
        name = st.text_input("Enter your name: ")
        count = st.text_input("Enter your count: ")
        submission = st.form_submit_button(label="Submit")
        if submission == True:
            addData(date,name,count)
def addData(a,b,c):
    cur.execute("""CREATE TABLE IF NOT EXISTS clg(Date TEXT(50),Name TEXT(50),count TEXT(60));""")
    cur.execute('INSERT INTO clg VALUES (?,?,?)',(a,b,c))
    con.commit()# changes will be save permanent databases table
    st.success("Show success")
# form()
def data():
    # if (mode=="")
    l=[]
    pic =con.execute('''SELECT * FROM clg''')
    data = pic.fetchall()
    for i in data:
        l.append(i)
    df=pd.DataFrame(l,columns=['time','name','count'])
    return df
def sum():
        l=[]
        count=con.execute('''Select  name,sum(count) from clg group by name''')
        data=count.fetchall()
        for i in data:
            l.append(i)
        data=pd.DataFrame(l,columns=[" ","count"])
        return data
def exce():
    # if (mode=="")
    l=[]
    pic =con.execute('''SELECT * FROM clg''')
    data = pic.fetchall()
    for i in data:
        l.append(i)
    df=pd.DataFrame(l)
    return df

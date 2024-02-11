import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
import os

#? Connect to Sqlite
connection = sqlite3.connect("student.db")

#? Creating a cursor object to insert record, create table, retrieve
cursor = connection.cursor()

#? Creating Table
table_info = """
Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARK INT);
"""
cursor.execute(table_info)

#? Inserting records
cursor.execute('''Insert Into STUDENT values('Vedant','Web Developer', 'A', 95)''')
cursor.execute('''Insert Into STUDENT values('Vanshay','Secondary School', 'A', 85)''')
cursor.execute('''Insert Into STUDENT values('Isha','ML Expert', 'B', 86)''')
cursor.execute('''Insert Into STUDENT values('Krishnal','Web Developer', 'B', 50)''')
cursor.execute('''Insert Into STUDENT values('Shresth','MERN Stack', 'C', 75)''')

#? Display all records
print("The inserted records are: ")
data = cursor.execute('''Select * From Student''')

for row in data:
    print(row)
    
#? Close the connection
connection.commit()
connection.close()


#! Gemini Integration

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt): #! Prompt defines how the particular model should behave like.
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows


prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

st.set_page_config(page_title="I can Retrieve any SQL Query")
st.header("Gemini App to Retrieve SQL Data")

question = st. text_input("Input: ", key="input")
submit = st.button("Ask the Question")

if submit:
    response = get_gemini_response(question, prompt)
    print(response)
    response = read_sql(response, "student.db")
    st.subheader("The Response is: ")
    for row in response:
        print(row)
        st.header
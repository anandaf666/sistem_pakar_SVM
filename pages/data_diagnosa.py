import streamlit as st
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ker_jar"
)

mycursor=mydb.cursor()

st.write("""
         # Diagnosa Gangguan Jaringan Local Area Network SVM
         """)

st.subheader("Data Diagnosa")
mycursor.execute("select * from data_diagnosa")
result = mycursor.fetchall()
for row in result:
    st.write(row)
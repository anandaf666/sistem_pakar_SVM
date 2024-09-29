import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
import pickle
import matplotlib.pyplot as plt
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

st.sidebar.header('Inputan User')
nama = st.sidebar.text_input("Masukkan Nama")
def input_user():
        G1 = st.sidebar.slider('(1.) SSID Wifi menghilang', 0.0, 1.0, 0.0)
        G2 = st.sidebar.slider('(2.) Password berubah', 0.0, 1.0, 0.0)
        G3 = st.sidebar.slider('(3.) SSID Wifi kembali ke setingan awal', 0.0, 1.0, 0.0)
        G4 = st.sidebar.slider('(4.) Loading page lambat saat browsing', 0.0, 1.0, 0.0)
        G5 = st.sidebar.slider('(5.) Indikator LAN card tidak menyala', 0.0, 1.0, 0.0)
        G6 = st.sidebar.slider('(6.) Indikator hub/swich tidak menyala', 0.0, 1.0, 0.0)
        G7 = st.sidebar.slider('(7.) Simbol wifi tanda seru kuning', 0.0, 1.0, 0.0)
        G8 = st.sidebar.slider('(8.) Slot LAN rusak', 0.0, 1.0, 0.0)
        G9 = st.sidebar.slider('(9.) Koneksi internet rendah', 0.0, 1.0, 0.0)
        G10 = st.sidebar.slider('(10.) Koneksi putus tiba-tiba tanpa adanya perubahan oleh admin', 0.0, 1.0, 0.0)
        G11 = st.sidebar.slider('(11.) Koneksi tidak stabil', 0.0, 1.0, 0.0)
        
        data = {
            'G1' : G1,
            'G2' : G2,
            'G3' : G3,
            'G4' : G4,
            'G5' : G5,
            'G6' : G6,
            'G7' : G7,
            'G8' : G8,
            'G9' : G9,
            'G10' : G10,
            'G11' : G11
        }

        fitur = pd.DataFrame(data, index=[0])
        return fitur
inputan = input_user()

kerusakan_raw = pd.read_csv('data_kerusakan.csv')
kerusakan = kerusakan_raw.drop(columns=['Kerusakan'])

df = pd.concat([inputan, kerusakan], axis=0)

df = df[:1]
st.subheader('Parameter Inputan')
st.write(df)

load_model = pickle.load(open('model-kerusakan.pkl', 'rb'))
prediksi = load_model.predict(df)
prediksi_proba = load_model.predict_proba(df)

st.subheader('Keterangan Label Class Kerusakan')

kelas_kerusakan = np.array(['Router Reset', 'Internet Limit', 'Network Cable Unplugged', 'Router/Switch rusak'])
st.write(kelas_kerusakan)

st.subheader('Hasil Diagnosa')
st.write(kelas_kerusakan[prediksi])

st.subheader('Probabilitas Hasil Diagnosa')
st.write(prediksi_proba)
hasl = max(max(prediksi_proba))
st.write(hasl)
nama = nama
G1 = df['G1'].item()
G2 = inputan['G2'].item()
G3 = inputan['G3'].item()
G4 = inputan['G4'].item()
G5 = inputan['G5'].item()
G6 = inputan['G6'].item()
G7 = inputan['G7'].item()
G8 = inputan['G8'].item()
G9 = inputan['G9'].item()
G10 = inputan['G10'].item()
G11 = inputan['G11'].item()
if st.sidebar.button("Create"):
    sql= "insert into data_diagnosa(nama,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,hasl) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val= (nama,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,hasl)
    mycursor.execute(sql,val)
    mydb.commit()
    st.success("Record Created Successfully!!!")
st.subheader('Solusi')
if prediksi==[0]:
    st.write('Restart Router dan pastikan Kabel Jaringan benar terpasang dengan baik')
elif prediksi==[1]:
    st.write('Setting ulang kembali Router ke pengaturan User seperti sebelum ter-reset')
elif prediksi==[2]:
    st.write('Cek Port jaringan sudah terpasang dengan baik dan sesuai urutan. Bersihkan Port jika terdapat kotoran dengan semprotan pembersih alat elektronik')
else:
    st.write('Coba ganti dengan Switch atau Router yang baru dan dalam kondisi baik')



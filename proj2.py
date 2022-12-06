import streamlit as st
import yolov5 as yl
from streamlit_webrtc import webrtc_streamer
import pandas as pd
from form2 import data, sum,exce
from image import imag
from io import BytesIO
from PIL import Image
import numpy as np
def call():
    th=st.sidebar.slider("Confidence threshold",min_value=0.00,max_value=1.00, step=0.15, value=0.65)
def staff():
    st.sidebar.date_input("Date")
    call()
    sel = st.sidebar.radio("View Mode", ["None", "📹video", "📊data", "📷image"])
    if (sel == "📹video"):
        st.title("📹 Objects deletion Model")
        webrtc_streamer(key="example")
    st.checkbox("Store")
    st.checkbox("Show the detected labels")
    if(sel=="📷image"):
        imag()
    if (sel == "📊data"):
        st.title("📊data")
        d = data()
        st.table(d)
        data2 = sum()
        data2.set_index(" ", inplace=True)#If I reset the index of my pandas DataFrame with "inplace=True"it returns a class 'NoneType'.
        st.table(data2)
        mode = st.sidebar.radio("Download Mode", ["None", "Excel", "Csv"])
        if(mode=="Csv"):
            c=exce()
            st.sidebar.download_button ( " Download CSV " ,c.to_csv(),file_name="d1.csv",mime = ' text / csv ' )
        elif(mode=="Excel"):
            c=exce()
            output=BytesIO()#Creating an object of bytes
            with pd.ExcelWriter(output,engine='xlsxwriter') as writer:
                c.to_excel(writer)
            st.sidebar.download_button ( " Download Excel " ,data=output,mime = ' application/vnd.ms-excel ' )
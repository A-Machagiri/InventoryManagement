import streamlit as st
import yolov5 as yl
import av

import sqlite3
from streamlit_webrtc import webrtc_streamer,WebRtcMode,RTCConfiguration
import pandas as pd
from form2 import data, sum,exce
from image import imag
from Controller.sequel import *
from Controller.userController import *
from io import BytesIO
from PIL import Image
import time
import torch
import numpy as np
def model():
    return yl.load("best.pt")
model=model()
class Videoprocessor:
    def __init__(self):
        self.res=None
        self.confidence=0.5

    def getRes(self):
        #time.sleep(5)
        return self.res

    def recv(self, frame):
        model.conf=self.confidence
        frm = frame.to_ndarray(format="bgr24")
        
        # vision processing
        flipped = frm[:, ::-1, :]

        # model processing
        im_pil = Image.fromarray(flipped)
        results = model(im_pil, size=112)
        self.res=results
        bbox_img = np.array(results.render()[0])
        return av.VideoFrame.from_ndarray(bbox_img, format="bgr24")
def staff():
    with st.sidebar:
        date=st.date_input("Date")
        confidence=st.slider("Confidence threshold", min_value=0.00,max_value=1.00, step=0.15, value=0.65)
        sel = st.radio("View Mode", ["None", "📹video", "📊data", "📷image"])
    if (sel == "📹video"):
        st.title("📹 Objects deletion Model")
        webrtc_ctx = webrtc_streamer(
                key="webcam",
                mode=WebRtcMode.SENDRECV,
                
                media_stream_constraints={"video": True, "audio": False},
                video_processor_factory=Videoprocessor,
                async_processing=True,
            )
        if webrtc_ctx.state.playing:
                webrtc_ctx.video_processor.confidence=confidence
        if st.checkbox('Show the detected labels'):
            empty=st.empty()
            store=st.button('Store')
            if webrtc_ctx.state.playing:
                while True:
                    if webrtc_ctx.video_processor:
                        results = webrtc_ctx.video_processor.getRes()
                        if results != None:
                            count = results.pandas().xyxy[0]
                            dj = count["name"].tolist()
                            dj = read_df(dj)

                            empty.table(dj)
                            for idx,row in dj.iterrows():
                                if store:
                                    Insert(date, row["Name"], int(row["Count"]))
                                    time.sleep(3)
                        else:
                            empty.write("No labels detected")
                    else:
                        break
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

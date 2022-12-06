import streamlit as st
import yolov5 as yl
from PIL import Image
# from proj2 import th
import numpy as np
def imag():
    upload = st.sidebar.checkbox("Upload")
    m = yl.load("./best.pt")# Loading the Trained model
    m.conf = 0.65  # Non Maximum Suppresion confidence threshold
    m.iou = 0.45  # NMS IoU threshold ov/ins above 0.5 is considered as good predicted
    m.agnostic = False  # NMS class-agnostic
    m.multi_label = False  # NMS multiple labels per box
    m.max_det = 1000
    if upload:
        image = st.sidebar.file_uploader("Upload an Image", type="jpg")
        if image is not None:
            image = Image.open(image)
            img=image
            image = np.array(image)
            results = m(image)
            results.save(save_dir="output/")
            if st.button('detect'):
                st.image("output/image0.jpg")
            else:
                st.image(img)
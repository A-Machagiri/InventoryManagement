import streamlit as st
from proj2 import staff
st.title("Cold Drinks Inventory Management System")
sl=st.selectbox("Mode",["none","staff"])
if(sl=="staff"):
    st.title("Staff")
    staff()
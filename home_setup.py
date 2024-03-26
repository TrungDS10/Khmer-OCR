import streamlit as st
from PIL import Image
@st.cache_data
def home_setup():
    col1,col2,col3 = st.columns([4,1,9])
    with col1:
        image = Image.open('logo1.jpeg')
        st.image(image)
    with col2:
        st.write("")
    with col3:
        st.title(" DEMO ")
        st.subheader("KhMer Reader Application")

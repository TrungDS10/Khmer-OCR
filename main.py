import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
from home_setup import *
from pdf_uploader import *

st.set_page_config(
    page_title="PDF Text Converter",
    page_icon="👋",
    layout = "wide"
)

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options =["Home", "Instruction","Text Converter"], 
        icons = ['house','book','images'],
        menu_icon = 'list',
        default_index = 0,
    )

if selected == "Home":  
   home_setup()

if selected == "Instruction":
    st.title("PDF Text Converter Instruction")
    st.markdown(
        '''
        Upload pdf file or image to use this application, you can find some example here: https://drive.google.com/file/d/1YJwgPWeNjYvtSOYqAUdg8lO8I-QPMRuP/view?usp=sharing
        '''
    )   
if selected == "Text Converter":
   st.title("PDF Text converter")
   with st.expander("**README**"):
      st.markdown(
         '''
         Upload pdf file or image to use this application, you can find some example here: https://drive.google.com/file/d/1YJwgPWeNjYvtSOYqAUdg8lO8I-QPMRuP/view?usp=sharing
         '''
      )   
   display_file = upload_pdf_file()
   

   
 

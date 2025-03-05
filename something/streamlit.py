import os
import streamlit as st

from docx import Document

import warnings
warnings.filterwarnings('ignore')

#importing function from application file

from app import analyze_text

st.sidebar.title("Menu")
st.sidebar.success("click on a demo above.")

task = st.sidebar.button("Performance Qualification")

if task:
    file = st.file_uploader('Upload the text file for Requirement Extraction')
    st.markdown('Click on **EXTRACT** after selecting the file')
   
    with st.form(key='my_form_to_submit'):
        submit_button = st.form_submit_button(label='EXTRACT')
       
        if submit_button:
            if file is not None:
                # Read the file content
                file_content = file.read().decode('utf-8')
                st.markdown('Performance Qualification generation using Google Gemini')
                text_g = analyze_text(file_content)
                
                st.write('Extracted PQ')
                st.write(text_g)
            else:
                st.write("Please upload a file before clicking EXTRACT.")

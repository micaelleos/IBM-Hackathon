import streamlit as st
import time

def side_bar():
    s = st.sidebar
    s.page_link("directory.py", label="Regulation Directory", icon="📂")
    with s:
        st.write("Workflow")
    s.page_link("pages/main.py", label="Regulatory Impact Analysis", icon="1️⃣")
    s.page_link("pages/main2.py", label="Regulatory Action Plan", icon="2️⃣", disabled=True)
    s.page_link("pages/main3.py", label="Internal Policies and Procedures", icon="3️⃣", disabled=True)
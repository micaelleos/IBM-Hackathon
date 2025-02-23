import streamlit as st
import os
from text import regulation
import pdfplumber
from sidebar import side_bar

side_bar()

st.title("Regulation Directory")



if "regulations" not in st.session_state:
    st.session_state.regulations = []
    st.session_state.regulations.append(regulation)

def save_uploadedfile(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        st.session_state.regulations.append({"title":"","text":text,"status":"Not Analizes","docs":{"roles":{"Compliance":"Not approved","Legal":"Not approved"}}})

uploaded_file = st.file_uploader("Add a new regulation", type=['pdf'], accept_multiple_files=False)

if uploaded_file is not None:
    with st.spinner('Uploading file...'):
        save_uploadedfile(uploaded_file)


def reg_bloc(regulation):
    with st.container(height=350):
        with st.container():
            st.write(f"**Title:** {regulation['title']}")
            st.write(f"**Status:** {regulation['status']}")
            st.write(f"**Text:** {regulation['text'][:200]}...")
            st.button("See documents", use_container_width= True)
            # st.write(f"**Roles for approvel:**")
            # for i in regulation['docs']['roles'].keys():
            #     st.write(f"{i} - status: {regulation['docs']['roles'][i]}")

if "regulations" in st.session_state:
    reg = st.session_state.regulations
    cols = st.columns(2)
    i=0
    for r in reg:
        with cols[i]:
            reg_bloc(r)
            i= i + 1
        if i > 1:
            i=0
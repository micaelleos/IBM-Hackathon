import streamlit as st
import os
from text import regulation
from sidebar import side_bar
from src.util import save_uploadedfile, init_workflow

if "current_regulation" not in st.session_state:
    st.session_state.current_regulation = {
        "regulation":None,
        "impact_analisys": True, 
        "action_plan": True, 
        "policies": True
    }


side_bar()

st.title("Regulation Directory")

if "regulations" not in st.session_state:
    st.session_state.regulations = []
    st.session_state.regulations.append(regulation)


if "system_params" not in st.session_state:
    st.session_state.system_params = {}
    st.session_state.system_params["role"] = "Compliance"

if "show_regulation" not in st.session_state:
    st.session_state.show_regulation = None


def call_show_documents_page(regulation):
    st.session_state.show_regulation  = regulation
    st.switch_page("pages/show_documents.py")


uploaded_file = st.file_uploader("Add a new regulation", type=['pdf'], accept_multiple_files=False)

if uploaded_file is not None:
    with st.spinner('Uploading file...'):
        save_uploadedfile(uploaded_file)

def reg_bloc(regulation):
    with st.container(height=400):
        with st.container():
            st.write(f"**Title:** {regulation['title']}")
            st.write(f"**Status:** {regulation['status']}")
            st.write(f"**Text:** {regulation['text'][:200]}...")
            if st.button("Init workflow",use_container_width=True):
                init_workflow(regulation["id"])
            if st.button("See documents", use_container_width= True):
                call_show_documents_page(regulation)

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
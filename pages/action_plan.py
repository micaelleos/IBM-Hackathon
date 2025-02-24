import streamlit as st
from src.complianceBot import ComplianceAgent
from styles import *
import os
from src.util import doc_approved
from sidebar import side_bar
import uuid

side_bar()

styles()

hash = uuid.uuid4()


@st.dialog("Role configuration")
def modal():
        st.markdown("## Role")
        role = st.radio(
            "Select the role",
            ["Compliance","Legal","Risk","Operations"], #Compliance, Legal, Risk, Operations, IT, (T), Internal Audit (A), Corporate Governance (G)
            horizontal=True,
            index=("Compliance","Legal","Risk","Operations").index(st.session_state.system_params["role"])  # mantém o valor anterior
        )
        if st.button("Salvar"):
            st.session_state.system_params["role"] = role
            st.rerun()

@st.fragment
def atualizar_chat(chat_container,prompt=None):
    with chat_container:
        if not prompt:
            initial_message = st.chat_message("assistant")
            initial_message.write("Hi, how can I assist you today?")
        messages = st.session_state.messages

        for i in range(0,len(messages)):
            message = messages[i]       
                                
            if message['role'] == "assistant":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            else:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])    

        if prompt:
            with st.chat_message("assistant"):
                with st.spinner(""): 
                    response=chat.chat(prompt)
                st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


if "messages" not in st.session_state:
    st.session_state.messages = []

if "document" not in st.session_state:
    st.session_state.document = None

chat = ComplianceAgent(st.session_state.system_params,st.session_state.regulations[0],hash)

with st.container():
    
    with st.container():
        col1, col2 = st.columns([0.8,0.2])
        with col1:
            st.title("Regulatory Impact Analysis Agent")
        with col2:
            if st.button("Role: " + st.session_state.system_params["role"],use_container_width=True): #:information_source: :receipt:
                modal()

    
    col11, col22 = st.columns([0.5,0.5])
    with col22:
        with st.container(border=False):
            chat_container = st.container(height=400,border=False)
            atualizar_chat(chat_container)

            if prompt:= st.chat_input("Make a question...",key="user_input"):
        
                st.session_state.messages.append({"role": "user", "content": prompt})
                atualizar_chat(chat_container,prompt)
                
    with col11:        
        if st.session_state.document:
            with st.expander("Document",expanded=True):
                for i in st.session_state.document:
                    st.markdown("## "+st.session_state.document[i]["title"])
                    st.markdown(st.session_state.document[i]["description"])

        else:
            with st.expander("Document",expanded=False):
                st.markdown("__Document__")
        with st.container(border=False):
            colsx = st.columns([0.3,0.3,0.3])
            with colsx[0]:
                pass
            with colsx[1]:
                if st.session_state.document:
                    if st.button(label="Approve",
                                       type="primary",
                                       use_container_width=True):
                        doc_approved(role=st.session_state.system_params["role"],type="Regulatory Action Plan", doc= st.session_state.document,workflow='action_plan', id_regulation=0)
                        

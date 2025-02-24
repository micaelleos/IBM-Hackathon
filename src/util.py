import streamlit as st
from langchain_ibm import WatsonxLLM
from ibm_granite_community.notebook_utils import get_env_var
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Literal
import pdfplumber
import uuid

load_dotenv()

def doc_approved(role,type,doc,id_regulation,workflow:Literal["impact_analisys", "action_plan", "policies"]):
    
    n = None
    if workflow == 'impact_analisys':
        n = 0
    elif workflow == "action_plan":
        n = 1
    elif workflow == 'policies':
        n = 2

    print("OIIII",len(st.session_state.regulations[id_regulation]['docs']), n+1)

    if len(st.session_state.regulations[id_regulation]['docs']) == n +1 :

        st.session_state.regulations[id_regulation]['docs'][n]['roles'][role] = "Approved"
        
        approved_dict = st.session_state.regulations[id_regulation]['docs'][n]['roles']
        if "Not approved" in approved_dict.values():
            status = "Pending review" 
        else: 
            status = "Approved"
            if workflow == "impact_analisys":
                st.session_state.current_regulation["action_plan"] = False
            if workflow == "action_plan":
                st.session_state.current_regulation["policies"] = False

        st.session_state.regulations[id_regulation]['docs'][n] = {
            "title":type,
            "text":doc,
            "status":status,
            "roles":approved_dict,
            "workflow":workflow
        }

    else:

        role_dict = {
                "Compliance":"Not approved",
                "Legal":"Not approved",
                "Risk":"Not approved",
                "Operations":"Not approved"
            }
        role_dict[role] = "Approved"

        st.session_state.regulations[id_regulation]['docs'].append({
            "title":type,
            "text":doc,
            "status":"Pending review",
            "roles":role_dict,
            "workflow":workflow
        })  
    
def doc_summary(text):
    pass

def save_uploadedfile(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        st.session_state.regulations.append(
            {"title":"",
             "id":uuid.uuid4(),
             "text":text,
             "status":"Not Analizes",
             "docs":[{"roles":
                     {"Compliance":"Not approved",
                      "Legal":"Not approved"}}]
            })


def search_regulation(id):
    for reg in st.session_state.regulations:
        if reg['id'] == id:
            return reg


def init_workflow(id):
    st.session_state.current_regulation["regulation"] = search_regulation(id)
    st.session_state.current_regulation["impact_analisys"] = False
    st.switch_page("pages/impact_analisys.py")

import streamlit as st
import time

def side_bar():
    s = st.sidebar
    with s:
        st.logo("logoComplyFlow.png",size="large")
        #st.markdown("# ComplyFlow")
    s.page_link("directory.py", label="Regulation Directory", icon="📂")
    with s:
        st.write("Workflow")
        impact_analisys = st.session_state.current_regulation['impact_analisys']
        action_plan = st.session_state.current_regulation['action_plan']
        policies = st.session_state.current_regulation['policies']

    s.page_link("pages/impact_analisys.py", label="Regulatory Impact Analysis", icon="1️⃣", disabled= impact_analisys)
    s.page_link("pages/action_plan.py", label="Regulatory Action Plan", icon="2️⃣", disabled= action_plan)
    s.page_link("pages/policies.py", label="Internal Policies and Procedures", icon="3️⃣", disabled = policies)
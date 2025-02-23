import streamlit as st

def doc_approved(role,type,doc,id_regulation):
    print("aqui-----------",role)
    if st.session_state.regulations[id_regulation]['docs']:
        print("outro ------",st.session_state.regulations[id_regulation]['docs'])
        st.session_state.regulations[id_regulation]['docs']['roles'][role] = "Approved"
        
        approved_dict = st.session_state.regulations[id_regulation]['docs']['roles']
        if "Not approved" in approved_dict.values():
            status = "Pending review" 
        else: 
            status = "Approved"

    st.session_state.regulations[id_regulation]['docs'] = {
        "title":type,
        "text":doc,
        "status":status,
        "roles":approved_dict,
    }

    print(st.session_state.regulations[id_regulation]['docs'])
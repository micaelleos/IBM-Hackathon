from sidebar import side_bar
import streamlit as st

side_bar()

st.title("Documents Details")

if st.button("Back"):
    st.switch_page("directory.py")

regulation = st.session_state.show_regulation 



for reg in regulation["docs"]:
    with st.container(border=True, height= 500):
        for doc in reg:
            if doc == "text":
                for i in reg[doc]:
                    st.write(f"**{reg[doc][i]['title']}:**")
                    st.write(f"{reg[doc][i]['description']}")
                
            elif doc == "roles":
                for r in reg[doc]:
                    st.write(f"**{r}:** {reg[doc][r]} ")
                    
            else:
                st.write(f"**{doc.capitalize()}**: {reg[doc]}")

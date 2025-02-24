from sidebar import side_bar
import streamlit as st

side_bar()

st.title("Documents Details")

if st.button("Back"):
    st.switch_page("directory.py")

regulation = st.session_state.current_regulation


with st.container(border=True, height= 500):
    for doc in regulation["docs"]:
        if doc == "text":
            for i in regulation['docs'][doc]:
                st.write(f"**{regulation['docs'][doc][i]['title']}:**")
                st.write(f"{regulation['docs'][doc][i]['description']}")
              
        elif doc == "roles":
            for r in regulation['docs'][doc]:
                st.write(f"**{r}:** {regulation['docs'][doc][r]} ")
                
        else:
            st.write(f"**{doc.capitalize()}**: {regulation['docs'][doc]}")
        #st.write(regulation["docs"][doc]["description"])

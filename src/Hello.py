import streamlit as st

st.set_page_config(
    page_title="Weeping Wranglers",
    page_icon="🧑🏼‍💻",
)

st.write("# Welcome to Our Project! 👋")

st.markdown(
    """
    We are the Weeping Wranglers. We are a group of student 
    from DSA3101 who designed an AI-Powered Knowledge Graph.
    This is designed for the fiancial analyst companies to extract
    meaningful insights from their database.
    We even trained a chatbot to allow for quicker querying of the database!

    
    **👈 Select a page from the sidebar** 
    
    
    Try it out for yourself!
    
"""
)






# Do not removes the following lines

st.session_state.last_query = None

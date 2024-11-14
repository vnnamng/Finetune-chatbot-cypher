import streamlit as st
import streamlit.components.v1 as components
from neo4j import GraphDatabase, basic_auth
from ui import draw_graph_with_pyvis
import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv('NEO4J_URI')
user = os.getenv('NEO4J_USERNAME')
password = os.getenv('NEO4J_PASSWORD')
driver = GraphDatabase.driver(host, auth=(user, password))

nodes_text_properties = {  # what property to use as text for each node
    "Country": "name",
    "Industry": "name",
    "Region": "name",
    "Company": "ticker",
    "Sector": "name",
}


if "queries" not in st.session_state.keys() or st.session_state.queries == []:
    st.markdown("No queries found in session state.")
else:
    print("Queries found in session state.")
    print(st.session_state.queries)
    HtmlFile, path = draw_graph_with_pyvis(driver, st.session_state.queries, nodes_text_properties, custom_html_name = 'custom_pyvis_graph')
    components.html(HtmlFile.read(), height=700)
driver.close()
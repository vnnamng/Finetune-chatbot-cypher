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

queries = ["""
    MATCH (a)-[r]-(b)
    RETURN a, r, b 
    """]
HtmlFile, path = draw_graph_with_pyvis(driver, queries, nodes_text_properties, custom_html_name = 'full_pyvis_graph')

st.markdown("Due to performance issues, pls wait a while for the graph to load.")
st.markdown("If the graph does not load, please refresh the page.")
st.markdown("Zoom in and out to view the full graph.")

components.html(HtmlFile.read(), height=700)
driver.close()
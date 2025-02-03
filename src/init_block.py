
import streamlit as st
import pandas as pd
import requests 
import os
from pandas import read_csv
import time
import json

def init_block():
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f'<p id="label_tag">Project Name</p>', unsafe_allow_html=True)
        st.markdown("<p id='env_comment'>Project name is only for reference purpose</p>",unsafe_allow_html=True)
        project_name = st.text_input(label="",placeholder="Name Your Project.. ",key="project_text_input",label_visibility="collapsed")
        if project_name:
            st.session_state["domains"] = True
            st.session_state["project_name"] = False
        

    st.divider()
    col1, col2 = st.columns([2,1 ])
    with col1:
        st.markdown(f'<p id="label_tag">Define Business Domain</p>', unsafe_allow_html=True)
        st.markdown("<p id='env_comment'>Business domain name will be used to generate database name. Example : MARKETING_PROD, MARKETING_QA</p>",unsafe_allow_html=True)
        domain_name = st.text_input(label = "",placeholder="e.g., Marketing, Healthcare or Finance ",key = "domains_input",label_visibility="collapsed")
        domain_name = (domain_name.replace(" ","")).upper()
        if domain_name and project_name:
            st.session_state["envs"] = True
            st.session_state["domains"] = False

    st.divider()
   
    return (domain_name,project_name)
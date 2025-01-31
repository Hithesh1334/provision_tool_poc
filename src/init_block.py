
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
        st.markdown(f'<p id="label_tag">Please specify your project name</p>', unsafe_allow_html=True)
        
        project_name = st.text_input(label="",placeholder="Project Name... ",key="project_text_input",label_visibility="collapsed")
        if project_name:
            st.session_state["domains"] = True
            st.session_state["project_name"] = False

    st.divider()
    col1, col2 = st.columns([2,1 ])
    with col1:
        st.markdown(f'<p id="label_tag">Please specify your business domain</p>', unsafe_allow_html=True)
        domain_name = st.text_input(label = "",placeholder="Marketing",key = "domains_input",label_visibility="collapsed")
        domain_name = (domain_name.replace(" ","")).upper()
        if domain_name and project_name:
            st.session_state["envs"] = True
            st.session_state["domains"] = False

    st.divider()
    
    env_list = []
    st.session_state['envs'] = False

    st.markdown(f'<p id="label_tag">Please select the environments required</p>', unsafe_allow_html=True)
    comment_content= "* Project name is only for reference purpose. Business domain name will be used to generate database name. Example : MARKETING_PROD, MARKETING_QA"
    st.markdown(f'<p id="env_comment">{comment_content}</p>', unsafe_allow_html=True)
    
    prod = st.checkbox(label="PROD",disabled= st.session_state['envs'])
    dev = st.checkbox(label="DEV",disabled= st.session_state['envs'])
    qa = st.checkbox(label="QA",disabled= st.session_state['envs'])
    nonprod = st.checkbox(label="NONPROD",disabled= st.session_state['envs'])
    sandbox = st.checkbox(label="SANDBOX",disabled= st.session_state['envs'])

    if prod:
        env_list.append("PROD")
    if dev:
        env_list.append("DEV")
    if qa:
        env_list.append("QA")
    if nonprod:
        env_list.append("NONPROD")
    if sandbox:
        env_list.append("SANDBOX")

    st.divider()
    if st.session_state["project_setup_spinner"]:
        my_bar = st.progress(0, text="")
    if project_name and st.session_state["project_setup_spinner"]:
        my_bar.progress(40,text="")
    if domain_name and st.session_state["project_setup_spinner"]:
        my_bar.progress(75,text="")
    if project_name and domain_name and env_list:
        my_bar.progress(100,text="")
        if st.session_state["project_setup_spinner_check"]:
            with st.spinner('In progress...'):
                time.sleep(3)
            st.session_state["project_setup_spinner_check"] = False
            st.session_state['status'][0] = True

    return (domain_name,env_list,project_name)
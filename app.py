import streamlit as st
import pandas as pd
import requests 
import os
from pandas import read_csv
import time
import json
from src.init_block import init_block
from src.warehouse import warehouse_fun
from src.user import user_fun
from src.roles import roles_fun
from src.schema import schema_fun
from src.json_handler import json_handler_fun
from src.display_yml import display_yml_fun

import yaml
import collections
import zipfile
from io import BytesIO
from PIL import Image


im = Image.open("phdata-removebg-preview.png")
st.set_page_config(page_title="Provision Tool", page_icon=im,layout='wide')

with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True) #adding css to streamlit

if 'project_name' not in st.session_state:
    st.session_state['project_name'] = True
if 'domains' not in st.session_state:
    st.session_state['domains'] = False
if 'envs' not in st.session_state:
    st.session_state['envs'] = False
if 'status' not in st.session_state:
    st.session_state['status'] = [False,False,False,False,False,False,False]
if 'state' not in st.session_state:
    st.session_state['state'] = [False,False,False,False,False,False]
if "rows" not in st.session_state:
    st.session_state["rows"] = [{"user_name": "", "password": "", "roles": []}]
if "yaml" not in st.session_state:
    st.session_state["yaml"] = False
if "save_button" not in st.session_state:
    st.session_state['save_button'] = False
if "warehouse" not in st.session_state:
    st.session_state["warehouse"] = [{"warehouse_name":"","warehouse_size":"","warehouse_type":"","initially_suspended":""}]
if "project_setup_spinner" not in st.session_state:
    st.session_state["project_setup_spinner"] = True
if "warehouse_spinner" not in st.session_state:
    st.session_state["warehouse_spinner"] = True
if "user_spinner" not in st.session_state:
    st.session_state["user_spinner"]  = True
if "roles_spinner" not in st.session_state:
    st.session_state["roles_spinner"] = True
if "Role" not in st.session_state:
    st.session_state["Role"] = [{"Roles":""}]
if "role_assign_user" not in st.session_state:
    st.session_state["role_assign_user"] = [{"Select_user":"","Select_role":""}]
if "project_setup_spinner_check" not in st.session_state:
    st.session_state["project_setup_spinner_check"] = True
if "schemas" not in st.session_state:
    st.session_state["schemas"] = [{"Schema_name":"","Database_name":[]}]
if "df" not in st.session_state:
            st.session_state['df'] = pd.DataFrame({})

if "generate_yml_button" not in st.session_state:
    st.session_state["generate_yml_button"] = False
# multipage handling comes here
# if "first_page" not in st.session_state:
#     st.session_state["first_page"] = True
# if "second_page" not in st.session_state:
#     st.session_state["second_page"] = True
# if "third_page" not in st.session_state:
#     st.session_state["third_page"] = True


def main():
    st.logo("image.png",size="large")
    st.title("Provision Tool")
    my_bar = st.progress(0,text="")
    with st.expander(label="Project Setup",expanded=True) as first_block:
        domain_name, project_name = init_block()

    if project_name and domain_name:
        my_bar.progress(20,text="")

    with st.status(label="Environment Setup",expanded=st.session_state['status'][3],state='complete' if st.session_state['state'][3] else 'error') as schema_container:
        schema_list,env_list = schema_fun(domain_name)

    if schema_list and env_list:
        my_bar.progress(40,text="")

    with st.status(label="Warehouse Setup",expanded=st.session_state['status'][0],state='complete' if st.session_state['state'][0] else 'error') as warehouse_container:
        warehouse,rm_name,rm_creditQuota,rm_frequency,rm_monitor_type,rm_notify,rm_notify_suspend,rm_notify_only = warehouse_fun(domain_name) 
    
    if warehouse and rm_creditQuota and rm_frequency and rm_name:
        my_bar.progress(60,text="")

    with st.status(label="Define Required Roles",expanded=st.session_state['status'][2],state='complete' if st.session_state['state'][2] else 'error') as roles_container:
        init_roles,roles_list,rw_ro = roles_fun(env_list)

    if init_roles and roles_list and rw_ro:
        my_bar.progress(80,text="")

    with st.status(label="Define Required Users.",expanded=st.session_state['status'][1],state='complete' if st.session_state['state'][2] else 'error') as user_block:
        user,role_assign_user = user_fun(roles_list) 
    
    if user and role_assign_user:
        my_bar.progress(100,text="")

    st.divider()

        # print("line 343",schema_list)
    
    if st.button("Save Data",disabled=st.session_state['save_button']):
        json_handler_fun(project_name,user,role_assign_user,warehouse,rm_name,rm_creditQuota,rm_frequency,rm_monitor_type,rm_notify,rm_notify_suspend,rm_notify_only,domain_name,env_list,roles_list,schema_list)
        st.session_state["generate_yml_button"] = True
    
    if st.button("Generate YML",key="json_to_ymal",disabled=st.session_state["save_button"]) and st.session_state["generate_yml_button"] :
        display_yml_fun()
    

if __name__ == '__main__':
    main()

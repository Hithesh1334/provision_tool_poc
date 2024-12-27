import streamlit as st
import pandas as pd
import requests 
from pandas import read_csv
import time

st.set_page_config(layout="wide")
def add_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

add_css("style.css")

add_css("style.css")


if "status_state" not in st.session_state:
    st.session_state["status_state"] = [True, False, False, False, False, False, False, False]  #for expander 
    st.session_state["is_completed"] = [False, False, False, False, False, False, False, False] #to disable the inputs 

def main():
    st.title("Provision Tool UI")

    data = {
        "Snowflake": {
            "ProjectName": "",
            "env": [],
            "user": [],
            "warehouse": [],
            "Domains": []
        }
    }

    with st.status("What is your project name", expanded = st.session_state['status_state'][0], state = "complete" if st.session_state['is_completed'][0] else "error") as first_block:
        project_name = st.text_input("Enter the Project Name ")
        
        if st.button("next", key="first_block"):
            st.session_state['status_state'][0] = False
            first_block.update( expanded = st.session_state['status_state'][0], state = "complete") # collapsing the widget and changing status to completed
            st.session_state['status_state'][1] = True
            if project_name:
                st.session_state['is_completed'][0] = True 
          
    with st.status("What are the domains that needs to be included", expanded=st.session_state['status_state'][1],state = "complete" if st.session_state['is_completed'][1] else "error") as second_block:
        domains_list = st.multiselect(label = "select the domains",
                       options=[
                           "Marketing",
                           "Finance",
                           "sales"
                       ],
                       key="second_block_multiselect",
                       disabled=not (all(st.session_state['is_completed'][:1]))) # all() returns true values if the list contains ture [this will check if privious valuse has been entered or not]

        if st.button("next", key="second_block"):
            st.session_state['status_state'][1] = False
            second_block.update( expanded = st.session_state['status_state'][1], state= "complete" )
            st.session_state['status_state'][2] = True
            st.session_state['is_completed'][1] = True
    
    with st.status("What are the envs that needs to be included", expanded=st.session_state['status_state'][2],state = "complete" if st.session_state['is_completed'][2] else "error") as third_block:
        envs_list = st.multiselect(label = "select the domains",
                       options=[
                           "PROD",
                           "DEV",
                           "QA",
                           "NONPROD",
                           "SANDBOX"
                       ],key="third_block_multiselect",
                       disabled=not all(st.session_state['is_completed'][:2]))
    
        if st.button("next", key="third_block"):
            st.session_state['status_state'][2] = False
            third_block.update( expanded = st.session_state['status_state'][2] , state = "complete")
            st.session_state['status_state'][3] = True
            st.session_state['is_completed'][2] = True

    with st.status("what are the warehose needs to be included", expanded=st.session_state['status_state'][3],state = "complete" if st.session_state['is_completed'][3] else "error") as fourth_block:
        cols = st.columns(3)
        with cols[0]:
            warehouse_name = st.text_input("enter the warehouse name",key="warehouse",
                       disabled=not all(st.session_state['is_completed'][:3]))
            if warehouse_name:
                data["Snowflake"]["warehouse"] = warehouse_name

        with cols[1]:
            warehouse_size = st.selectbox(
                        "warehouse Size",
                        ("x-small", "small", "medium","large","x-large"),
                       disabled=not all(st.session_state['is_completed'][:3]))
    
        if st.button("next", key="warehose_block"):
            st.session_state['status_state'][3] = False
            fourth_block.update( expanded = st.session_state['status_state'][3] , state = "complete")
            st.session_state['status_state'][4] = True
            st.session_state['is_completed'][3] = True 

    with st.status("How many users to be included", expanded=st.session_state['status_state'][4],state = "complete" if st.session_state['is_completed'][3] else "error") as user_block:
        cols = st.columns(3)
        with cols[0]:
            user_name = st.text_input("enter the user(comma-separated)",key="user",
                       disabled=not all(st.session_state['is_completed'][:3]))
            if user_name:
                data["Snowflake"]["user"] = user_name
     
        if st.button("next", key="user_block"):
            st.session_state['status_state'][4] = False
            user_block.update( expanded = st.session_state['status_state'][4] , state = "complete")
            st.session_state['status_state'][5] = True
            st.session_state['is_completed'][4] = True 

    with st.status("Roles creation", expanded=st.session_state['status_state'][5],state = "complete" if st.session_state['is_completed'][5] else "error") as role_block:
        cols = st.columns(3)
        with cols[0]:
            role_name = st.text_input("enter the roles to be created (comma-separated)",
                       disabled=not all(st.session_state['is_completed'][:3]))    
    
        if st.button("next", key="role_block"):
            st.session_state['status_state'][5] = False
            role_block.update( expanded = st.session_state['status_state'][5] , state = "complete")
            st.session_state['status_state'][6] = True
            st.session_state['is_completed'][5] = True 

    with st.status("create database level objects ", expanded=st.session_state['status_state'][6],state = "complete" if st.session_state['is_completed'][7] else "error") as fifth_block:
        database_name = st.text_input("enter the databases to be created (comma-separated)",
        key="database",disabled=not all(st.session_state['is_completed'][:3]))
       
        print(database_name)
        database_name = database_name.split(",")

        if st.button("next", key="fifth_block"):
            st.session_state['status_state'][6] = False
            fifth_block.update( expanded = st.session_state['status_state'][3] , state = "complete")
            st.session_state['status_state'][7] = True
            st.session_state['is_completed'][6] = True 

    with st.status("create database level objects ", expanded=st.session_state['status_state'][7],state = "complete" if st.session_state['is_completed'][7] else "error") as database_schema_block:
    
    
        for env in envs_list:
            env_data = {
                env: [
                    {
                        "database": database_name,
                        "schemas": [
                            {
                                st.selectbox("which database",database_name,key=f"{env}"): st.text_input(f"Enter schemas for database in {env} (comma-separated)").split(",")
                            }
                        ],
                        "role": role_name,
                    }
                ]
            }
            data["Snowflake"]["env"].append(env_data)
        
        if st.button("next", key="fifthasdfa_block"):
            st.session_state['status_state'][7] = False
            database_schema_block.update( expanded = st.session_state['status_state'][3] , state = "complete")
            st.session_state['status_state'][7] = True
            st.session_state['is_completed'][7] = True 
            
if __name__ == '__main__':
    main()

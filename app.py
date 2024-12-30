import streamlit as st
import pandas as pd
import requests 
from pandas import read_csv
import time

st.set_page_config(layout="wide")

with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if 'project_name' not in st.session_state:
    st.session_state['project_name'] = True
if 'domains' not in st.session_state:
    st.session_state['domains'] = False
if 'envs' not in st.session_state:
    st.session_state['envs'] = False
if 'status' not in st.session_state:
    st.session_state['status'] = [False,False,False]
if 'state' not in st.session_state:
    st.session_state['state'] = [False,False,False]

def main():
    st.title("Provision Tool POC")

    with st.container(border=True,key="first_block"):
        st.subheader("What is the project Name?")
        project_name = st.text_input(label='',placeholder="project name... ",disabled=not st.session_state["project_name"],key="project_text_input")
        if project_name:
            st.session_state["domains"] = True
            st.session_state["project_name"] = False
        st.divider()

        st.subheader("What are the domains to be included?")
        with open("domains.txt","r") as file:
            domains = [line.strip() for line in file]
        domain_list = st.pills(label="domains",selection_mode="multi",options=domains,disabled=not st.session_state['domains'],default=None) #change this to st.selector if required
        if domain_list and project_name:
            st.session_state["envs"] = True
            st.session_state["domains"] = False
            # st.success('This is a success message!', icon="✅")
        # else:
        #     st.error('Please enter the value before proceeding', icon="🚨")
        st.divider()
        
        
        st.subheader("What are the environments/database to be created on Snowflake?")
        cols = st.columns(2)
        with cols[0]:
            stander_envs = st.checkbox(label="Standard Environments/Database")
        with cols[1]:
            customized_envs = st.checkbox(label="customized")
        if stander_envs and customized_envs:
            st.write("Please select any one not both")
        elif stander_envs:
            st.session_state['envs'] = False
            env_list = st.pills(label="envs",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)
        elif customized_envs:
            st.session_state['envs'] = True
            env_list = st.pills(label="envs",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)
        if st.button("Next",key="first_block_button"):
            if project_name and domain_list:
                st.session_state['status'][0] = True
                # add here st.success and st.error
        
        # drop down code is from here
        # do you need all the combinations of env and domains? if no then specify them
            # for this i can have one expander which will have a editor dataframe which will include all the combination of env and domains and one extra column which will be tick box.
        # user followed by role creation expander below roles one tick box to ask weather they need rw/ro combinations
        # Then warehouse creation block which includes resource monitor tick box do you need rm 
        # Then schema creation part
        # Then role grant privileges grant part

    # WAREHOUSE CREATION CODE COMES HERE
    with st.status(label="Please specify the warehouse that needs to be created",expanded=st.session_state['status'][0],state='error') as warehouse_container:
        cols = st.columns(5)
        with cols[0]:
            warehouse_name = st.text_input("Warehouse name",placeholder="adhoc_wh",key="warehouse_name")
        with cols[1]:
            warehouse_size = st.selectbox(label="warehouse size",options=['X-Small','Small','Medium','Large','X-large'])
        with cols[2]:
            warehouse_initially_suspended = st.selectbox(label="Initially Suspend",options=['True','False'])
        rm_required = st.checkbox(label="Do you need resource monitor?")
        if rm_required: 
            rm_name = st.text_input(label = "Resource monitor name",placeholder="load_monitor",key="resource_monitor")
            rm_frequency = st.selectbox(label="What should be the frequency of resource monitor",options=['Daily','Weekly','Monthly'])
            st.write("Select the below optinos of how would you like to be notifyed")
            rm_notify = st.checkbox(label = "notify at 70%")
            rm_notify_suspend = st.checkbox(label = "notify and suspend at 85%")
            rm_notify_only = st.checkbox(label = "notify at 95%")
        
        if st.button("Next",key="warehouse_block_button"):
            st.session_state['status'][0] = False
            st.session_state['status'][1] = True
            warehouse_container.update(expanded=st.session_state['status'][0],state="complete")

    with st.status(label="Please specify the roles that need to be created.",expanded=st.session_state['status'][1],state='error') as roles_container:
        radio_value = st.checkbox(label="do you need all the combinations of env and domains?",)
        if radio_value :
            role_name = st.text_input(label = "Enter the role name",placeholder="dataEngineer",key="role_name")  #make it dataframe
            domain_name_included = st.checkbox(label="do you need Domain names to be included into your object names?",key="domain_radio")
            envs_name_included = st.checkbox(label="do you need envs/Database names to be included into your object names?",key="envs_radio")
            # if domain_name_included  or envs_name_included :
            rw_ro = st.checkbox(label="do you want rw_ro combination as well for each role",)
            if rw_ro :
                #write code here to handle the combinations as mentioned above
                st.write("rw_ro yes")
            st.divider()
            cols = st.columns(2)
            with cols[0]:
                suffix = st.checkbox(label="do you need them to be added as suffix?",key="suffix")
            with cols[1]:
                prifix = st.checkbox(label="do you need them to be added as prefix?",key="prefix")
            # else:
            #     #write a code to display df with the combinatios mentioned with selection options for rw and ro
            #     st.write("rw_ro No")
            # else:
            #     pass
        else:
            #write here the df code to take custome role name as inputs
            pass
        
        if st.button("Next",key="roles_block_button"):
            st.session_state['status'][1] = False
            roles_container.update(expanded=st.session_state['status'][1],state='complete')
            # saving data into a json file code comes here
                                

                    





        
            
if __name__ == '__main__':
    main()

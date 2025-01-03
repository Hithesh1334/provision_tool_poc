import streamlit as st
import pandas as pd
import requests 
from pandas import read_csv
import time
import json

st.set_page_config(layout="wide")

with open('style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

if 'project_name' not in st.session_state:
    st.session_state['project_name'] = True
if 'standard_env' not in st.session_state:
    st.session_state['standard_env'] = False
if 'customized_env' not in st.session_state:
    st.session_state['customized_env'] = False
if 'domains' not in st.session_state:
    st.session_state['domains'] = False
if 'envs' not in st.session_state:
    st.session_state['envs'] = False
if 'status' not in st.session_state:
    st.session_state['status'] = [False,False,False,False,False,False,False]
if 'state' not in st.session_state:
    st.session_state['state'] = [False,False,False,False,False,False]
if 'updated_df' not in st.session_state:
    st.session_state['updated_df'] = [False,False,False,False,False,False]
if 'user_object' not in st.session_state:
    st.session_state['user_object'] = False
if 'database_object' not in st.session_state:
    st.session_state['database_object'] = False
if "rows" not in st.session_state:
    st.session_state["rows"] = [{"user_name": "", "password": "", "roles": []}]


def main():
    st.logo(
    "image.png",
    size="large"
    )
    st.title("phData Provision Tool")

    with st.container(border=True,key="first_block"):
        st.write("Project Name?")
        project_name = st.text_input(label='',placeholder="project name... ",disabled=not st.session_state["project_name"],key="project_text_input")
        if project_name:
            st.session_state["domains"] = True
            st.session_state["project_name"] = False
        st.divider()

        st.write("What are the domains to be included?")
        with open("domains.txt","r") as file:
            domains = [line.strip() for line in file]
        domain_list = st.pills(label="domains",selection_mode="multi",options=domains,disabled=not st.session_state['domains'],default=None) #change this to st.selector if required
        if domain_list and project_name:
            st.session_state["envs"] = True
            st.session_state["domains"] = False

        st.divider()
        
        # st.write("What are the environments/database to be created on Snowflake?")
        cols = st.columns(2)
        env = st.radio(
            "What are the environments/database to be created on Snowflake?",
            ["Standard", "Customized"],
            horizontal=True
        )
        if env == "Standard Environment/Database":
            st.session_state['envs'] = False
            env_list = st.pills(label="envs",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)
        elif env == "Customized":
            st.session_state['envs'] = True
            env_list = st.pills(label="envs",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)

        st.divider()

        if st.button("Next",key="first_block_button"):
            if project_name and domain_list:
                st.session_state['status'][0] = True

    with st.status(label="Please specify the warehouse that needs to be created",expanded=st.session_state['status'][0],state='complete' if st.session_state['state'][0] else 'error') as warehouse_container:
        warehouse_data = pd.read_json("json/warehouse.json")
        warehouse_df = st.data_editor(warehouse_data,column_config={
                "warehouse_size": st.column_config.SelectboxColumn(
                    "warehouse_size",
                    help="The category of the app",
                    width="medium",
                    options=[
                        "X-Small",
                        "Small",
                        "Medium",
                        "Large",
                        "X-Large",
                        "2X-Large",
                        "3X-Large",
                        "4X-Large",
                        "5X-Large",
                        "6X-Large",
                    ],
                    required=True,
                ),
                "warehouse_type": st.column_config.SelectboxColumn(
                    "warehouse_type",
                    help="The category of the app",
                    width="medium",
                    options=[
                        "SNOWPARK-OPTIMIZED",
                        "STANDARD",
                    ],
                    required=True,
                ),
            },hide_index=True,use_container_width=True,num_rows="dynamic")
        
        # resource monitor
        rm_required = st.checkbox(label="Do you need resource monitor?")
        if rm_required: 
            rm_name = st.text_input(label = "Resource monitor name",placeholder="load_monitor",key="resource_monitor")
            rm_monitor_type = st.pills(label = "Monitor type",options=['Account','Warehouse'],key="monitor_type")
            if rm_monitor_type == 'Warehouse':
                st.write("write here warehouse multiselector code")
            rm_frequency = st.pills(label="What should be the frequency of resource monitor",options=['Daily','Weekly','Monthly','Yearly'],selection_mode='single')
            st.write("Select the below optinos of how would you like to be notifyed")
            rm_notify = st.checkbox(label = "notify at 70%")
            rm_notify_suspend = st.checkbox(label = "notify and suspend at 85%")
            rm_notify_only = st.checkbox(label = "notify at 95%")

        st.divider()

        if st.button("Next",key="warehouse_block_button"):
            st.session_state['status'][0] = False
            st.session_state['status'][1] = True
            warehouse_container.update(expanded=st.session_state['status'][0],state="complete")
            st.session_state['state'][0] = True

    
    with st.status(label="Please specify the roles that need to be created.",expanded=st.session_state['status'][1],state='complete' if st.session_state['state'][1] else 'error') as roles_container:
        if not st.session_state['updated_df'][0]:
            roles_data = pd.read_json("json/roles.json")
        else:
            roles_data = pd.read_json("json/updated_Json/updated_roles.json")
        roles_df = st.data_editor(roles_data, use_container_width=True,num_rows="dynamic")
        radio_value = st.checkbox(label="do you need all the combinations of env and domains?",)
        roles_list = {"role_name":[]}
        if radio_value :
            cols = st.columns(2)
            with cols[0]:
                suffix = st.checkbox(label="Add as suffix?",key="suffix")
            with cols[1]:
                prefix = st.checkbox(label="Add as Prefix?",key="prefix")
            domain_name_included = st.checkbox(label="Include domain names in object names?",key="domain_radio")               
                
            envs_name_included = st.checkbox(label="Include env names in object names?",key="envs_radio")

            rw_ro = st.checkbox(label="do you want rw_ro combination as well for each role",)
            with open("json/roles.json", 'r') as file:
                roles_data = json.load(file)
            
            if domain_name_included:
                for role in roles_data:
                    for domain in domain_list:
                        for env in env_list:
                            print(domain,domain_list,role,"line 198")
                            role_name = role['role_name']
                            if suffix:
                                if envs_name_included:
                                    role_name = role_name + '_' + domain + '_' + env
                                else:
                                    role_name = role_name + '_' + domain 
                            if prefix:
                                if envs_name_included:
                                    role_name = env + '_' + domain + '_' + role_name
                                else:
                                    role_name = domain + '_' + role_name

                            roles_list["role_name"].append(role_name)
            # if envs_name_included:
            #     for i in range(len(roles_list['role_name'])):
            #         for env in env_list:
            #             print(roles_list['role_name'][i],i,"line 172",env_list)
            #             role_name = roles_list['role_name'][i]
            #             if suffix:
            #                 role_name = role_name + '_' + env
            #             if prefix:
            #                 role_name = env + '_' + role_name
            #             roles_list['role_name'][i] = role_name
            
            roles_data_new = pd.DataFrame(roles_list)
            roles_data_new = roles_list 
            roles_data_new['rw'] = True
            roles_data_new['ro'] = True
            if rw_ro :
                st.data_editor(roles_data_new,use_container_width=True,num_rows="dynamic",disabled=True)
            else:
                st.data_editor(roles_data_new,use_container_width=True,num_rows="dynamic")
        else:
            #write here the df code to take custome role name as inputs
            pass
        
        st.divider()
        if st.button("Next",key="roles_block_button"):
            st.session_state['status'][1] = False
            roles_container.update(expanded=st.session_state['status'][1],state='complete')
            st.session_state['state'][1] = True
            st.session_state['status'][2] = True
        
    # if st.session_state['user_object']:
    with st.status(label="Please specify the Users to be created",expanded=st.session_state['status'][2],state='complete' if st.session_state['state'][2] else 'error') as user_block:
        def add_row():
            st.session_state["rows"].append({"user_name": "", "password": "", "roles": []})
        def delete_row(index):
            st.session_state["rows"].pop(index)
        user_name = []
        password = []
        role_to_assg = []
        def render_rows():
            for index, row in enumerate(st.session_state["rows"]):
                cols = st.columns(4)
                with cols[0]:
                    row["user_name"] = st.text_input(
                        label=f"User Name",
                        value=row["user_name"],
                        placeholder="user133",
                        key=f"user_name_{index}"
                    )
                with cols[1]:
                    row["password"] = st.text_input(
                        label=f"Password",
                        value=row["password"],
                        placeholder="Temp#@123",
                        key=f"password_{index}",
                        type="password"
                    )
                with cols[2]:
                    role_list = ["SYSADMIN", "SECURITYADMIN", "USERADMIN", "PUBLIC"] + roles_list['role_name'] 
                    row["roles"] = st.multiselect(
                        label=f"Default Role",
                        options=role_list,
                        default=row["roles"],
                        key=f"roles_{index}"
                    )

                with cols[3]:
                    cl = st.columns(2)
                    with cl[0]:
                        if st.button("Add",key=f"add_{index}"):
                            add_row()
                    with cl[1]:
                        if st.button("Del", key=f"delete_{index}"):
                            delete_row(index)
                            st.rerun()  # Force rerun to update the UI
                user_name.append(row["user_name"])
                password.append(row["password"])
                role_to_assg.append(row["roles"])
        

        render_rows()

    if st.button("Save Data"):
        data = {
            "Snowflake": {
                "ProjectName": project_name,
                "user": [
                    {
                        "user_name": user_name,
                        "password": password,
                        "roles": role_to_assg
                    }
                ],
                "warehouse": warehouse_data["warehouse_name"].tolist(),
                "env": [{"databases": env_list}],
                "Domains": ["marketing", "finance", "sales"],
                "roles": roles_data_new["role_name"],
            }
        }

        with open("output.json", "w") as json_file:
            json.dump(data, json_file, indent=2)
        
    if st.session_state['database_object']:
        with st.status(label="Please specify the Users to be created",expanded=st.session_state['status'][3],state='complete' if st.session_state['state'][3] else 'error'):
            st.write("here")

    st.divider()
    
    with st.expander(label="Review",expanded=st.session_state["status"][5]) as review:
        st.write("review section")


if __name__ == '__main__':
    main()

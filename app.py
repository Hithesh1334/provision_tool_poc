import streamlit as st
import pandas as pd
import requests 
from pandas import read_csv
import time
import json
from yaml_convertor import warehouse_yaml
import yaml

st.set_page_config(page_title="Provision Tool", page_icon=":shield:",layout='wide')

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
if 'warehouse_df' not in st.session_state:
    st.session_state['warehouse_df'] = True
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
if "yaml" not in st.session_state:
    st.session_state["yaml"] = False
if "save_button" not in st.session_state:
    st.session_state['save_button'] = True


def main():
    st.logo(
    "image.png",
    size="large"
    )
    st.title("Provision Tool")

    with st.container(border=True,key="first_block"):
        project_name = st.text_input(label="Project Name ?",placeholder="project name... ",disabled=not st.session_state["project_name"],key="project_text_input")
        if project_name:
            st.session_state["domains"] = True
            st.session_state["project_name"] = False

        st.divider()

        with open("domains.txt","r") as file:
            domains = [line.strip() for line in file]
        domain_list = st.pills(label="domains to be included?",options=domains,disabled=not st.session_state['domains'],default=None,selection_mode="multi",key="domains_selector_key") #change this to st.selector if required
        if domain_list and project_name:
            st.session_state["envs"] = True
            st.session_state["domains"] = False

        st.divider()
        
        cols = st.columns(2)
        on = st.toggle(
            "environments/database to be created on Snowflake?",
        )
        env_list = []
        if on:
            st.session_state['envs'] = False
            env_list = st.pills(label="",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)
        # elif env == "Customized":
        #     st.session_state['envs'] = True
        #     # env_list = st.pills(label="envs",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)
        #     st.write("database creation code comes ther ")

        st.divider()

        if st.button("Next",key="first_block_button"):
            if project_name and domain_list:
                st.session_state['status'][0] = True
                st.session_state['warehouse_df'] = False

    with st.status(label="Specify the warehouse to create.",expanded=st.session_state['status'][0],state='complete' if st.session_state['state'][0] else 'error') as warehouse_container:
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
                    default="X-small"
                ),
            },hide_index=True,use_container_width=True,num_rows="dynamic",disabled=st.session_state['warehouse_df'])
        
        # resource monitor
        rm_required = st.checkbox(label="Do you need resource monitor?")
        rm_name,rm_monitor_type,rm_frequency,rm_notify,rm_notify_suspend,rm_notify_only= "","","","","",""
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

    
    with st.status(label="Specify the roles to create.",expanded=st.session_state['status'][1],state='complete' if st.session_state['state'][1] else 'error') as roles_container:
        if not st.session_state['updated_df'][0]:
            roles_data = pd.read_json("json/roles.json")
        else:
            roles_data = pd.read_json("json/updated_Json/updated_roles.json")
        roles_df = st.data_editor(roles_data, use_container_width=True,num_rows="dynamic")
        radio_value = st.checkbox(label="do you need all the combinations of env and domains?",)
        roles_list = {"role_name":[]}
        if radio_value :
            append_on = st.radio(
                label = "",
                options = ["Suffix","Prefix"],
                horizontal = True
            )
            
            domain_name_included = st.checkbox(label="Include domain names in object names?",key="domain_radio")               
                
            envs_name_included = st.checkbox(label="Include env names in object names?",key="envs_radio")

            rw_ro = st.checkbox(label="do you want rw_ro combination as well for each role",)
            with open("json/roles.json") as file:
                roles_data = json.load(file)
            
            if domain_name_included:
                for role in roles_data:
                    for domain in domain_list:
                        for env in env_list:
                            role_name = role['role_name']
                            if append_on == "Suffix":
                                if envs_name_included:
                                    role_name = role_name + '_' + domain + '_' + env
                                else:
                                    role_name = role_name + '_' + domain 
                            if append_on == "Prefix":
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
    with st.status(label="Specify the users to create.",expanded=st.session_state['status'][2],state='complete' if st.session_state['state'][2] else 'error') as user_block:
        def add_row():
            st.session_state["rows"].append({"user_name": "", "password": "", "roles": []})
        def delete_row(index):
            st.session_state["rows"].pop(index)
        user = []
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
                user.append([row["user_name"],row["password"],row["roles"]])
        

        render_rows()

    if project_name and warehouse_df and role_name:
        st.session_state["save_button"] = False

    if st.button("Save Data",disabled=st.session_state['save_button']):
        st.session_state['status'][2] = False
        roles_container.update(expanded=st.session_state['status'][2],state='complete')
        st.session_state['state'][2] = True
        st.session_state['status'][3] = True
        snowflake_config = {
            "Snowflake": {
                "ProjectName": project_name,
                "user": [
                    {
                        "user_name": u[0],
                        "password": u[1],
                        "roles_to_assign": u[2]
                    } for u in user
                ],
                "warehouse": [
                    {
                        "warehouse_name":warehouse_df["warehouse_name"][i],
                        "warehouse_size":warehouse_df["warehouse_size"][i],
                        "warehouse_type":warehouse_df["warehouse_type"][i],
                        "initially_suspended":str(warehouse_df["initially_suspended"][i])
                    } for i in range(len(warehouse_df))
                ],
                "resource_monitor": {
                    "resource_monitor_name":"" if not rm_name else rm_name,
                    "frequency":"" if not rm_frequency else rm_frequency,
                    "monitor_level":"" if not rm_monitor_type else rm_monitor_type,
                    "trigger": {
                        "notify" :"" if not rm_notify else rm_notify,
                        "notify_suspend":"" if not rm_notify_suspend else rm_notify_suspend,
                        "notify_only":"" if not rm_notify_only else rm_notify_only
                    }
                },
                "env": env_list,
                "Domains": domains,
                "roles": roles_list["role_name"]
            }
        }

        with open("output.json", "w") as json_file:
            json.dump(snowflake_config, json_file, indent=2)

        st.divider()
    
        with st.expander(label="Review",expanded=True) as review:
            with open("output.json","r") as file:
                data = json.load(file)
            st.json(data,expanded=True)

    if st.button("Generate",key="json_to_ymal",disabled=st.session_state["save_button"]):
#         st.session_state["yaml"]  = True
#         pass    
# if st.session_state["yaml"]:
        warehouse_yaml()
        with open("groups\\warehouse.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

if __name__ == '__main__':
    main()

import streamlit as st
import pandas as pd
import requests 
from pandas import read_csv
import time
import json
from yaml_convertor import warehouse_yaml
from yaml_convertor import database_yaml
from yaml_convertor import role_yaml
from yaml_convertor import user_yaml
from yaml_convertor import  privileges_yaml
from yaml_convertor import grantRole_yaml
from yaml_convertor import rm_yaml
import yaml
import collections

st.set_page_config(page_title="Provision Tool", page_icon=":shield:",layout='wide')

with open('style.css') as f:
    css = f.read()
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True) #adding css to streamlit

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
    st.session_state['save_button'] = False
if "warehouse" not in st.session_state:
    st.session_state["warehouse"] = [{"warehouse_name":"","warehouse_size":"","warehouse_type":"","initially_suspended":""}]
if "init_spinner" not in st.session_state:
    st.session_state["init_spinner"] = True
if "warehouse_spinner" not in st.session_state:
    st.session_state["warehouse_spinner"] = True
if "user_spinner" not in st.session_state:
    st.session_state["user_spinner"]  = True
if "role" not in st.session_state:
    st.session_state["role"] = [{"role_name":""}]
if "role_assign_user" not in st.session_state:
    st.session_state["role_assign_user"] = [{"Select_user":"","Select_role":""}]


def add(resource,value):
            st.session_state[f"{resource}"].append(value)
def delete(resource,index):
    if len(st.session_state[f"{resource}"]) > 1:
        st.session_state[f"{resource}"].pop(index)


def main():
    st.logo("image.png",size="large")
    st.title("Provision Tool")

    with st.container(border=True,key="first_block"):
        project_name = st.text_input(label="Please specify your project name",placeholder="project name... ",key="project_text_input")
        if project_name:
            st.session_state["domains"] = True
            st.session_state["project_name"] = False

        st.divider()
        
        domain_name = st.text_input(label = "Please specify your business domain",placeholder="marketing",key = "domains_input")
        if domain_name and project_name:
            st.session_state["envs"] = True
            st.session_state["domains"] = False

        st.divider()
     
        env_list = []
        st.session_state['envs'] = False
        env_list = st.pills(label="Please select the environments required",selection_mode="multi",options=["PROD","DEV","QA","NONPROD","SANDBOX"],disabled= st.session_state['envs'],default=None)

        st.divider()
        if not project_name or not domain_name or not env_list:
            st.session_state["init_spinner"] = True
        if st.session_state["init_spinner"]:
            my_bar = st.progress(0, text="")
        if project_name and st.session_state["init_spinner"]:
            my_bar.progress(40,text="")
        if domain_name and st.session_state["init_spinner"]:
            my_bar.progress(75,text="")
        if project_name and domain_name and env_list and st.session_state["init_spinner"]:
            my_bar.progress(100,text="")
            with st.spinner('In progress...'):
                time.sleep(3)
            st.session_state['status'][0] = True
            st.session_state['warehouse_df'] = False
            st.session_state["init_spinner"] = False

    with st.status(label="Specify the warehouse to create.",expanded=st.session_state['status'][0],state='complete' if st.session_state['state'][0] else 'error') as warehouse_container:
        warehouse = []
        def render_rows():
            for index, row in enumerate(st.session_state["warehouse"]):
                cols = st.columns(5)
                with cols[0]:
                    if domain_name:
                        row["warehouse_name"] = st.text_input(
                            label=f"Warehouse Name",
                            value=(f"{domain_name}_Adhoc_wh").upper(),
                            placeholder=(f"{domain_name}_Adhoc_wh").upper(),
                            key=f"warehouse_name_{index}"
                        )
                    else:
                        row["warehouse_name"] = st.text_input(
                            label=f"Warehouse Name",
                            value=row["warehouse_name"],
                            placeholder=f"Domain_Adhoc_wh",
                            key=f"warehouse_name_{index}"
                        )
                with cols[1]:
                    row["warehouse_size"] = st.selectbox(
                        label=f"Warehouse Size",
                        # value=row["warehouse_size"],
                        options = ["X-Small","Small","Medium","Large","X-Large","2X-Large","3X-Large","4X-Large","5X-Large","6X-Large",],
                        placeholder="X-Small",
                        # default = "X-Small",
                        key=f"warehouse_size_{index}",
                    )
                with cols[2]:
                    row["warehouse_type"] = st.selectbox(
                        label=f"Warehosue Type",
                        options=["STANDARD","SNOWPARK-OPTIMIZED"],
                        placeholder="STANDARD",
                        # default= "STANDARD",
                        key=f"warehouse_type_{index}"
                    )
                with cols[3]:
                    row["initially_suspended"] = st.selectbox(
                        label=f"Initially Suspended",
                        options=["True","False"],
                        # placeholder="STANDARD",
                        # default= "STANDARD",
                        key=f"initially_suspended_{index}"
                    )
                with cols[4]:
                    cl = st.columns(2)
                    with cl[0]:
                        if st.button("Add",key=f"add_warehouse_{index}"):
                            add("warehouse",{"warehouse_name":"","warehouse_size":"","warehouse_type":"","initially_suspended":""})
                    with cl[1]:
                        if st.button("Del", key=f"delete_warehouse_{index}"):
                            delete("warehouse",index)
                            st.rerun()  # Force rerun to update the UI
                warehouse.append([row["warehouse_name"],row["warehouse_size"],row["warehouse_type"],row["initially_suspended"]])
        

        render_rows()

        
        # resource monitor
        rm_required = st.checkbox(label="Do you need resource monitor?")
        rm_name,rm_monitor_type,rm_frequency,rm_notify,rm_notify_suspend,rm_notify_only= "","","","","",""
        if rm_required: 
            rm_name = st.text_input(label = "Resource Monitor Name",placeholder="load_monitor",key="resource_monitor")
            rm_monitor_type = st.pills(label = "Monitor Type",options=['Account','Warehouse'],key="monitor_type")
            rm_creditQuota = st.text_input(label= "CreditQuota",placeholder="10",key="creditQuota")
            if rm_monitor_type == 'Warehouse':
                st.write("write here warehouse multiselector code")
            rm_frequency = st.pills(label="What should be the frequency of resource monitor",options=['Daily','Weekly','Monthly','Yearly'],selection_mode='single')
            st.write("Select the below optinos of how would you like to be notifyed")
            rm_notify = st.checkbox(label = "Notify at 70%")
            rm_notify_suspend = st.checkbox(label = "Notify and suspend at 85%")
            rm_notify_only = st.checkbox(label = "Notify at 95%")

        st.divider()

        if warehouse[0][0] and st.session_state["warehouse_spinner"]:
            with st.spinner("In progress..."):
                time.sleep(5)
            st.session_state['status'][0] = False
            st.session_state['status'][1] = True
            warehouse_container.update(expanded=st.session_state['status'][0],state="complete")
            st.session_state['state'][0] = True
            st.session_state["warehouse_spinner"] = False

    with st.status(label="Specify the users to create.",expanded=st.session_state['status'][1],state='complete' if st.session_state['state'][2] else 'error') as user_block:
    
        user = collections.defaultdict(list)
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
                    role_list = ["SYSADMIN", "SECURITYADMIN", "USERADMIN","ACCOUNTADMIN","PUBLIC"] 
                    row["roles"] = st.multiselect(
                        label=f"System Defined Roles",
                        options=role_list,
                        key=f"roles_{index}"
                    )

                with cols[3]:
                    cl = st.columns(2)
                    with cl[0]:
                        if st.button("Add",key=f"add_{index}"):
                            add("rows",{"user_name": "", "password": "", "roles": []})
                    with cl[1]:
                        if st.button("Del", key=f"delete_{index}"):
                            delete("rows",index)
                            st.rerun()  # Force rerun to update the UI
                user[row['user_name']].append(row["user_name"])
                user[row['user_name']].append(row["password"])
                user[row['user_name']].append(row["roles"])
        

        render_rows()

        st.divider()
        # if st.button("Next",key="roles_block_button")
        user_keys = list(user.keys())
        if not(len(user_keys)==1 and user_keys[0]=='') and st.session_state["user_spinner"]:
            with st.spinner("In progress..."):
                time.sleep(5)
            st.session_state['status'][1] = False
            user_block.update(expanded=st.session_state['status'][1],state='complete')
            st.session_state['state'][1] = True
            st.session_state['status'][2] = True
    
    with st.status(label="Specify the roles to create.",expanded=st.session_state['status'][2],state='complete' if st.session_state['state'][2] else 'error') as roles_container:
        
        rw_ro = st.checkbox(label="Do you need database level RO and RW roles?",key="rw_ro",help="Roles will be created as <Domain_name>_<ENV>_<RO>,<Domain_name>_<ENV>_<RW>")
        roles_list = {"role_name":[]}
        rw_ro_list = ["RW","RO"]
        # if domain_name_include:
        if rw_ro:   
            for env in env_list:
                    print("in line 373")
                    for value in rw_ro_list:
                        role_name =  domain_name.upper() + '_' + env + '_' + value 
                        roles_list["role_name"].append(role_name)
                
        else:
            role_name = domain_name.upper() 
            roles_list["role_name"].append(role_name)
        df = pd.DataFrame(roles_list)
        st.data_editor(df,num_rows="dynamic",use_container_width=True)
        st.divider()

        #Assign roles to user
        st.write("Assign roles to user")
        role_assign_user = collections.defaultdict(list)
        def render_rows():
            for index, row in enumerate(st.session_state["role_assign_user"]):
                cols = st.columns(3)
                with cols[0]:
                    row["Select_user"] = st.multiselect(label ="",options=[key for key,value in user.items()],default=None,key=f"role_assign_user_select_user_{index}",placeholder="Select the users")
                with cols[1]:
                    row["Select_role"] = st.multiselect(label ="",options=[roles_list['role_name'][i] for i in range(len(roles_list["role_name"]))],default=None,key=f"role_assign_user_select_role_{index}",placeholder="Select the roles")
                with cols[2]:
                    cl = st.columns(2)
                    with cl[0]:
                        if st.button("Add",key=f"assign_role_assign_user_{index}"):
                            add("role_assign_user",{"Select_user": "", "Select_role": ""})
                    with cl[1]:
                        if st.button("Del", key=f"delete_role_assign_user_{index}"):
                            delete("role_assign_user",index)
                            st.rerun()  # Force rerun to update the UI
                for value in row["Select_user"]:
                    role_assign_user[value].append(row["Select_role"])
                    
        

        render_rows()
       
        # print("line 298",role_assign_user,"userlist",user["temp"][2]+role_assign_user["temp"])
        
        if st.button("Save Data",disabled=st.session_state['save_button']):
            st.session_state['status'][2] = False
            roles_container.update(expanded=st.session_state['status'][2],state='complete')
            st.session_state['state'][2] = True
            st.session_state['status'][3] = True
            print("line 298",roles_list)
            snowflake_config = {
                "Snowflake": {
                    "ProjectName": project_name,
                    "user": [
                        {
                            "user_name": key,
                            "password": user[key][1],
                            "roles_to_assign": user[key][2] + role_assign_user[key][0]
                        } for key,items in user.items()
                    ],
                    "warehouse": [
                        {
                            "warehouse_name":w[0],
                            "warehouse_size":w[1],
                            "warehouse_type":w[2],
                            "initially_suspended":str(w[3])
                        } for w in warehouse
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
                    "Domains": domain_name,
                    "roles": roles_list["role_name"],
                    "assign_privileges_to_role": [
                        {
                            "object_name": (
                                "PROD" if "_PROD_" in roles_list["role_name"][i] else
                                "DEV" if "_DEV_" in roles_list["role_name"][i] else
                                "QA" if "_QA_" in roles_list["role_name"][i] else
                                "SANDBOX"
                            ),
                            "object_type": "Database",
                            "role_name": roles_list["role_name"][i] ,
                            "privilege": (
                                "usage" if "_RO" in roles_list["role_name"][i] else
                                ["usage","modify"] 
                             ) 
                        } for i in range(len(roles_list["role_name"]))
                    ],
                    "assign_role_to_user":[
                        {
                            "role_name": role_assign_user[key][0],
                            "to_user": key
                        } for key,value in role_assign_user.items() 
                    ],
                    "resource_monitor":[
                        {
                        "rm_name": rm_name,
                        "rm_frequency": rm_frequency,
                        "rm_type": rm_monitor_type,
                        "rm_notify": rm_notify,
                        "rm_notify_suspend": rm_notify_suspend,
                        "rm_notify_only": rm_notify_only,
                        "creditQuota": int(rm_creditQuota)
                    }
                    ]
                    
                }
            }

            with open("output.json", "w") as json_file:
                json.dump(snowflake_config, json_file, indent=2)

        
    with st.expander(label="Review",expanded= st.session_state['status'][3]) as review:
        with open("output.json","r") as file:
            data = json.load(file)
        st.json(data,expanded=True)

    if st.button("Generate",key="json_to_ymal",disabled=st.session_state["save_button"]):
#         st.session_state["yaml"]  = True
#         pass    
# if st.session_state["yaml"]:

        # display yaml file code 
        url = "git clone https://hiteshp__h__1334_-admin@bitbucket.org/phdata/provision_tool_test_repo.git"
        st.write("Use this URL to clone Provision Tool Repository and paste the below generated yaml code in group section files")
        st.code(url,language="git")
        st.write("warehouse.yaml")
        warehouse_yaml()
        with open("groups\\warehouse.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

        st.write("database.yaml")
        database_yaml()
        with open("groups\\database.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

        st.write("roles.yaml")
        role_yaml()
        with open("groups\\roles.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

        st.write("user.yaml")
        user_yaml()
        with open("groups\\user.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

        st.write("privileges.yaml")
        privileges_yaml()
        with open("groups\\privileges.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

        st.write("grantRole.yaml")
        grantRole_yaml()
        with open("groups\\grantRole.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

        st.write("resource_monitor.yaml")
        rm_yaml()
        with open("groups\\resource_monitor.yaml") as file:
            yaml_data = file.read()
        st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

if __name__ == '__main__':
    main()

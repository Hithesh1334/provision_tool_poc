import streamlit as st
import pandas as pd
import requests 
from pandas import read_csv
import time
import json
from yaml_convertor import warehouse_yaml
from yaml_convertor import database_yaml
from yaml_convertor import role_yaml
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
        def add_warehouse():
            st.session_state["warehouse"].append({"warehouse_name":"","warehouse_size":"","warehouse_type":"","initially_suspended":""})
        def delete_warehouse(index):
            if len(st.session_state["warehouse"]) > 1:
                st.session_state["warehouse"].pop(index)
        warehouse = []
        def render_rows():
            for index, row in enumerate(st.session_state["warehouse"]):
                cols = st.columns(5)
                with cols[0]:
                    if domain_name:
                        row["warehouse_name"] = st.text_input(
                            label=f"warehouse Name",
                            value=f"{domain_name}_Adhoc_wh",
                            placeholder=f"{domain_name}_Adhoc_wh",
                            key=f"warehouse_name_{index}"
                        )
                    else:
                        row["warehouse_name"] = st.text_input(
                            label=f"warehouse Name",
                            value=row["warehouse_name"],
                            placeholder=f"Domain_Adhoc_wh",
                            key=f"warehouse_name_{index}"
                        )
                with cols[1]:
                    row["warehouse_size"] = st.selectbox(
                        label=f"warehouse size",
                        # value=row["warehouse_size"],
                        options = ["X-Small",
                        "Small",
                        "Medium",
                        "Large",
                        "X-Large",
                        "2X-Large",
                        "3X-Large",
                        "4X-Large",
                        "5X-Large",
                        "6X-Large",],
                        placeholder="X-Small",
                        # default = "X-Small",
                        key=f"warehouse_size_{index}",
                    )
                with cols[2]:
                    row["warehouse_type"] = st.selectbox(
                        label=f"warehosue Type",
                        options=["STANDARD","SNOWPARK-OPTIMIZED"],
                        placeholder="STANDARD",
                        # default= "STANDARD",
                        key=f"warehouse_type_{index}"
                    )
                with cols[3]:
                    row["initially_suspended"] = st.selectbox(
                        label=f"initially suspended",
                        options=["True","False"],
                        # placeholder="STANDARD",
                        # default= "STANDARD",
                        key=f"initially_suspended_{index}"
                    )

                with cols[4]:
                    # option_map = {
                    #     0: "add",
                    #     1: "delete",
                    # }
                    # selection = st.segmented_control(
                    #     "",
                    #     options=option_map.keys(),
                    #     format_func=lambda option: option_map[option],
                    #     selection_mode="single",
                    #     key = f"add_warehouse_{index}"
                    # )
                    # print("in 170",selection)
                    # if selection == 0:
                    #     print("in 171")
                    #     add_warehouse()
                    # if selection == 1:
                    #     delete_warehouse(index)
                    #     st.rerun()
                    cl = st.columns(2)
                    with cl[0]:
                        if st.button("Add",key=f"add_warehouse_{index}"):
                            add_warehouse()
                    with cl[1]:
                        if st.button("Del", key=f"delete_warehouse_{index}"):
                            delete_warehouse(index)
                            st.rerun()  # Force rerun to update the UI
                warehouse.append([row["warehouse_name"],row["warehouse_size"],row["warehouse_type"],row["initially_suspended"]])
        

        render_rows()

        # warehouse_data = pd.read_json("json/warehouse.json")
        # warehouse_df = st.data_editor(warehouse_data,column_config={
        #         "warehouse_size": st.column_config.SelectboxColumn(
        #             "warehouse_size",
        #             help="The category of the app",
        #             width="medium",
        #             options=[
        #                 "X-Small",
        #                 "Small",
        #                 "Medium",
        #                 "Large",
        #                 "X-Large",
        #                 "2X-Large",
        #                 "3X-Large",
        #                 "4X-Large",
        #                 "5X-Large",
        #                 "6X-Large",
        #             ],
        #             required=True,
        #             default="X-Small"
        #         ),
        #         "warehouse_type": st.column_config.SelectboxColumn(
        #             "warehouse_type",
        #             help="The category of the app",
        #             width="medium",
        #             options=[
        #                 "SNOWPARK-OPTIMIZED",
        #                 "STANDARD",
        #             ],
        #             required=True
        #         ),
        #     },hide_index=True,use_container_width=True,num_rows="dynamic",disabled=st.session_state['warehouse_df'])
        
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

        if warehouse[0][0] and st.session_state["warehouse_spinner"]:
            with st.spinner("In progress..."):
                time.sleep(3)
            st.session_state['status'][0] = False
            st.session_state['status'][1] = True
            warehouse_container.update(expanded=st.session_state['status'][0],state="complete")
            st.session_state['state'][0] = True
            st.session_state["warehouse_spinner"] = False

    with st.status(label="Specify the users to create.",expanded=st.session_state['status'][1],state='complete' if st.session_state['state'][2] else 'error') as user_block:
        def add_row():
            st.session_state["rows"].append({"user_name": "", "password": "", "roles": []})
        def delete_row(index):
            if len(st.session_state["rows"]) > 1:
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
                    role_list = ["SYSADMIN", "SECURITYADMIN", "USERADMIN"] 
                    row["roles"] = st.multiselect(
                        label=f"Default Role",
                        options=role_list,
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

    # if project_name and warehouse_df and role_name:
    #     st.session_state["save_button"] = False
        st.divider()
        # if st.button("Next",key="roles_block_button"):
        print(user,"in line 297")
        if user[0][0] and user[0][1] and st.session_state["user_spinner"]:
            with st.spinner("In progress..."):
                time.sleep(3)
            st.session_state['status'][1] = False
            user_block.update(expanded=st.session_state['status'][1],state='complete')
            st.session_state['state'][1] = True
            st.session_state['status'][2] = True
    
    with st.status(label="Specify the roles to create.",expanded=st.session_state['status'][2],state='complete' if st.session_state['state'][1] else 'error') as roles_container:
        cols = st.columns(2)
        with cols[0]:
            input = st.radio(label = "",options=["Custom","Standard"],horizontal=True)
        if input == "Custom":
                st.divider()
                def add_role():
                    st.session_state["role"].append({"role_name":""})
                def delete_role(index):
                    if len(st.session_state["role"]) > 1:
                        st.session_state["role"].pop(index)
                role = []
                def render_rows():
                    for index, row in enumerate(st.session_state["role"]):
                        cols = st.columns(2)
                        with cols[0]:
                            row["role_name"] = st.text_input(
                                label=f"Role Name",
                                value=row["role_name"],
                                placeholder=f"domain_env_rw    ",
                                key=f"role_name_{index}"
                            )

                        with cols[1]:
                            # option_map = {
                            #     0: "add",
                            #     1: "delete",
                            # }
                            # selection = st.segmented_control(
                            #     "",
                            #     options=option_map.keys(),
                            #     format_func=lambda option: option_map[option],
                            #     selection_mode="single",
                            #     key = f"add_warehouse_{index}"
                            # )
                            # print("in 170",selection)
                            # if selection == 0:
                            #     print("in 171")
                            #     add_warehouse()
                            # if selection == 1:
                            #     delete_warehouse(index)
                            #     st.rerun()
                            cl = st.columns(2)
                            with cl[0]:
                                if st.button("Add",key=f"add_role_{index}"):
                                    add_role()
                            with cl[1]:
                                if st.button("Del", key=f"delete_role_{index}"):
                                    delete_role(index)
                                    st.rerun()  # Force rerun to update the UI
                        role.append([row["role_name"]])
                

                render_rows()
        if input == "Standard":
            st.divider()
            suffix_prefix = st.radio(label = "",options = ["Suffix","Prefix"],horizontal=True)
            domain_name_include = st.checkbox(label = "Include domain names in object names?",key="domain_radio")
            env_name_include = st.checkbox(label = "Include env names in object names?",key="env_radio")
            rw_ro = st.checkbox(label="do you want rw_ro combination as well for each role",key="rw_ro")
            roles_list = {"role_name":[]}
            rw_ro_list = ["rw","ro"]
            if domain_name_include:
                for env in env_list:
                    if rw_ro:
                        print("in line 373")
                        for value in rw_ro_list:
                            print("in line 375",value,env)
                            if suffix_prefix == "Suffix":
                                if env_name_include:
                                    role_name = value + '_' + domain_name + '_' + env
                                else:
                                    role_name = value + '_' + domain_name 
                            if suffix_prefix == "Prefix":
                                if env_name_include:
                                    role_name = env + '_' + domain_name + '_' + value
                                else:
                                    role_name = domain_name + '_' + value
                            roles_list["role_name"].append(role_name)
                    
                    else:
                        for value in rw_ro_list:
                            if suffix_prefix == "Suffix":
                                if env_name_include:
                                    role_name =   domain_name + '_' + env
                                else:
                                    role_name = domain_name 
                            if suffix_prefix == "Prefix":
                                if env_name_include:
                                    role_name = env + '_' + domain_name 
                                else:
                                    role_name = domain_name 
                    

                            roles_list["role_name"].append(role_name)
                df = pd.DataFrame(roles_list)
                st.data_editor(df,num_rows="dynamic",use_container_width=True)
        st.divider()
        
        
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
                    "roles": roles_list["role_name"]
                }
            }

            with open("output.json", "w") as json_file:
                json.dump(snowflake_config, json_file, indent=2)

        
    with st.expander(label="Review",expanded=True) as review:
        with open("output.json","r") as file:
            data = json.load(file)
        st.json(data,expanded=True)

    if st.button("Generate",key="json_to_ymal",disabled=st.session_state["save_button"]):
#         st.session_state["yaml"]  = True
#         pass    
# if st.session_state["yaml"]:
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


if __name__ == '__main__':
    main()

import streamlit as st
import json




def json_handler_fun(project_name,user,role_assign_user,warehouse,rm_name,rm_creditQuota,rm_frequency,rm_monitor_type,rm_notify,rm_notify_suspend,rm_notify_only,domain_name,env_list,roles_list,schema_list):
    # st.session_state['status'][3] = False
    # schema_container.update(expanded=st.session_state['status'][2],state='complete')
    # st.session_state['state'][3] = True
    # st.session_state['status'][4] = True
    print("line 12 in json_handler",role_assign_user )
    print("line no 13 in json_hanler ",roles_list)
    print("line no 14 in json_hanler ",user)

    snowflake_config = {
        "Snowflake": {
            "ProjectName": project_name,
            "user": [
                {
                    "user_name": key,
                    "password": user[key][1],
                    "default_roles": user[key][2],
                    "roles_to_assign": ["hh"] if len(list(user.items())) == 1 and len(role_assign_user) == 0  else user[key][2] + role_assign_user[key][0] if key in role_assign_user else []
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
            "env": [domain_name + "_" +env for env in env_list],
            "Domains": domain_name,
            "roles": roles_list["Roles"],
            "assign_privileges_to_role": [
                {
                    "object_name": (
                        domain_name + "_" +"PROD" if "_PROD" in roles_list["Roles"][i] else
                        domain_name + "_" +"DEV" if "_DEV" in roles_list["Roles"][i] else
                        domain_name + "_" +"QA" if "_QA" in roles_list["Roles"][i] else
                        domain_name + "_" + "NONPROD" if "_NONPROD" in roles_list["Roles"][i] else
                        domain_name + "_" +"SANDBOX"
                    ),
                    "object_type": "Database",
                    "roles": roles_list["Roles"][i] ,
                    "privilege": (
                        "USAGE" if "_RO" in roles_list["Roles"][i] else
                        ["ALL PRIVILEGES"] 
                        ) 
                } for i in range(len(roles_list["Roles"]))
            ],
            "assign_role_to_user":[
                {
                    "roles": role_assign_user[key][0]+user[key][2],
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
                "creditQuota": "" if not rm_creditQuota else int(rm_creditQuota)
            }
            ],
            "schema":[
                {
                    "schema_name": schema.upper(),
                    "database": database[0]
                }for schema,database in schema_list.items()
            ]
            
        }
    }

    with open("output.json", "w") as json_file:
        json.dump(snowflake_config, json_file, indent=2)

    with st.expander(label="Review Data",expanded= True) as review:
        with open("output.json","r") as file:
            data = json.load(file)
        st.json(data,expanded=True)

    
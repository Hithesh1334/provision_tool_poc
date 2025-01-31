import json
import streamlit as st

def collect_user_input():
    # Initialize the data structure
    data = {
        "Snowflake": {
            "ProjectName": "",
            "env": [],
            "user": [],
            "warehouse": [],
            "Domains": []
        }
    }

    # Collect Project Name
    st.title("Provision Tool UI")
    project_name = st.text_input("Enter the Project Name")
    if project_name:
        data["Snowflake"]["ProjectName"] = project_name

    # Collect Domains
    domains = st.multiselect(
        "Select the domains",
        options=["Marketing", "Finance", "Sales"],
        key="domains"
    )
    if domains:
        data["Snowflake"]["Domains"] = domains

    warehouse = st.text_input("Enter the waerhouses(comma-separated)",key="warehouse")
    if warehouse:
        data["Snowflake"]["warehouse"] = warehouse
 
    user = st.text_input("Enter the users(comma-separated)",key="user")
    if user:
        data["Snowflake"]["user"] = user
    # Collect Environments
    environments = st.multiselect(
        "Select the environments",
        options=["Prod", "Dev", "NonProd", "QA", "SandBox"],
        key="environments"
    )

    for env in environments:
        env_data = {
            env: [
                {
                    "database": st.text_input(f"Enter the databases for {env} (comma-separated)").split(","),
                    "schemas": [
                        {
                            db: st.text_input(f"Enter schemas for database '{db}' in {env} (comma-separated)").split(",")
                            for db in st.text_input(f"Enter the databases for schema setup in {env} (comma-separated)").split(",")
                        }
                    ],
                    "role": st.text_input(f"Enter the roles for {env} (comma-separated)").split(","),
                }
            ]
        }
        data["Snowflake"]["env"].append(env_data)

    return data

def main():
    # Collect user input
    json_data = collect_user_input()

    # Convert to JSON format
    if st.button("Generate JSON"):
        json_output = json.dumps(json_data, indent=4)

        # Save to file
        with open("snowflake_config.json", "w") as file:
            file.write(json_output)

        st.success("JSON configuration saved to 'snowflake_config.json'")
        st.json(json_output)

if __name__ == "__main__":
    main()


# if not st.session_state['updated_df'][0]:
#                 roles_data = pd.read_json("json/roles.json")
#             else:
#                 print("in line 318")
#                 roles_data = pd.read_json("json/updated_Json/updated_roles.json")
#             roles_df = st.data_editor(roles_data, use_container_width=True,num_rows="dynamic")
#             radio_value = st.checkbox(label="do you need all the combinations of env and domains?",)
#             roles_list = {"role_name":[]}
#             if radio_value :
#                 append_on = st.radio(
#                     label = "",
#                     options = ["Suffix","Prefix"],
#                     horizontal = True
#                 )
                
#                 domain_name_included = st.checkbox(label="Include domain names in object names?",key="domain_radio")               
                    
#                 envs_name_included = st.checkbox(label="Include env names in object names?",key="envs_radio")

#                 rw_ro = st.checkbox(label="do you want rw_ro combination as well for each role",)
#                 with open("json/roles.json") as file:
#                     roles_data = json.load(file)
                
#                 if domain_name_included:
#                     for role in roles_df:
#                         print(role,roles_df)
#                         for domain in domain_name:
#                             for env in env_list:
#                                 role_name = role['role_name']
#                                 if append_on == "Suffix":
#                                     if envs_name_included:
#                                         role_name = role_name + '_' + domain + '_' + env
#                                     else:
#                                         role_name = role_name + '_' + domain 
#                                 if append_on == "Prefix":
#                                     if envs_name_included:
#                                         role_name = env + '_' + domain + '_' + role_name
#                                     else:
#                                         role_name = domain + '_' + role_name

#                                 roles_list["role_name"].append(role_name)
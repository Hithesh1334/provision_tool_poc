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

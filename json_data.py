import json

def get_user_input():
    data = {
        "Snowflake": {
            "ProjectName": input("Enter the Project Name: "),
            "env": [],
            "Domains": input("Enter the domains (comma-separated): ").split(",")
        } 
    }

    environments = ["Prod", "Dev", "NonProd", "QA", "SandBox"]

    for env in environments:
        env_data = {
            env: [
                {
                    "warehouse": input(f"Enter the warehouses for {env} (comma-separated): ").split(","),
                    "database": input(f"Enter the databases for {env} (comma-separated): ").split(","),
                    "schemas": [
                        {
                            db: input(f"Enter schemas for database '{db}' in {env} (comma-separated): ").split(",")
                            for db in input(f"Enter the databases for schema setup in {env} (comma-separated): ").split(",")
                        }
                    ],
                    "role": input(f"Enter the roles for {env} (comma-separated): ").split(","),
                    "user": input(f"Enter the users for {env} (comma-separated): ").split(",")
                }
            ]
        }
        data["Snowflake"]["env"].append(env_data)

    return data

def main():
    json_data = get_user_input()

    # Convert to JSON format
    json_output = json.dumps(json_data, indent=4)
    
    # Save to file
    with open("snowflake_config.json", "w") as file:
        file.write(json_output)

    print("JSON configuration saved to 'snowflake_config.json':")
    print(json_output)

if __name__ == "__main__":
    main()

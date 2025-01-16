import pandas as pd
import yaml
import streamlit as st
import json


savepath = "groups\\"
file_path = "output.json"

def convert(file,file_name):
    # Convert the dictionary to YAML
    yaml_data = yaml.dump(file, default_flow_style=False)
    path = f"{savepath}{file_name}.yaml"
    with open(path, "w") as file:
        file.write(yaml_data)

def warehouse_yaml():
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    warehouses = []

    # Populate the list with dictionaries
    for warehouse in json_data['Snowflake']['warehouse']:
        
        temp = {
            'name': warehouse['warehouse_name'] ,
            'warehouse_size': warehouse['warehouse_size'],
            'warehouse_type': warehouse['warehouse_type'],
            'initially_suspended': warehouse['initially_suspended'],
        }
        warehouse = {}
        for key, value in temp.items():
            if value not in ('', None):
                warehouse[key] = value
        warehouses.append(warehouse)

    output_data = {'entries': warehouses}
    convert(output_data,'warehouse')

def database_yaml():
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    databases = []

    # Populate the list with dictionaries
    for database in json_data["Snowflake"]['env']:
        temp = {
            'name': database,
            }
        database = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                database[key] = value
        databases.append(database)

    output_data = {'entries': databases}
    convert(output_data,'database')
    
def user_yaml():
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    users = []

    # Populate the list with dictionaries
    for user in json_data["Snowflake"]["user"]:
        temp = {
            'name': user["user_name"],
            'password': user["password"],
            }
        user = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                user[key] = value
        users.append(user)

    output_data = {'entries': users}
    convert(output_data,'user')
    
def schema_yaml(df):
    df = pd.DataFrame(df)
    schemas = []

    # Populate the list with dictionaries
    for index, row in df.iterrows():
        temp = {
            'name': row['schema_name'],
            'database' : row['Database_name'],
            }
        schema = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                schema[key] = value
        schemas.append(schema)

    output_data = {'entries': schemas}
    convert(output_data,'schema')

def rm_yaml():
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    rms = []

    # Populate the list with dictionaries
    for rm in json_data["Snowflake"]["resource_monitor"]:
        temp = {
            'name': rm["rm_name"],
            # 'creditQuota': rm['creditQuota'],
            'frequency': rm['rm_frequency'],
            
            }
        rm = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                rm[key] = value
        rms.append(rm)

    output_data = {'entries': rms}
    convert(output_data,'resource_monitor')

def role_yaml():
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    roles = []

    # Populate the list with dictionaries
    for role in json_data["Snowflake"]["roles"]:
        temp = {
            'name': role,
            }
        role = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                role[key] = value
        roles.append(role)

    output_data = {'entries': roles}
    convert(output_data,'roles')

def privileges_yaml():
    with open(file_path, 'r') as file:
            json_data = json.load(file)
    privileges = []

    # Populate the list with dictionaries
    for p in json_data["Snowflake"]["assign_privileges_to_role"]:
        temp = {
            'privilege_name': p['privilege'],
            'objectType': p['object_type'],
            'objectName': p['object_name'],
            'roleName': p['role_name'],
            }
        privilege = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                privilege[key] = value
        privileges.append(privilege)

    output_data = {'entries': privileges}
    convert(output_data,'privileges')

def grantRole_yaml():
    with open(file_path, 'r') as file:
            json_data = json.load(file)
    grantRoles = []
    
    # Populate the list with dictionaries
    for g in json_data["Snowflake"]["assign_role_to_user"]:
        for role_name in g["role_name"]:
            temp = {
                'name': role_name,
                # 'toRoles': ['RoleToAssign'],
                'toUsers': g['to_user'],
                } 
            grantRole = {}
            for key,value in temp.items():
                if temp[key] != '' and temp[key] != None and temp[key] != None:
                    grantRole[key] = value
            grantRoles.append(grantRole)

    output_data = {'entries': grantRoles}
    convert(output_data,'grantRole')

def file_format_yaml(df):
    df = pd.DataFrame(df)
    file_formats = []
    
    # Populate the list with dictionaries
    for index, row in df.iterrows():
        temp = {
            'name': row['name'],
            'database' : row['database'],
            'schema' : row['schema'],
            'compression': row['compression'],
            'allow_duplicate': row['allow_duplicate'],
            'date_format': row['date_format'],
            'time_format': row['time_format'],
            'timestamp_format': row['timestamp_format'],
            'trim_space': row['trim_space'],
            'enable_octal': row['enable_octal'],
            'ignore_utf8_errors': row['ignore_utf8_errors'],
            'skip_byte_order_mark': row['skip_byte_order_mark'],
            'strip_outer_array': row['strip_outer_array'],
            'fileType' : row['fileType'],
            'binary_format': row['binary_format']
            }
        file_format = {}
        for key,value in temp.items():
            if temp[key] != '' and temp[key] != None and temp[key] != None:
                file_format[key] = value
        file_formats.append(file_format)

    output_data = {'entries': file_formats}
    convert(output_data,'fileFormats')
    


if __name__ == '__main__':
    pass
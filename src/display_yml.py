import streamlit as st
import pandas as pd
import requests 
import os
from pandas import read_csv
import time
import json
import yaml
import collections
import zipfile

from src.yaml_convertor import warehouse_yaml
from src.yaml_convertor import database_yaml
from src.yaml_convertor import role_yaml
from src.yaml_convertor import user_yaml
from src.yaml_convertor import  privileges_yaml
from src.yaml_convertor import grantRole_yaml
from src.yaml_convertor import rm_yaml
from src.yaml_convertor import schema_yaml
from src.create_zip import create_zip_fun

def display_yml_fun():
    url = "https://bitbucket.org/phdata/provision_tool_test_repo/src/master/"
    st.write("check out this [provision tool repository](%s)" % url)
    # st.markdown("check out this [link](%s)" % url)
    url = "git clone https://hiteshp__h__1334_-admin@bitbucket.org/phdata/provision_tool_test_repo.git"
    st.caption("Note: Use the below command to clone Provision Tool Repository and paste the below generated yaml code in group section files")
    st.code(url,language="git")
    st.write("warehouse.yml")
    warehouse_yaml()
    with open("groups\\warehouse.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    st.write("database.yml")
    database_yaml()
    with open("groups\\database.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    st.write("roles.yml")
    role_yaml()
    with open("groups\\roles.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    st.write("user.yml")
    user_yaml()
    with open("groups\\user.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    st.write("privileges.yml")
    privileges_yaml()
    with open("groups\\privileges.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    st.write("grantRole.yml")
    grantRole_yaml()
    with open("groups\\grantRole.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    st.write("resource_monitor.yml")
    rm_yaml()
    with open("groups\\resource_monitor.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)
    
    st.write("schema.yml")
    schema_yaml()
    with open("groups\\schema.yaml") as file:
        yaml_data = file.read()
    st.code(yaml_data,language='yaml',wrap_lines=True,line_numbers=True)

    zip_buffer = create_zip_fun("groups")

    # Provide a download button
    st.download_button(
        label="Download files",
        data=zip_buffer,
        file_name="groups.zip",
        mime="application/zip",
    )
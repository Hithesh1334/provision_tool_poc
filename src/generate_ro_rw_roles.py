
import streamlit as st
import pandas as pd

def gen_ro_rw(df):
    role_list = {"Roles": []}

    for index , row in df.iterrows():
        role_name = ""
        if row["Read-Only"] and not row["Read-Write"]:
            role_name = row["Roles"] + "_" + "RO"
            role_list["Roles"].append(role_name)
        elif not row["Read-Only"] and row["Read-Write"]:
            role_name = row["Roles"] + "_" + "RW"
            role_list["Roles"].append(role_name)
        elif row["Read-Only"] and  row["Read-Write"]:
            role_name = row["Roles"] + "_" + "RO"
            role_list["Roles"].append(role_name)
            role_name = row["Roles"] + "_" + "RW"
            role_list["Roles"].append(role_name)
    
    return role_list
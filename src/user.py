

import streamlit as st
from pandas import read_csv
import collections
from src.add_new_row import add
from src.add_new_row import delete



def user_fun():
    user = collections.defaultdict(list)
    st.markdown(f'<p id="env_comment">Tip : System defined roles can be selected as per the requirements here. If role is not mentioned , by default , public role will be assigned to the user. <br> Please note , it is required to follow snowflake password policies and passwords will be visible in YML file.', unsafe_allow_html=True)
    def render_rows():
        for index, row in enumerate(st.session_state["rows"]):
            cols = st.columns(4)
            with cols[0]:
                st.markdown(f'<p id="subheading_tag">User Name</p>', unsafe_allow_html=True)
                row["user_name"] = st.text_input(
                    label=f"",
                    value=row["user_name"],
                    placeholder=" ",
                    key=f"user_name_{index}", label_visibility="collapsed"
                )
            with cols[1]:
                st.markdown(f'<p id="subheading_tag">Password</p>', unsafe_allow_html=True)
                row["password"] = st.text_input(
                    label=f"",
                    value=row["password"],
                    placeholder="Temp#@123",
                    key=f"password_{index}",
                    type="password",
                    help = "Note: Password should be of 12 charecter lenght, First letter should be capital and should contain special charecter as well example: 'TLhhoK$$9ZuI7#77#' ", label_visibility="collapsed"
                )
            with cols[2]:
                st.markdown(f'<p id="subheading_tag">System Defined Roles</p>', unsafe_allow_html=True)
                role_list = ["SYSADMIN", "SECURITYADMIN", "USERADMIN","ACCOUNTADMIN","PUBLIC"] 
                row["Roles"] = st.multiselect(
                    label=f"",
                    options=role_list,
                    key=f"roles_{index}", label_visibility="collapsed"
                    
                )

            with cols[3]:
                cl = st.columns(3)
                with cl[0]:
                    if st.button("Add",key=f"add_{index}",use_container_width=True):
                        add("rows",{"user_name": "", "password": "", "roles": []})
                with cl[1]:
                    if st.button("Delete", key=f"delete_{index}",use_container_width=True):
                        delete("rows",index)
                        st.rerun()  # Force rerun to update the UI
            user[row['user_name']].append(row["user_name"])
            user[row['user_name']].append(row["password"])
            user[row['user_name']].append(row["Roles"])
    

    render_rows()
    
    st.divider()
    
    

    return user

import streamlit as st
from pandas import read_csv
import collections
from src.add_new_row import add
from src.add_new_row import delete


def assign_role_to_roles_fun(roles_list):
    #Assign roles to user
    st.markdown(f'<p id="env_comment">Tip : Multiple users can be assigned to multiple roles and vice a versa. Be causious while assigning "Read-Write" roles to any user as it assigns all the permissions to the user.</p>', unsafe_allow_html=True)
    # st.markdown(f'<p id="subheading_tag">Assign roles to user</p>', unsafe_allow_html=True)
    role_assign_roles = collections.defaultdict(list)
    def render_rows():
        for index, row in enumerate(st.session_state["role_assign_roles"]):
            cols = st.columns(4)
            with cols[0]:
                row["Select_role"] = st.multiselect(label ="",options=[roles_list['Roles'][i] for i in range(len(roles_list["Roles"]))],default=None,key=f"role_assign_roles_select_role_{index}",placeholder="Select the roles")
            with cols[1]:
                row["Select_role_to_assign"] = st.multiselect(label ="",options=[roles_list['Roles'][i] for i in range(len(roles_list["Roles"]))],default=None,key=f"role_assign_roles_select_role_to_assign_{index}",placeholder="Select the roles to assign")
            with cols[2]:
                cl = st.columns(2)
                with cl[0]:
                    if st.button("Add",key=f"assign_role_assign_roles_{index}",use_container_width=True):
                        add("role_assign_roles",{"Select_role": "", "Select_role_to_assign": ""})
                with cl[1]:
                    if st.button("Delete", key=f"delete_role_assign_roles_{index}",use_container_width=True):
                        delete("role_assign_roles",index)
                        st.rerun()  # Force rerun to update the UI
            for value in row["Select_role"]:
                role_assign_roles[value].append(row["Select_role_to_assign"])
                
    
    
    render_rows()

    st.divider()
    return role_assign_roles

import streamlit as st
import pandas as pd

def roles_fun(env_list):
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f'<p id="label_tag">Role Name</p>', unsafe_allow_html=True)
        init_roles = st.text_input(label="",placeholder=" ",key = "roles",label_visibility="collapsed")
        init_roles = init_roles.replace(" ","")
    rw_ro = st.checkbox(label="Do you need database level Read-Only(RO) and Read-Write(RW) roles ?",key="rw_ro",help="Roles will be created as <Domain_name>_<ENV>_<RO>,<Domain_name>_<ENV>_<RW>")
    roles_list = {"Roles":[]}
    rw_ro_list = ["RW","RO"]
    # if domain_name_include:
    if rw_ro:   
        for env in env_list:
                # print("in line 373")
                # for value in rw_ro_list:
                    if init_roles:
                        roles = init_roles + '_' + env 
                    else:
                        roles =   '_' + env + '_'  
                    roles_list["Roles"].append(roles.upper())
        df = pd.DataFrame(roles_list)
        df['Read Only'] = False
        df['Read Write'] = False
        
        st.session_state['df'] = df
        print(st.session_state['df'],"line number 29 in roles.py")
        edited_df = st.data_editor(st.session_state['df'],num_rows="dynamic",use_container_width=True)

        # for index, row in edited_df.iterrows():
        #     ro = row["RO"]
        #     rw = row["RW"]
        #     role = row["Roles"]
        #     if ro:
        #          role = role + "_" + 'RO'
        #     if rw:
        #          role = role + "_" + 'RW'
            
        #     edited_df.at[index,"Roles"] = role 
        #     print(edited_df,"line 42 in roles.py")
        # st.session_state["df"] = edited_df
        # # st.rerun()
        # print(st.session_state["df"],"in line 45 roles.oy")

    else:
        roles_list["Roles"].append(init_roles)
    # else:
    #     # roles = domain_name.upper() 
    #     init_roles = (init_roles.replace(" ","")).upper()
    #     roles_list["Roles"].append(init_roles)
    st.divider()


    return (init_roles,roles_list,rw_ro)
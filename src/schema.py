import streamlit as st
import collections
from src.add_new_row import add
from src.add_new_row import delete


def schema_fun(domain_name):

    env_list = []
    st.session_state['envs'] = False

    comment_content= "Environment name will be used to generate the database name along with domain specified in step1. Format : <DOMAIN>_<ENV> , Example : MARKETING_PROD"
    st.markdown(f'<p id="env_comment">Tip: {comment_content}</p>', unsafe_allow_html=True)
    st.markdown(f'<p id="label_tag">Select Environments</p>', unsafe_allow_html=True)
    
    prod = st.checkbox(label="PROD",disabled= st.session_state['envs'])
    dev = st.checkbox(label="DEV",disabled= st.session_state['envs'])
    qa = st.checkbox(label="QA",disabled= st.session_state['envs'])
    nonprod = st.checkbox(label="NONPROD",disabled= st.session_state['envs'])
    sandbox = st.checkbox(label="SANDBOX",disabled= st.session_state['envs'])

    if prod:
        env_list.append("PROD")
    if dev:
        env_list.append("DEV")
    if qa:
        env_list.append("QA")
    if nonprod:
        env_list.append("NONPROD")
    if sandbox:
        env_list.append("SANDBOX")
    
    st.divider()
    st.markdown(f'<p id="env_comment">Tip: It is recommednded to add _SCH after schema name to make the object identifiable</p>', unsafe_allow_html=True)
    schema_list = collections.defaultdict(list)
    def render_rows():
        for index, row in enumerate(st.session_state["schemas"]):
            cols = st.columns(3)
            with cols[0]:
                st.markdown(f'<p id="subheading_tag">Schema Name</p>', unsafe_allow_html=True)
                row["Schema_name"] = st.text_input(label="",placeholder="",key=f"schema_name_{index}",label_visibility="collapsed")
            with cols[1]:
                st.markdown(f'<p id="subheading_tag">Database</p>', unsafe_allow_html=True)
                row["Database_name"] = st.multiselect(label ="",options=[domain_name + "_"+env_list[i] for i in range(len(env_list))],default=None,key=f"schema_database_{index}",placeholder="",label_visibility="collapsed")
            with cols[2]:
                cl = st.columns(3)
                with cl[0]:
                    if st.button("Add",key=f"add_schema_{index}",use_container_width=True):
                        add("schemas",{"Scheam_name": "", "Database_name": []})
                with cl[1]:
                    if st.button("Delete", key=f"delete_schema_{index}",use_container_width=True):
                        delete("schemas",index)
                        st.rerun()  # Force rerun to update the UI
            
            schema_list[row["Schema_name"]].append(row["Database_name"])
                
    

    render_rows()
    st.divider()

    return (schema_list,env_list)
import streamlit as st
import collections
from src.add_new_row import add
from src.add_new_row import delete


def schema_fun(domain_name,env_list):
    schema_list = collections.defaultdict(list)
    def render_rows():
        for index, row in enumerate(st.session_state["schemas"]):
            cols = st.columns(4)
            with cols[0]:
                st.markdown(f'<p id="label_tag">Schema Name</p>', unsafe_allow_html=True)
                row["Schema_name"] = st.text_input(label="",placeholder="",key=f"schema_name_{index}",label_visibility="collapsed")
            with cols[1]:
                st.markdown(f'<p id="label_tag">Database</p>', unsafe_allow_html=True)
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

    return schema_list
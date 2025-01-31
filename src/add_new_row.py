import streamlit as st


def add(resource,value):
            st.session_state[f"{resource}"].append(value)
def delete(resource,index):
    if len(st.session_state[f"{resource}"]) > 1:
        st.session_state[f"{resource}"].pop(index)

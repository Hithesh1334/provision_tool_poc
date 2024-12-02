import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import requests 
from pandas import read_csv

# URL to the sample CSV file 
sample_warehouse_CSV_URL = "https://docs.google.com/spreadsheets/d/1HiXz3-_u6Qlxb_zKlmjrMoFgu-KaBvH1V-pbao5O9T0/edit?usp=drive_link"
sample_databse_CSV_URL = "https://docs.google.com/spreadsheets/d/1ekKAP6Ibo53-YN0J9WxXlwumifE_uDIkYrXx32w_nTI/edit?usp=drive_link"
sample_schema_CSV_URL = "https://docs.google.com/spreadsheets/d/1Gp9RVVhITQpvxxO2c2gq2FoW-X29qWnx0VVPbIaXxN8/edit?usp=drive_link"
sample_user_CSV_URL = "https://docs.google.com/spreadsheets/d/1Tnx-ZlXUDfiyMwqwLWOqsTSwuBAb_2EUjMJyc3iYEgg/edit?usp=drive_link"
sample_rm_CSV_URL = "https://docs.google.com/spreadsheets/d/1HiXz3-_u6Qlxb_zKlmjrMoFgu-KaBvH1V-pbao5O9T0/edit?usp=drive_link"


def download_sample_csv():
    pass
    #dummy code // need to fix the downlaod
    download_url = sample_warehouse_CSV_URL + "&export=download"
    session = requests.Session()
    response = requests.get(sample_warehouse_CSV_URL)
    response.raise_for_status() 
    if "confirm" in response.url:
        token = response.url.split("confirm=")[1]
        download_url = f"{sample_warehouse_CSV_URL}&confirm={token}&export=download"
        response = session.get(download_url, stream=True)
    response.raise_for_status() 
    return response.content

def display_editable_dataframe(df):
    #display the dataframe table 
    st.write("Edit the DataFrame:")
    edited_df = st.data_editor(df, use_container_width=True,num_rows="dynamic")
    return edited_df

def display_download_upload():
    #display the download and upload options
    cols=st.columns(2)
    with cols[0]:
        csv_content = download_sample_csv()
        st.download_button(
            label="Download Sample CSV",
            data=csv_content,
            file_name="sample_warehouse.csv",
            mime="application/octet-stream"
        )
    with cols[1]:
        uploaded_file = st.file_uploader("Upload your CSV file here:", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write("Uploaded CSV File Preview:")
            st.dataframe(df)

def main():
    with st.sidebar:
        selected = option_menu(
            "Main menu", 
            ["Home", "Warehouse Entry", "Database Entry", "User Entry", "Roles Entry", "Schema Entry", "Resource Monitor Entry"], 
            icons=["bi bi-house", "bi bi-cloud-plus", "bi bi-database-fill", "bi bi-people-fill", "bi bi-person-badge-fill", "bi bi-shield-fill-check", "bi bi-display-fill"], 
            menu_icon="cast", 
            default_index=0
        )
        
    if selected == "Home":
        st.subheader("User-friendly Provision Tool")
        
    elif selected == "Warehouse Entry":
        st.header("Enter Warehouse Details")
        display_download_upload()
        df = pd.read_json("resources\\warehouse.json")
        # Display the editable dataframe
        display_editable_dataframe(df)
        
    elif selected == "Database Entry":
        st.header("Enter Warehouse Details")
        display_download_upload()
        df = pd.read_json("resources\\database.json")
        # Display the editable dataframe
        display_editable_dataframe(df)
        
    elif selected == "User Entry":
        st.header("Enter Warehouse Details")
        display_download_upload()
        df = pd.read_json("resources\\user.json")
        # Display the editable dataframe
        display_editable_dataframe(df)
        
    elif selected == "Roles Entry":
        st.header("Enter Warehouse Details")
        display_download_upload()
        df = pd.read_json("resources\\roles.json")
        # Display the editable dataframe
        display_editable_dataframe(df)
        
    elif selected == "Schema Entry":
        st.header("Enter Schema Details")
        display_download_upload()
        df = pd.read_json("resources\\schema.json")
        # Display the editable dataframe
        display_editable_dataframe(df)
        
    elif selected == "Resource Monitor Entry":
        st.header("Enter Resource Monitor Details")
        display_download_upload()
        df = pd.read_json("resources\\resource_monitor.json")
        # Display the editable dataframe
        display_editable_dataframe(df)
        
if __name__ == '__main__':
    main()

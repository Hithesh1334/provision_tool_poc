
import streamlit as st
from pandas import read_csv
from src.add_new_row import add
from src.add_new_row import delete

def warehouse_fun(domain_name):
    warehouse = []
    st.markdown("<p id='env_comment'>By default , Adhoc warehouse will be created based on domain name given.You can also add more warehouses if required. It is recommednded to suffix warehouse name with _WH for consistency.</p>",unsafe_allow_html=True)
    def render_rows():
        for index, row in enumerate(st.session_state["warehouse"]):
            cols = st.columns(5)
            with cols[0]:
                if domain_name:
                    st.markdown(f'<p id="subheading_tag">Warehouse Name</p>', unsafe_allow_html=True)
                    row["warehouse_name"] = st.text_input(
                        label="",
                        value=(f"{domain_name}_Adhoc_wh").upper(),
                        placeholder=(f"{domain_name}_Adhoc_wh").upper(),
                        key=f"warehouse_name_{index}",label_visibility="collapsed"
                    )
                else:
                    st.markdown(f'<p id="subheading_tag">Warehouse Name</p>', unsafe_allow_html=True)
                    row["warehouse_name"] = st.text_input(
                        label=f"",
                        value=row["warehouse_name"],
                        placeholder=f"Domain_Adhoc_wh",
                        key=f"warehouse_name_{index}",label_visibility="collapsed"
                    )
            with cols[1]:
                st.markdown(f'<p id="subheading_tag">Warehouse Size</p>', unsafe_allow_html=True)
                row["warehouse_size"] = st.selectbox(
                    label=f"",
                    # value=row["warehouse_size"],
                    options = ["X-Small","Small","Medium","Large","X-Large","2X-Large","3X-Large","4X-Large","5X-Large","6X-Large",],
                    placeholder="X-Small",
                    key=f"warehouse_size_{index}",label_visibility="collapsed"
                )
            with cols[2]:
                st.markdown(f'<p id="subheading_tag">Warehouse Type</p>', unsafe_allow_html=True)
                row["warehouse_type"] = st.selectbox(
                    label=f"",
                    options=["STANDARD","SNOWPARK-OPTIMIZED"],
                    placeholder="STANDARD",
                    # default= "STANDARD",
                    key=f"warehouse_type_{index}",label_visibility='collapsed'
                )
            with cols[3]:
                st.markdown(f'<p id="subheading_tag">Initially Suspended</p>', unsafe_allow_html=True)
                row["initially_suspended"] = st.selectbox(
                    label=f"",
                    options=["True","False"],
                    key=f"initially_suspended_{index}", label_visibility="collapsed"
                )
            with cols[4]:
                cl = st.columns(2)
                with cl[0]:
                    if st.button("Add",key=f"add_warehouse_{index}",use_container_width=True):
                        add("warehouse",{"warehouse_name":"","warehouse_size":"","warehouse_type":"","initially_suspended":""})
                with cl[1]:
                    if st.button("Delete", key=f"delete_warehouse_{index}",use_container_width=True):
                        delete("warehouse",index)
                        st.rerun()  # Force rerun to update the UI
            warehouse.append([row["warehouse_name"],row["warehouse_size"],row["warehouse_type"],row["initially_suspended"]])
    

    render_rows()

    
    # resource monitor
    rm_required = st.checkbox(label="Do you need resource monitor?")
    rm_name,rm_monitor_type,rm_frequency,rm_notify,rm_notify_suspend,rm_notify_only= "","","","","",""
    rm_creditQuota = ""
    if rm_required:
        st.markdown(f'<p id="subheading_tag">Resource Monitor Name</p>', unsafe_allow_html=True) 
        rm_name = st.text_input(label = "",placeholder=" ",value="LOAD_MONITOR",key="resource_monitor",label_visibility="collapsed")
        st.markdown(f'<p id="subheading_tag">Monitor Type</p>', unsafe_allow_html=True)
        rm_monitor_type = st.radio(label = "",options=['Account','Warehouse'],key="monitor_type",label_visibility="collapsed")
        st.markdown(f'<p id="subheading_tag">CreditQuota</p>', unsafe_allow_html=True)
        st.markdown("<p id='env_comment'>CreditQuota values should be in positive number e.g., 10,15 or 20 etc</p>",unsafe_allow_html=True)
        rm_creditQuota = st.text_input(label= "",placeholder=" ",key="creditQuota",help="Example: creaditQuota = 10",label_visibility="collapsed")
        if rm_monitor_type == 'Warehouse':
            st.write("write here warehouse multiselector code")
        st.markdown(f'<p id="subheading_tag">What should be the frequency of resource monitor</p>', unsafe_allow_html=True)
        rm_frequency = st.radio(label="",options=['Daily','Weekly','Monthly','Yearly'],label_visibility="collapsed")
        st.markdown(f'<p id="subheading_tag">Select the below optinos of how would you like to be notifyed</p>', unsafe_allow_html=True)
        rm_notify = st.checkbox(label = "Notify at 70%")
        rm_notify_suspend = st.checkbox(label = "Notify and suspend at 85%")
        rm_notify_only = st.checkbox(label = "Notify at 95%")

    st.divider()
    
    # if warehouse[0][0] and st.session_state["warehouse_spinner"]:
    #     with st.spinner("In Progress..."):
    #         time.sleep(5)
    #     if rm_required:
    #         if rm_name and rm_creditQuota:
    #             # with st.spinner("In Progress..."):
    #             #     time.sleep(5)
    #             st.session_state['status'][0] = False
    #             st.session_state['status'][1] = True
    #             warehouse_container.update(expanded=st.session_state['status'][0],state="complete")
    #             st.session_state['state'][0] = True
    #             st.session_state["warehouse_spinner"] = False
    #     else:
    #         st.session_state['status'][0] = False
    #         st.session_state['status'][1] = True
    #         warehouse_container.update(expanded=st.session_state['status'][0],state="complete")
    #         st.session_state['state'][0] = True
    #         st.session_state["warehouse_spinner"] = False

    return (warehouse,rm_name,rm_creditQuota,rm_frequency,rm_monitor_type,rm_notify,rm_notify_suspend,rm_notify_only)


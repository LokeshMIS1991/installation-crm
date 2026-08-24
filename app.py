import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Installation CRM", layout="wide", page_icon="🛠️")

st.title("🛠️ Installation CRM")

# Navigation Tabs
tab1, tab2 = st.tabs(["📝 New Entry Form", "📊 View & Update Requests"])

# --- TAB 1: NEW ENTRY FORM ---
with tab1:
    st.subheader("Supervisor Data Entry Form")
    with st.form("crm_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            req_type = st.selectbox("Reason or Type*", ["Installation", "Complaint", "Repairing"])
            client_id = st.text_input("Client ID*")
        with col2:
            complaint_date = st.date_input("Complaint / Request Date", datetime.now())
            client_name = st.text_input("Client Name*")
        with col3:
            company_name = st.text_input("Company Name")
            contact_number = st.text_input("Contact Number*")

        st.markdown("---")
        col4, col5 = st.columns(2)
        with col4:
            product_details = st.text_input("Product Suggested / Type", placeholder="e.g. CCTV, Purifier, Model A")
        with col5:
            location = st.text_area("Location / Address", height=68)

        st.markdown("---")
        col6, col7 = st.columns(2)
        with col6:
            installer_name = st.text_input("Installer Name")
        with col7:
            helper_name = st.text_input("Helper Name")

        st.markdown("---")
        col8, col9, col10, col11 = st.columns(4)
        with col8:
            status = st.selectbox("Status*", ["Running", "Done", "Hold"])
        with col9:
            start_date = st.date_input("Start Date", datetime.now())
        with col10:
            end_date = st.date_input("End Date", datetime.now())
        with col11:
            deliver_date = st.date_input("Deliver Date", datetime.now())

        remarks = st.text_area("Remarks / Notes")

        submit_btn = st.form_submit_button("Submit Data")

    if submit_btn:
        if not client_id or not client_name or not contact_number:
            st.error("⚠️ Please fill required fields: Client ID, Client Name, and Contact Number!")
        else:
            st.success(f"✅ Entry saved successfully for {client_name} ({client_id})!")

# --- TAB 2: VIEW & SEARCH DATA (Dummy Layout for Team Review) ---
with tab2:
    st.subheader("Live Status Dashboard")
    st.info("Yeh Section Google Sheet integration ke baad real-time update dikhayega.")
    
    # Sample Table Layout for Supervisor Preview
    dummy_data = pd.DataFrame([
        {
            "Client ID": "C-101",
            "Client Name": "Rajesh Kumar",
            "Type": "Installation",
            "Status": "Running",
            "Installer": "Amit Sharma",
            "Location": "Delhi"
        },
        {
            "Client ID": "C-102",
            "Client Name": "Global Tech",
            "Type": "Complaint",
            "Status": "Done",
            "Installer": "Vikas Verma",
            "Location": "Noida"
        }
    ])
    st.dataframe(dummy_data, use_container_width=True)
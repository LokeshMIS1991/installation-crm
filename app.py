import streamlit as st
import pandas as pd
from datetime import datetime
import random
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Installation CRM", layout="wide", page_icon="🛠️")

# --- GOOGLE SHEETS CONNECTION ---
SHEET_NAME = "Installation_CRM"

@st.cache_resource
def get_gspread_client():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scopes
    )
    return gspread.authorize(credentials)

def load_data():
    try:
        gc = get_gspread_client()
        sh = gc.open(SHEET_NAME)
        worksheet = sh.worksheet("Sheet1")
        records = worksheet.get_all_records()
        df = pd.DataFrame(records)
        return worksheet, df
    except Exception as e:
        st.error(f"❌ Google Sheet Connection Error: {e}")
        return None, pd.DataFrame()

worksheet, crm_df = load_data()

# --- PRODUCT LIST FROM IMAGE ---
PRODUCT_LIST = [
    "Automatic Rolling Shutters", "Dock Leveller", "Dock Shelter", "High-Speed Roll Up Door",
    "High-Speed Fold Up Door", "High-Speed Self Repairable Door", "Residential Sectional Doors",
    "Industrial Sectional Door", "Hermetic Doors", "Fire Exit Door", "Auto Sliding Door",
    "Motorised Swing Gates", "Motorised Sliding Gates", "Retractable Gates", "Boom Barriers",
    "Strong Life Shutter Motor", "Manual Shutters", "Wind Shutters", "Spare Part",
    "Service Charge", "Sensor / Automatic Glass Door", "Motors", "Dock Bumper",
    "Dock Edge", "Overhead Sectional Door", "Gate", "Tank Door Shutter", "Gear Shutter",
    "General purpose Doors", "Hanger Door", "Impact Barrier", "Manual Swing Gate",
    "Manual Sliding Gate", "Other"
]

# --- INDIA STATES LIST ---
INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Other"
]

st.title("🛠️ Installation CRM")

# Navigation Tabs
tab_dash, tab_entry, tab_update = st.tabs(["📊 Dashboard", "📝 New Request Entry", "🔄 Edit & Update Request"])

# ==========================================
# --- TAB 1: EXECUTIVE DASHBOARD ---
# ==========================================
with tab_dash:
    st.subheader("📌 Performance Overview")
    df = crm_df
    
    if not df.empty and "Status" in df.columns:
        total_entries = len(df)
        running_count = len(df[df["Status"] == "Running"])
        hold_count = len(df[df["Status"] == "Hold"])
        done_count = len(df[df["Status"] == "Done"])
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("📋 Total Requests", total_entries)
        col_m2.metric("🔄 Running", running_count)
        col_m3.metric("⏸️ On Hold", hold_count)
        col_m4.metric("✅ Completed (Done)", done_count)
        
        st.markdown("---")
        
        col_d1, col_d2 = st.columns([2, 1])
        with col_d1:
            st.subheader("📋 All Registered Service Requests")
            st.dataframe(df, use_container_width=True)
            
        with col_d2:
            st.subheader("📊 Request Types")
            if "Type" in df.columns:
                type_counts = df["Type"].value_counts()
                st.bar_chart(type_counts)
    else:
        st.info("No records found in Google Sheet. Please register a new entry.")

# ==========================================
# --- TAB 2: NEW REQUEST ENTRY ---
# ==========================================
with tab_entry:
    st.subheader("📝 Register New Installation or Complaint")
    
    # Short Client ID Format (e.g. CL-4821)
    generated_client_id = f"CL-{random.randint(1000, 9999)}"
    
    with st.form("crm_form", clear_on_submit=True):
        st.info(f"🆔 **Auto-Generated Client ID:** `{generated_client_id}`")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            req_type = st.selectbox("Reason or Type*", ["Installation", "Complaint", "Repairing"])
            complaint_date = st.date_input("Complaint / Request Date", datetime.now())
        with col2:
            client_name = st.text_input("Client Name*")
            company_name = st.text_input("Company Name")
        with col3:
            contact_number = st.text_input("Contact Number*")
            product_details = st.selectbox("Product Name*", PRODUCT_LIST)

        st.markdown("---")
        st.subheader("📍 Location Details")
        col_st, col_ct, col_addr = st.columns(3)
        with col_st:
            state_selected = st.selectbox("State*", INDIAN_STATES)
        with col_ct:
            city_input = st.text_input("City Name*", placeholder="Enter City Manually")
        with col_addr:
            address = st.text_area("Specific Address", height=68, placeholder="Street, Landmark, Pincode...")

        st.markdown("---")
        st.subheader("👨‍🔧 Team Assignment & Initial Status")
        col6, col7, col8 = st.columns(3)
        with col6:
            installer_name = st.text_input("Installer Name")
        with col7:
            helper_name = st.text_input("Helper Name")
        with col8:
            status = st.selectbox("Status*", ["Running", "Hold", "Done"])

        col9, col10, col11 = st.columns(3)
        with col9:
            start_date = st.date_input("Start Date", datetime.now())
        with col10:
            end_date = st.date_input("End Date", datetime.now())
        with col11:
            deliver_date = st.date_input("Deliver Date", datetime.now())

        remarks = st.text_area("Remarks / Initial Notes")
        submit_btn = st.form_submit_button("Submit Request")

    if submit_btn:
        if not client_name or not contact_number or not city_input:
            st.error("⚠️ Please fill in all required fields: Client Name, Contact Number, and City.")
        else:
            new_row = [
                generated_client_id,
                str(complaint_date),
                client_name,
                company_name,
                contact_number,
                req_type,
                product_details,
                state_selected,
                city_input,
                address,
                installer_name,
                helper_name,
                status,
                str(start_date),
                str(end_date),
                str(deliver_date),
                remarks
            ]
            try:
                worksheet.append_row(new_row)
                st.success(f"✅ Record successfully saved! Client ID: {generated_client_id}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to save entry to Google Sheet: {e}")

    # --- TOP 10 LATEST ENTRIES SECTION ---
    st.markdown("---")
    st.subheader("📑 Top 10 Recent Registrations")
    if not crm_df.empty:
        top_10_df = crm_df.tail(10).iloc[::-1]  # Show latest entries first
        st.dataframe(top_10_df, use_container_width=True)
    else:
        st.info("No registrations recorded yet.")

# ==========================================
# --- TAB 3: EDIT & UPDATE REQUEST ---
# ==========================================
with tab_update:
    st.subheader("🔄 Edit Any Entry & Live Update Tracking")
    
    if not crm_df.empty and "Client ID" in crm_df.columns:
        client_list = crm_df["Client ID"].astype(str).tolist()
        selected_client_id = st.selectbox("Select Client ID to Edit/Update:", client_list)
        
        matching_rows = crm_df[crm_df["Client ID"].astype(str) == selected_client_id]
        
        if not matching_rows.empty:
            record_idx = matching_rows.index[0]
            selected_row = crm_df.loc[record_idx]
            sheet_row_num = record_idx + 2  # Pandas 0 index = Sheet Row 2
            
            st.markdown("---")
            st.subheader(f"✏️ Editing Details for: {selected_row.get('Client Name', '')} (`{selected_client_id}`)")
            
            with st.form("full_edit_form"):
                col_e1, col_e2, col_e3 = st.columns(3)
                with col_e1:
                    e_client_name = st.text_input("Client Name", value=str(selected_row.get("Client Name", "")))
                    e_company_name = st.text_input("Company Name", value=str(selected_row.get("Company Name", "")))
                    e_contact = st.text_input("Contact Number", value=str(selected_row.get("Contact Number", "")))
                with col_e2:
                    curr_prod = str(selected_row.get("Product", ""))
                    p_idx = PRODUCT_LIST.index(curr_prod) if curr_prod in PRODUCT_LIST else 0
                    e_product = st.selectbox("Product Name", PRODUCT_LIST, index=p_idx)
                    
                    type_options = ["Installation", "Complaint", "Repairing"]
                    curr_type = str(selected_row.get("Type", ""))
                    t_idx = type_options.index(curr_type) if curr_type in type_options else 0
                    e_type = st.selectbox("Reason or Type", type_options, index=t_idx)
                    
                    e_city = st.text_input("City", value=str(selected_row.get("City", "")))
                with col_e3:
                    curr_st = str(selected_row.get("State", ""))
                    st_idx = INDIAN_STATES.index(curr_st) if curr_st in INDIAN_STATES else 0
                    e_state = st.selectbox("State", INDIAN_STATES, index=st_idx)
                    
                    status_options = ["Running", "Hold", "Done"]
                    curr_stat = str(selected_row.get("Status", "Running"))
                    s_idx = status_options.index(curr_stat) if curr_stat in status_options else 0
                    e_status = st.selectbox("Status", status_options, index=s_idx)
                    
                    e_address = st.text_area("Address", value=str(selected_row.get("Address", "")), height=68)

                st.markdown("---")
                col_e4, col_e5, col_e6 = st.columns(3)
                with col_e4:
                    e_installer = st.text_input("Installer Name", value=str(selected_row.get("Installer", "")))
                    e_helper = st.text_input("Helper Name", value=str(selected_row.get("Helper", "")))
                with col_e5:
                    e_start_date = st.text_input("Start Date (YYYY-MM-DD)", value=str(selected_row.get("Start Date", "")))
                    e_end_date = st.text_input("End Date (YYYY-MM-DD)", value=str(selected_row.get("End Date", "")))
                with col_e6:
                    e_deliver_date = st.text_input("Deliver Date (YYYY-MM-DD)", value=str(selected_row.get("Deliver Date", "")))
                    e_remarks = st.text_area("Remarks / Notes", value=str(selected_row.get("Remarks", "")), height=68)

                save_update_btn = st.form_submit_button("Update Entire Record in Google Sheet")
                
                if save_update_btn:
                    try:
                        # Full row update in Google Sheet
                        updated_row_values = [
                            selected_client_id,
                            str(selected_row.get("Complaint Date", "")),
                            e_client_name,
                            e_company_name,
                            e_contact,
                            e_type,
                            e_product,
                            e_state,
                            e_city,
                            e_address,
                            e_installer,
                            e_helper,
                            e_status,
                            e_start_date,
                            e_end_date,
                            e_deliver_date,
                            e_remarks
                        ]
                        
                        cell_range = f"A{sheet_row_num}:Q{sheet_row_num}"
                        worksheet.update(cell_range, [updated_row_values])
                        
                        st.success(f"✅ Record successfully updated in Google Sheet for Client ID: {selected_client_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error updating Google Sheet: {e}")
    else:
        st.info("No records available to edit/update.")

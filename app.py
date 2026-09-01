import streamlit as st
import pandas as pd
from datetime import datetime, date
import re
import gspread
from google.oauth2.service_account import Credentials

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Enterprise Installation CRM", layout="wide", page_icon="🛠️")

# --- PROFESSIONAL CRM CUSTOM CSS ---
st.markdown("""
<style>
    /* Global Page Styling */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Headers & Title */
    h1 {
        color: #1e293b;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Metric Cards Styling */
    [data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: bold !important;
        color: #0f172a !important;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    
    /* Tabs Header Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #ffffff;
        padding: 8px 12px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 6px;
        font-weight: 600;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
    }
    
    /* Buttons Styling */
    .stButton>button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

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

# --- FUNCTION TO GENERATE SEQUENTIAL CLIENT ID ---
def generate_next_client_id(df):
    if df.empty or "Client ID" not in df.columns:
        return "CL-001"
    
    max_num = 0
    # Search through all Client IDs to find the highest number
    for cid in df["Client ID"].dropna().astype(str):
        match = re.search(r'CL-(\d+)', cid, re.IGNORECASE)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
                
    next_num = max_num + 1
    return f"CL-{next_num:03d}"

# --- PRODUCT LIST ---
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

# --- OVERDUE CHECKER ---
def check_overdue_expected_dates(df):
    overdue_list = []
    date_col = "Expected Date" if "Expected Date" in df.columns else ("Deliver Date" if "Deliver Date" in df.columns else None)
    
    if not df.empty and date_col and "Status" in df.columns:
        today = date.today()
        for idx, row in df.iterrows():
            status = str(row.get("Status", "")).strip()
            exp_date_str = str(row.get(date_col, "")).strip()
            client_id = str(row.get("Client ID", ""))
            client_name = str(row.get("Client Name", ""))
            
            if status != "Done" and exp_date_str and exp_date_str != "None":
                try:
                    exp_date = datetime.strptime(exp_date_str, "%Y-%m-%d").date()
                    if exp_date < today:
                        overdue_list.append({
                            "Client ID": client_id,
                            "Client Name": client_name,
                            "Expected Date": exp_date_str,
                            "Status": status
                        })
                except ValueError:
                    pass
    return overdue_list

overdue_items = check_overdue_expected_dates(crm_df)

def show_overdue_alert():
    if overdue_items:
        st.error(f"🚨 **CRITICAL ALERT: {len(overdue_items)} Overdue Expected Date Request(s) Pending Action!**")
        with st.expander("🔍 View All Overdue Details"):
            st.table(pd.DataFrame(overdue_items))

# --- HEADER SECTION ---
col_head1, col_head2 = st.columns([4, 1])
with col_head1:
    st.title("🛠️ Installation & Service CRM")
    st.caption("Real-Time Operations Management & Lead Tracking Dashboard")

show_overdue_alert()

# NAVIGATION TABS
tab_dash, tab_entry, tab_update = st.tabs(["📊 Analytics Dashboard", "📝 Register New Request", "🔄 Edit, Update & Delete Lead"])

# ==========================================
# --- TAB 1: ANALYTICS DASHBOARD ---
# ==========================================
with tab_dash:
    st.subheader("📌 Executive Performance Overview")
    df = crm_df.copy()
    
    if not df.empty and "Complaint Date" in df.columns:
        df['Parsed_Date'] = pd.to_datetime(df['Complaint Date'], errors='coerce')
        df['Year'] = df['Parsed_Date'].dt.year.fillna(0).astype(int)
        df['Month_Name'] = df['Parsed_Date'].dt.strftime('%B').fillna("Unknown")
        
        st.markdown("##### 📅 Filter History Data by Request Date")
        col_f1, col_f2 = st.columns(2)
        
        available_years = ["All Years"] + sorted([y for y in df['Year'].unique() if y != 0], reverse=True)
        selected_year = col_f1.selectbox("Select Year", available_years)
        
        months_list = ["All Months", "January", "February", "March", "April", "May", "June", 
                       "July", "August", "September", "October", "November", "December"]
        selected_month = col_f2.selectbox("Select Month", months_list)
        
        filtered_df = df.copy()
        if selected_year != "All Years":
            filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]
        if selected_month != "All Months":
            filtered_df = filtered_df[filtered_df['Month_Name'] == selected_month]
            
        st.markdown("---")
        
        total_entries = len(filtered_df)
        running_count = len(filtered_df[filtered_df["Status"] == "Running"])
        hold_count = len(filtered_df[filtered_df["Status"] == "Hold"])
        done_count = len(filtered_df[filtered_df["Status"] == "Done"])
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("📋 Total Requests", total_entries)
        col_m2.metric("🔄 Active Running", running_count)
        col_m3.metric("⏸️ On Hold", hold_count)
        col_m4.metric("✅ Completed (Done)", done_count)
        
        st.markdown("---")
        
        col_d1, col_d2 = st.columns([2, 1])
        with col_d1:
            st.subheader("📋 Service Records Data")
            display_cols = [c for c in ["Client ID", "Complaint Date", "Client Name", "Type", "City", "Status", "Installer"] if c in filtered_df.columns]
            st.dataframe(filtered_df[display_cols], use_container_width=True)
            
        with col_d2:
            st.subheader("📊 Category Distribution")
            if "Type" in filtered_df.columns and not filtered_df.empty:
                type_counts = filtered_df["Type"].value_counts()
                st.bar_chart(type_counts)
    else:
        st.info("No records available in Google Sheet. Please add new entries.")

# ==========================================
# --- TAB 2: REGISTER NEW REQUEST ---
# ==========================================
with tab_entry:
    st.subheader("📝 Register New Client Service Request")
    
    # Generate Sequential Client ID based on Google Sheet
    next_client_id = generate_next_client_id(crm_df)
    
    with st.form("crm_entry_form", clear_on_submit=True):
        st.info(f"🆔 **Next Serial Client ID:** `{next_client_id}`")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            req_type = st.selectbox("Reason or Request Type*", ["Installation", "Complaint", "Repairing"])
            complaint_date = st.date_input("Complaint / Request Date*", datetime.now())
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
        st.subheader("👨‍🔧 Team Assignment & Initial Schedule")
        col6, col7, col8 = st.columns(3)
        with col6:
            installer_name = st.text_input("Installer Name")
        with col7:
            helper_name = st.text_input("Helper Name")
        with col8:
            status = st.selectbox("Initial Status*", ["Running", "Hold", "Done"])

        col9, col10, col11 = st.columns(3)
        with col9:
            add_start = st.checkbox("Set Start Date", value=True)
            start_date_val = st.date_input("Start Date", datetime.now()) if add_start else ""
        with col10:
            add_end = st.checkbox("Set End Date", value=False)
            end_date_val = st.date_input("End Date", datetime.now()) if add_end else ""
        with col11:
            add_exp = st.checkbox("Set Expected Date", value=False)
            expected_date_val = st.date_input("Expected Date", datetime.now()) if add_exp else ""

        remarks = st.text_area("Remarks / Initial Notes")
        submit_btn = st.form_submit_button("Submit & Save Record")

    if submit_btn:
        if not client_name or not contact_number or not city_input:
            st.error("⚠️ Mandatory Fields Missing! Please fill: Client Name, Contact Number, and City.")
        else:
            # Re-fetch fresh worksheet data before submitting to prevent concurrent ID clash
            _, fresh_df = load_data()
            final_client_id = generate_next_client_id(fresh_df)

            new_row = [
                final_client_id,
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
                str(start_date_val) if start_date_val else "",
                str(end_date_val) if end_date_val else "",
                str(expected_date_val) if expected_date_val else "",
                remarks
            ]
            try:
                worksheet.append_row(new_row)
                st.success(f"✅ Record successfully created with ID: **{final_client_id}**")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Database Error: {e}")

    st.markdown("---")
    st.subheader("📑 Top 10 Recent Registrations")
    if not crm_df.empty:
        top_10_df = crm_df.tail(10).iloc[::-1]
        st.dataframe(top_10_df, use_container_width=True)
    else:
        st.info("No registrations recorded yet.")

# ==========================================
# --- TAB 3: EDIT, UPDATE & DELETE ---
# ==========================================
with tab_update:
    st.subheader("🔄 Update Lead Details or Remove Entry")
    
    if not crm_df.empty and "Client ID" in crm_df.columns:
        client_list = crm_df["Client ID"].astype(str).tolist()
        selected_client_id = st.selectbox("🔍 Search & Select Client ID to Modify:", client_list)
        
        matching_rows = crm_df[crm_df["Client ID"].astype(str) == selected_client_id]
        
        if not matching_rows.empty:
            record_idx = matching_rows.index[0]
            selected_row = crm_df.loc[record_idx]
            sheet_row_num = record_idx + 2
            
            st.markdown("---")
            st.subheader(f"✏️ Editing Details for: {selected_row.get('Client Name', '')} (`{selected_client_id}`)")
            
            prev_expected = selected_row.get("Expected Date", selected_row.get("Deliver Date", ""))
            
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
                    e_type = st.selectbox("Request Type", type_options, index=t_idx)
                    
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
                st.caption("ℹ️ Note: Leave Date fields empty if not applicable (YYYY-MM-DD format).")
                col_e4, col_e5, col_e6 = st.columns(3)
                with col_e4:
                    e_installer = st.text_input("Installer Name", value=str(selected_row.get("Installer", "")))
                    e_helper = st.text_input("Helper Name", value=str(selected_row.get("Helper", "")))
                with col_e5:
                    e_complaint_date = st.text_input("Request Date", value=str(selected_row.get("Complaint Date", "")))
                    e_start_date = st.text_input("Start Date", value=str(selected_row.get("Start Date", "")))
                with col_e6:
                    e_end_date = st.text_input("End Date", value=str(selected_row.get("End Date", "")))
                    e_expected_date = st.text_input("Expected Date", value=str(prev_expected))

                e_remarks = st.text_area("Remarks / Notes", value=str(selected_row.get("Remarks", "")), height=68)

                save_update_btn = st.form_submit_button("💾 Save & Sync Changes")
                
                if save_update_btn:
                    try:
                        updated_row_values = [
                            selected_client_id,
                            e_complaint_date,
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
                            e_expected_date,
                            e_remarks
                        ]
                        
                        cell_range = f"A{sheet_row_num}:Q{sheet_row_num}"
                        worksheet.update(cell_range, [updated_row_values])
                        
                        st.success(f"✅ Record successfully updated in Google Sheet for Client ID: {selected_client_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error updating Google Sheet: {e}")

            # --- DELETE ENTRY SECTION ---
            st.markdown("---")
            st.subheader("🚨 Danger Zone (Delete Record)")
            
            with st.expander("🗑️ Delete This Client Entry Permanently"):
                st.warning(f"Are you sure you want to delete Client ID: **{selected_client_id}** ({selected_row.get('Client Name', '')})? This action cannot be undone.")
                if st.button("Yes, Delete Entry Permanently", type="primary"):
                    try:
                        worksheet.delete_rows(sheet_row_num)
                        st.success(f"🗑️ Record {selected_client_id} has been permanently deleted from Google Sheet!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Delete action failed: {e}")
    else:
        st.info("No records available to edit or delete.")

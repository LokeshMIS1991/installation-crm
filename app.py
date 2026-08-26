import streamlit as st
import pandas as pd
from datetime import datetime
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

# --- INDIA STATES & CITIES DATA ---
INDIA_DATA = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Other"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Other"],
    "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Other"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Other"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Other"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Other"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Other"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Mohali", "Other"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Other"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Other"],
    "Uttar Pradesh": ["Noida", "Ghaziabad", "Lucknow", "Kanpur", "Agra", "Varanasi", "Other"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Other"],
    "Other": ["Other"]
}

st.title("🛠️ Installation CRM")

# Navigation Tabs
tab_dash, tab_entry, tab_update = st.tabs(["📊 Dashboard", "📝 New Request Entry", "🔄 Update & View Status"])

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
            st.subheader("📋 Recent Service Requests")
            display_cols = [col for col in ["Client ID", "Client Name", "Type", "City", "Status", "Installer"] if col in df.columns]
            st.dataframe(df[display_cols], use_container_width=True)
            
        with col_d2:
            st.subheader("📊 Request Types")
            if "Type" in df.columns:
                type_counts = df["Type"].value_counts()
                st.bar_chart(type_counts)
    else:
        st.info("Abhi Google Sheet mein koi data nahi hai. Nayi entry add karein!")

# ==========================================
# --- TAB 2: NEW REQUEST ENTRY ---
# ==========================================
with tab_entry:
    st.subheader("📝 Register New Installation or Complaint")
    generated_client_id = f"CL-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
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
            product_details = st.text_input("Product Suggested / Type", placeholder="e.g. CCTV, Water Purifier, Model X")

        st.markdown("---")
        st.subheader("📍 Location Details")
        col_st, col_ct, col_addr = st.columns(3)
        with col_st:
            state_selected = st.selectbox("State*", sorted(list(INDIA_DATA.keys())))
        with col_ct:
            city_options = INDIA_DATA.get(state_selected, ["Other"])
            city_selected = st.selectbox("City*", city_options)
            custom_city = st.text_input("Specify City Name*") if city_selected == "Other" else city_selected
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
        if not client_name or not contact_number:
            st.error("⚠️ Please fill required fields: Client Name and Contact Number!")
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
                custom_city,
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
                st.success(f"✅ Record saved directly to Google Sheet! Client ID: {generated_client_id}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to save entry to Google Sheet: {e}")

# ==========================================
# --- TAB 3: UPDATE STATUS & EDIT DATA ---
# ==========================================
with tab_update:
    st.subheader("🔄 Update Lead Status & Tracking")
    
    if not crm_df.empty and "Client ID" in crm_df.columns:
        status_filter = st.radio("Filter List By Status:", ["All", "Running", "Hold", "Done"], horizontal=True)
        
        filtered_df = crm_df
        if status_filter != "All" and "Status" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]
            
        st.dataframe(filtered_df, use_container_width=True)
        
        st.markdown("---")
        st.subheader("✏️ Edit Request Details")
        
        client_list = crm_df["Client ID"].astype(str).tolist()
        
        if client_list:
            selected_client_id = st.selectbox("Select Client ID to Update:", client_list)
            
            # Find row in DataFrame
            matching_rows = crm_df[crm_df["Client ID"].astype(str) == selected_client_id]
            if not matching_rows.empty:
                record_idx = matching_rows.index[0]
                selected_row = crm_df.loc[record_idx]
                
                # Google Sheet Header row counts as row 1, pandas index 0 is sheet row 2
                sheet_row_num = record_idx + 2
                
                with st.form("update_form"):
                    st.write(f"Updating Details for: **{selected_row.get('Client Name', '')}** (`{selected_client_id}`)")
                    
                    up_col1, up_col2, up_col3 = st.columns(3)
                    with up_col1:
                        status_list = ["Running", "Hold", "Done"]
                        curr_status = str(selected_row.get("Status", "Running"))
                        status_idx = status_list.index(curr_status) if curr_status in status_list else 0
                        new_status = st.selectbox("Update Status*", status_list, index=status_idx)
                        
                    with up_col2:
                        new_installer = st.text_input("Installer Name", value=str(selected_row.get("Installer", "")))
                    with up_col3:
                        new_helper = st.text_input("Helper Name", value=str(selected_row.get("Helper", "")))
                        
                    up_col4, up_col5 = st.columns(2)
                    with up_col4:
                        new_remarks = st.text_area("Update Remarks / Progress Notes", value=str(selected_row.get("Remarks", "")))
                    with up_col5:
                        new_deliver_date = st.text_input("Deliver Date", value=str(selected_row.get("Deliver Date", "")))
                        
                    update_btn = st.form_submit_button("Save Status Update")
                    
                    if update_btn:
                        try:
                            # Update specific cells in Google Sheet
                            # K=Installer (Col 11), L=Helper (Col 12), M=Status (Col 13), P=Deliver Date (Col 16), Q=Remarks (Col 17)
                            worksheet.update_cell(sheet_row_num, 11, new_installer)
                            worksheet.update_cell(sheet_row_num, 12, new_helper)
                            worksheet.update_cell(sheet_row_num, 13, new_status)
                            worksheet.update_cell(sheet_row_num, 16, new_deliver_date)
                            worksheet.update_cell(sheet_row_num, 17, new_remarks)
                            
                            st.success(f"✅ Google Sheet updated successfully for {selected_client_id}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error updating sheet: {e}")
    else:
        st.info("Update karne ke liye filhaal Sheet mein koi data nahi milaa.")

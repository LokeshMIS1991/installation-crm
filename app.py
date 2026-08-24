import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Installation CRM", layout="wide", page_icon="🛠️")

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

# --- DUMMY DATA INITIALIZATION (Simulating Google Sheets) ---
if "crm_data" not in st.session_state:
    st.session_state.crm_data = pd.DataFrame([
        {
            "Client ID": "CL-20260824100001",
            "Complaint Date": "2026-08-20",
            "Client Name": "Rajesh Kumar",
            "Company Name": "ABC Infra",
            "Contact Number": "9876543210",
            "Type": "Installation",
            "Product": "CCTV Camera",
            "State": "Delhi",
            "City": "New Delhi",
            "Address": "Connaught Place",
            "Installer": "Amit Sharma",
            "Helper": "Ramesh",
            "Status": "Running",
            "Start Date": "2026-08-21",
            "End Date": "2026-08-25",
            "Deliver Date": "2026-08-26",
            "Remarks": "Wiring in progress"
        },
        {
            "Client ID": "CL-20260824100002",
            "Complaint Date": "2026-08-22",
            "Client Name": "Global Tech Ltd",
            "Company Name": "Global Tech",
            "Contact Number": "9123456789",
            "Type": "Complaint",
            "Product": "Water Purifier",
            "State": "Uttar Pradesh",
            "City": "Noida",
            "Address": "Sector 62",
            "Installer": "Vikas Verma",
            "Helper": "Suresh",
            "Status": "Done",
            "Start Date": "2026-08-22",
            "End Date": "2026-08-23",
            "Deliver Date": "2026-08-23",
            "Remarks": "Filter replaced successfully"
        },
        {
            "Client ID": "CL-20260824100003",
            "Complaint Date": "2026-08-23",
            "Client Name": "Sunil Verma",
            "Company Name": "Sunil Enterprises",
            "Contact Number": "9988776655",
            "Type": "Repairing",
            "Product": "Solar Inverter",
            "State": "Rajasthan",
            "City": "Jaipur",
            "Address": "Malviya Nagar",
            "Installer": "Karan Singh",
            "Helper": "Mahesh",
            "Status": "Hold",
            "Start Date": "2026-08-24",
            "End Date": "2026-08-28",
            "Deliver Date": "2026-08-29",
            "Remarks": "Waiting for spare parts arrival"
        }
    ])

st.title("🛠️ Installation CRM")

# Navigation Tabs
tab_dash, tab_entry, tab_update = st.tabs(["📊 Dashboard", "📝 New Request Entry", "🔄 Update & View Status"])

# ==========================================
# --- TAB 1: EXECUTIVE DASHBOARD ---
# ==========================================
with tab_dash:
    st.subheader("📌 Performance Overview")
    df = st.session_state.crm_data
    
    # Key Metric Cards
    total_entries = len(df)
    running_count = len(df[df["Status"] == "Running"])
    hold_count = len(df[df["Status"] == "Hold"])
    done_count = len(df[df["Status"] == "Done"])
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("📋 Total Requests", total_entries)
    col_m2.metric("🔄 Running", running_count, delta_color="normal")
    col_m3.metric("⏸️ On Hold", hold_count, delta_color="inverse")
    col_m4.metric("✅ Completed (Done)", done_count)
    
    st.markdown("---")
    
    # Breakdowns & Filtered View
    col_d1, col_d2 = st.columns([2, 1])
    
    with col_d1:
        st.subheader("📋 Recent Service Requests")
        st.dataframe(df[["Client ID", "Client Name", "Type", "City", "Status", "Installer"]], use_container_width=True)
        
    with col_d2:
        st.subheader("📊 Request Types")
        type_counts = df["Type"].value_counts()
        st.bar_chart(type_counts)

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
            new_record = {
                "Client ID": generated_client_id,
                "Complaint Date": str(complaint_date),
                "Client Name": client_name,
                "Company Name": company_name,
                "Contact Number": contact_number,
                "Type": req_type,
                "Product": product_details,
                "State": state_selected,
                "City": custom_city,
                "Address": address,
                "Installer": installer_name,
                "Helper": helper_name,
                "Status": status,
                "Start Date": str(start_date),
                "End Date": str(end_date),
                "Deliver Date": str(deliver_date),
                "Remarks": remarks
            }
            # Add to dataframe
            st.session_state.crm_data = pd.concat([st.session_state.crm_data, pd.DataFrame([new_record])], ignore_index=True)
            st.success(f"✅ Record saved! Client ID: {generated_client_id}")

# ==========================================
# --- TAB 3: UPDATE STATUS & EDIT DATA ---
# ==========================================
with tab_update:
    st.subheader("🔄 Update Lead Status & Tracking")
    
    # Filter Records by Status
    status_filter = st.radio("Filter List By Status:", ["All", "Running", "Hold", "Done"], horizontal=True)
    
    filtered_df = st.session_state.crm_data
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status_filter]
        
    st.dataframe(filtered_df, use_container_width=True)
    
    st.markdown("---")
    st.subheader("✏️ Edit Request Details")
    
    # Select Client ID to Update
    client_list = st.session_state.crm_data["Client ID"].tolist()
    
    if client_list:
        selected_client_id = st.selectbox("Select Client ID to Update:", client_list)
        
        # Fetch existing record
        record_idx = st.session_state.crm_data[st.session_state.crm_data["Client ID"] == selected_client_id].index[0]
        selected_row = st.session_state.crm_data.loc[record_idx]
        
        with st.form("update_form"):
            st.write(f"Updating Details for: **{selected_row['Client Name']}** (`{selected_client_id}`)")
            
            up_col1, up_col2, up_col3 = st.columns(3)
            with up_col1:
                # Set default index for Status dropdown
                status_list = ["Running", "Hold", "Done"]
                status_idx = status_list.index(selected_row["Status"]) if selected_row["Status"] in status_list else 0
                new_status = st.selectbox("Update Status*", status_list, index=status_idx)
                
            with up_col2:
                new_installer = st.text_input("Installer Name", value=selected_row["Installer"])
            with up_col3:
                new_helper = st.text_input("Helper Name", value=selected_row["Helper"])
                
            up_col4, up_col5 = st.columns(2)
            with up_col4:
                new_remarks = st.text_area("Update Remarks / Progress Notes", value=selected_row["Remarks"])
            with up_col5:
                new_deliver_date = st.text_input("Deliver Date", value=selected_row["Deliver Date"])
                
            update_btn = st.form_submit_button("Save Status Update")
            
            if update_btn:
                # Update session state data
                st.session_state.crm_data.at[record_idx, "Status"] = new_status
                st.session_state.crm_data.at[record_idx, "Installer"] = new_installer
                st.session_state.crm_data.at[record_idx, "Helper"] = new_helper
                st.session_state.crm_data.at[record_idx, "Remarks"] = new_remarks
                st.session_state.crm_data.at[record_idx, "Deliver Date"] = new_deliver_date
                
                st.success(f"✅ Status updated to '{new_status}' for {selected_client_id}!")
                st.rerun()

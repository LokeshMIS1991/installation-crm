import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Installation CRM", layout="wide", page_icon="🛠️")

# Complete India States (28 States + 8 Union Territories) and Major Cities
INDIA_DATA = {
    # --- STATES ---
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Tirupati", "Kakinada", "Other"],
    "Arunachal Pradesh": ["Itanagar", "Naharlagun", "Pasighat", "Other"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Nagaon", "Other"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Purnia", "Darbhanga", "Other"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Durg", "Other"],
    "Goa": ["Panaji", "Margao", "Vasco da Gama", "Mapusa", "Other"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Other"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Karnal", "Hisar", "Rohtak", "Other"],
    "Himachal Pradesh": ["Shimla", "Dharamshala", "Mandi", "Solan", "Baddi", "Other"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Hazaribagh", "Other"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Belagavi", "Davangere", "Other"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam", "Other"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain", "Sagar", "Other"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Chhatrapati Sambhajinagar", "Solapur", "Other"],
    "Manipur": ["Imphal", "Churachandpur", "Other"],
    "Meghalaya": ["Shillong", "Tura", "Other"],
    "Mizoram": ["Aizawl", "Lunglei", "Other"],
    "Nagaland": ["Kohima", "Dimapur", "Other"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri", "Sambalpur", "Other"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Mohali", "Bathinda", "Other"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Ajmer", "Bhilwara", "Alwar", "Other"],
    "Sikkim": ["Gangtok", "Namchi", "Other"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Tiruppur", "Erode", "Other"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam", "Other"],
    "Tripura": ["Agartala", "Udaipur", "Other"],
    "Uttar Pradesh": ["Noida", "Ghaziabad", "Lucknow", "Kanpur", "Agra", "Varanasi", "Prayagraj", "Meerut", "Bareilly", "Aligarh", "Other"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Haldwani", "Rudrakyapur", "Other"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Siliguri", "Asansol", "Other"],
    
    # --- UNION TERRITORIES ---
    "Andaman and Nicobar Islands": ["Port Blair", "Other"],
    "Chandigarh": ["Chandigarh", "Other"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Daman", "Diu", "Silvassa", "Other"],
    "Delhi": ["New Delhi", "North Delhi", "South Delhi", "East Delhi", "West Delhi", "Central Delhi", "Other"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Baramulla", "Other"],
    "Ladakh": ["Leh", "Kargil", "Other"],
    "Lakshadweep": ["Kavaratti", "Other"],
    "Puducherry": ["Puducherry", "Karaikal", "Ozhukarai", "Other"]
}

st.title("🛠️ Installation CRM")

# Navigation Tabs
tab1, tab2 = st.tabs(["📝 New Entry Form", "📊 View & Update Requests"])

# --- TAB 1: NEW ENTRY FORM ---
with tab1:
    st.subheader("Supervisor Data Entry Form")
    
    # Auto-generate unique Client ID based on timestamp
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
            product_details = st.text_input("Product Suggested / Type", placeholder="e.g. CCTV, Purifier, Model A")

        st.markdown("---")
        st.subheader("📍 Location Details")
        col_st, col_ct, col_addr = st.columns(3)
        
        with col_st:
            state_selected = st.selectbox("State*", sorted(list(INDIA_DATA.keys())))

        with col_ct:
            city_options = INDIA_DATA.get(state_selected, ["Other"])
            city_selected = st.selectbox("City*", city_options)
            
            if city_selected == "Other":
                custom_city = st.text_input("Specify City Name*")
            else:
                custom_city = city_selected

        with col_addr:
            address = st.text_area("Specific Area / Address", height=68, placeholder="Street, Landmark, Pincode...")

        st.markdown("---")
        st.subheader("👨‍🔧 Team Assignment")
        col6, col7 = st.columns(2)
        with col6:
            installer_name = st.text_input("Installer Name")
        with col7:
            helper_name = st.text_input("Helper Name")

        st.markdown("---")
        st.subheader("📅 Status & Timeline")
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
        final_city = custom_city if city_selected == "Other" else city_selected
        
        if not client_name or not contact_number:
            st.error("⚠️ Please fill required fields: Client Name and Contact Number!")
        else:
            st.success(f"✅ Entry saved successfully! Client ID: {generated_client_id} | Location: {final_city}, {state_selected}")

# --- TAB 2: VIEW & SEARCH DATA ---
with tab2:
    st.subheader("Live Status Dashboard")
    st.info("Yeh Section Google Sheet integration ke baad real-time update dikhayega.")
    
    dummy_data = pd.DataFrame([
        {
            "Client ID": "CL-20260824120000",
            "Client Name": "Rajesh Kumar",
            "Type": "Installation",
            "State": "Delhi",
            "City": "New Delhi",
            "Status": "Running",
            "Installer": "Amit Sharma"
        },
        {
            "Client ID": "CL-20260824120500",
            "Client Name": "Global Tech",
            "Type": "Complaint",
            "State": "Uttar Pradesh",
            "City": "Noida",
            "Status": "Done",
            "Installer": "Vikas Verma"
        }
    ])
    st.dataframe(dummy_data, use_container_width=True)

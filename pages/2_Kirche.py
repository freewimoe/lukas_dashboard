import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# === Page Configuration ===
st.set_page_config(page_title="Church Dashboard", page_icon="⛪", layout="wide")

# === Header ===
st.title("⛪ Church Dashboard")
st.markdown("Management of church services, parish events and religious activities")
st.markdown("---")

# === Navigation ===
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🏠 Back to Main", use_container_width=True):
        st.switch_page("streamlit_app.py")

# === Main Content ===
tab1, tab2, tab3 = st.tabs(["🛐 Services", "📅 Events", "👥 Parish"])

with tab1:
    st.subheader("🛐 Church Services Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Regular Services Schedule**")
        
        # Sample service schedule
        services_data = {
            'Day': ['Sunday', 'Sunday', 'Wednesday', 'Friday'],
            'Time': ['09:00', '11:00', '19:00', '18:00'],
            'Service Type': ['Morning Service', 'Family Service', 'Evening Prayer', 'Youth Service'],
            'Average Attendance': [45, 65, 20, 25]
        }
        
        services_df = pd.DataFrame(services_data)
        st.dataframe(services_df, use_container_width=True)
    
    with col2:
        st.metric("This Week's Services", "4")
        st.metric("Average Attendance", "39")
        st.metric("Special Events", "2")
    
    # Add new service form
    with st.expander("➕ Add New Service"):
        with st.form("new_service_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                service_date = st.date_input("Service Date")
                service_time = st.time_input("Service Time")
                
            with col2:
                service_type = st.selectbox("Service Type", 
                    ["Regular Service", "Family Service", "Youth Service", "Evening Prayer", "Special Service"])
                expected_attendance = st.number_input("Expected Attendance", min_value=1, value=30)
            
            service_notes = st.text_area("Notes")
            
            if st.form_submit_button("Add Service"):
                st.success("✅ Service added to schedule!")

with tab2:
    st.subheader("📅 Parish Events")
    
    # Upcoming events
    st.write("**Upcoming Events**")
    
    # Sample events data
    events_data = {
        'Event': ['Parish Meeting', 'Bible Study', 'Community Lunch', 'Confirmation Class'],
        'Date': ['2024-07-25', '2024-07-27', '2024-07-30', '2024-08-01'],
        'Time': ['19:00', '18:30', '12:00', '16:00'],
        'Expected Participants': [15, 8, 40, 12],
        'Status': ['Confirmed', 'Confirmed', 'Planning', 'Confirmed']
    }
    
    events_df = pd.DataFrame(events_data)
    st.dataframe(events_df, use_container_width=True)
    
    # Add new event
    with st.expander("➕ Add New Parish Event"):
        with st.form("parish_event_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                event_name = st.text_input("Event Name")
                event_date = st.date_input("Event Date")
                event_time = st.time_input("Event Time")
                
            with col2:
                event_type = st.selectbox("Event Type", 
                    ["Parish Meeting", "Bible Study", "Community Event", "Educational", "Other"])
                expected_participants = st.number_input("Expected Participants", min_value=1, value=15)
                event_status = st.selectbox("Status", ["Planning", "Confirmed", "Cancelled"])
            
            event_description = st.text_area("Event Description")
            
            if st.form_submit_button("Add Event"):
                st.success(f"✅ Event '{event_name}' added successfully!")

with tab3:
    st.subheader("👥 Parish Community")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Members", "127")
        st.metric("Regular Attendees", "85")
        
    with col2:
        st.metric("Youth Members", "23")
        st.metric("Senior Members", "34")
        
    with col3:
        st.metric("Volunteers", "18")
        st.metric("Committees", "5")
    
    # Member engagement tracking
    st.write("**Member Engagement Overview**")
    
    engagement_data = {
        'Category': ['Regular Attendees', 'Occasional Attendees', 'Special Events Only', 'Volunteers'],
        'Count': [45, 30, 25, 18],
        'Percentage': ['35%', '24%', '20%', '14%']
    }
    
    engagement_df = pd.DataFrame(engagement_data)
    st.dataframe(engagement_df, use_container_width=True)
    
    # Member directory (placeholder)
    with st.expander("📋 Member Directory"):
        st.info("🚧 Member directory feature under development")
        st.write("This section will include:")
        st.write("- Member contact information")
        st.write("- Volunteer roles and responsibilities")
        st.write("- Committee memberships")
        st.write("- Attendance tracking")

# === Footer Information ===
st.markdown("---")
st.info("💡 **Note:** This is a demo version. In production, all data would be stored in a secure database with proper member privacy protections.")
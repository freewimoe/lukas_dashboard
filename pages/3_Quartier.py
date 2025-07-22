import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# === Page Configuration ===
st.set_page_config(page_title="District Dashboard", page_icon="🏘️", layout="wide")

# === Header ===
st.title("🏘️ District Dashboard")
st.markdown("Neighborhood engagement and local community projects")
st.markdown("---")

# === Navigation ===
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🏠 Back to Main", use_container_width=True):
        st.switch_page("streamlit_app.py")

# === Main Content ===
tab1, tab2, tab3, tab4 = st.tabs(["🏘️ Overview", "🤝 Projects", "📊 Community Data", "📞 Contacts"])

with tab1:
    st.subheader("🏘️ District Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Projects", "8")
        st.metric("Volunteers", "34")
        
    with col2:
        st.metric("Households Reached", "156")
        st.metric("Monthly Events", "12")
        
    with col3:
        st.metric("Partner Organizations", "6")
        st.metric("Success Rate", "94%")
        
    with col4:
        st.metric("Budget Used", "€2,840")
        st.metric("Budget Remaining", "€1,160")
    
    # Recent activities
    st.subheader("📋 Recent Activities")
    
    activities_data = {
        'Date': ['2024-07-20', '2024-07-18', '2024-07-15', '2024-07-12'],
        'Activity': ['Senior Citizen Support', 'Neighborhood Clean-up', 'Youth Soccer Training', 'Community Garden'],
        'Participants': [12, 25, 18, 8],
        'Status': ['Completed', 'Completed', 'Ongoing', 'Ongoing'],
        'Impact': ['High', 'Medium', 'High', 'Medium']
    }
    
    activities_df = pd.DataFrame(activities_data)
    st.dataframe(activities_df, use_container_width=True)

with tab2:
    st.subheader("🤝 Community Projects")
    
    # Project categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Active Projects**")
        
        projects_data = {
            'Project Name': ['Senior Care Network', 'Youth Mentorship', 'Community Garden', 'Neighborhood Watch'],
            'Category': ['Social Services', 'Education', 'Environment', 'Safety'],
            'Status': ['Active', 'Active', 'Planning', 'Active'],
            'Volunteers': [8, 6, 4, 12],
            'Budget': ['€800', '€600', '€400', '€200']
        }
        
        projects_df = pd.DataFrame(projects_data)
        st.dataframe(projects_df, use_container_width=True)
    
    with col2:
        # Project distribution chart
        if len(projects_df) > 0:
            category_counts = projects_df['Category'].value_counts()
            fig = px.pie(
                values=category_counts.values,
                names=category_counts.index,
                title="Projects by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Add new project
    with st.expander("➕ Add New Project"):
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("Project Name")
                project_category = st.selectbox("Category", 
                    ["Social Services", "Education", "Environment", "Safety", "Health", "Culture"])
                start_date = st.date_input("Start Date")
                
            with col2:
                project_leader = st.text_input("Project Leader")
                estimated_budget = st.number_input("Estimated Budget (€)", min_value=0, value=500)
                target_participants = st.number_input("Target Participants", min_value=1, value=10)
            
            project_description = st.text_area("Project Description")
            project_goals = st.text_area("Project Goals")
            
            if st.form_submit_button("Add Project"):
                st.success(f"✅ Project '{project_name}' added successfully!")

with tab3:
    st.subheader("📊 Community Data & Analytics")
    
    # Demographics (sample data)
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Age Distribution**")
        age_data = {
            'Age Group': ['0-18', '19-35', '36-50', '51-65', '65+'],
            'Count': [45, 78, 92, 67, 43],
            'Percentage': ['14%', '24%', '28%', '21%', '13%']
        }
        age_df = pd.DataFrame(age_data)
        
        fig_age = px.bar(
            age_df, 
            x='Age Group', 
            y='Count',
            title="Neighborhood Age Distribution"
        )
        st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        st.write("**Engagement Levels**")
        engagement_data = {
            'Engagement Level': ['Very Active', 'Active', 'Occasional', 'Passive'],
            'Households': [25, 45, 56, 30]
        }
        engagement_df = pd.DataFrame(engagement_data)
        
        fig_engagement = px.pie(
            engagement_df,
            values='Households',
            names='Engagement Level',
            title="Community Engagement"
        )
        st.plotly_chart(fig_engagement, use_container_width=True)
    
    # Community needs assessment
    st.subheader("🎯 Community Needs Assessment")
    
    needs_data = {
        'Need Category': ['Senior Support', 'Youth Programs', 'Safety Measures', 'Environmental', 'Social Events'],
        'Priority Level': ['High', 'High', 'Medium', 'Medium', 'Low'],
        'Current Coverage': ['60%', '75%', '40%', '30%', '80%'],
        'Gap': ['40%', '25%', '60%', '70%', '20%']
    }
    
    needs_df = pd.DataFrame(needs_data)
    st.dataframe(needs_df, use_container_width=True)

with tab4:
    st.subheader("📞 Important Contacts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Local Organizations**")
        
        contacts_data = {
            'Organization': ['City District Office', 'Local Police', 'Health Center', 'School District'],
            'Contact Person': ['Maria Schmidt', 'Officer Weber', 'Dr. Mueller', 'Principal Klein'],
            'Phone': ['+49 721 123-456', '+49 721 133', '+49 721 789-012', '+49 721 345-678'],
            'Email': ['m.schmidt@karlsruhe.de', 'weber@polizei-ka.de', 'info@gesundheit-ka.de', 'klein@schule-ka.de']
        }
        
        contacts_df = pd.DataFrame(contacts_data)
        st.dataframe(contacts_df, use_container_width=True)
    
    with col2:
        st.write("**Community Leaders**")
        
        leaders_data = {
            'Name': ['Hans Quartier', 'Anna Müller', 'Peter Weber', 'Lisa Fischer'],
            'Role': ['District Coordinator', 'Youth Leader', 'Senior Advocate', 'Environment Coordinator'],
            'Phone': ['+49 721 555-001', '+49 721 555-002', '+49 721 555-003', '+49 721 555-004'],
            'Specialization': ['General Coordination', 'Youth Programs', 'Senior Services', 'Sustainability']
        }
        
        leaders_df = pd.DataFrame(leaders_data)
        st.dataframe(leaders_df, use_container_width=True)
    
    # Emergency contacts
    with st.expander("🚨 Emergency Contacts"):
        st.error("**Emergency Services**")
        st.write("- **Police:** 110")
        st.write("- **Fire/Medical:** 112") 
        st.write("- **Local Emergency Coordination:** +49 721 133-7777")
        
        st.warning("**Non-Emergency Support**")
        st.write("- **City Hotline:** +49 721 133-0")
        st.write("- **Social Services:** +49 721 133-5555")
        st.write("- **Senior Emergency:** +49 721 133-6666")

# === Quick Actions ===
st.markdown("---")
st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📋 Report Issue", use_container_width=True):
        st.info("Issue reporting form would open here")

with col2:
    if st.button("🤝 Volunteer Sign-up", use_container_width=True):
        st.info("Volunteer registration form would open here")

with col3:
    if st.button("📅 Event Calendar", use_container_width=True):
        st.info("Community event calendar would open here")

with col4:
    if st.button("💬 Community Forum", use_container_width=True):
        st.info("Community discussion forum would open here")
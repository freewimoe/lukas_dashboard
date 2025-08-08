import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# === Page Configuration ===
st.set_page_config(page_title="Community Dashboard", page_icon="💬", layout="wide")

# === Header ===
st.title("💬 Community Dashboard")
st.markdown("Communication and collaboration between all areas")
st.markdown("---")

# === Navigation ===
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🏠 Back to Main", use_container_width=True):
        st.switch_page("streamlit_app.py")

# === Main Content ===
tab1, tab2, tab3, tab4 = st.tabs(["📢 Announcements", "📅 Calendar", "📊 Cross-Area Analytics", "🔧 Tools"])

with tab1:
    st.subheader("📢 Community Announcements")
    
    # Create new announcement
    with st.expander("➕ Create New Announcement"):
        with st.form("announcement_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                announcement_title = st.text_input("Announcement Title")
                announcement_category = st.selectbox("Category", 
                    ["General", "Culture", "Church", "District", "Emergency", "Event"])
                priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
                
            with col2:
                target_audience = st.multiselect("Target Audience", 
                    ["All Users", "Culture Team", "Church Team", "District Team", "Volunteers", "Community Members"])
                publish_date = st.date_input("Publish Date", value=datetime.now().date())
                expiry_date = st.date_input("Expiry Date", value=datetime.now().date() + timedelta(days=30))
            
            announcement_content = st.text_area("Announcement Content", height=100)
            
            if st.form_submit_button("Publish Announcement"):
                if announcement_title and announcement_content:
                    # Store announcement (in production: database)
                    if 'announcements' not in st.session_state:
                        st.session_state['announcements'] = []
                    
                    new_announcement = {
                        'title': announcement_title,
                        'category': announcement_category,
                        'priority': priority,
                        'content': announcement_content,
                        'target_audience': target_audience,
                        'publish_date': publish_date.strftime('%Y-%m-%d'),
                        'expiry_date': expiry_date.strftime('%Y-%m-%d'),
                        'created_by': 'Current User',
                        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    st.session_state['announcements'].append(new_announcement)
                    st.success(f"✅ Announcement '{announcement_title}' published successfully!")
                else:
                    st.error("❌ Please fill in all required fields")
    
    # Display announcements
    st.subheader("📋 Current Announcements")
    
    if 'announcements' in st.session_state and len(st.session_state['announcements']) > 0:
        for i, announcement in enumerate(st.session_state['announcements']):
            priority_color = {
                'Low': '🟢',
                'Medium': '🟡', 
                'High': '🟠',
                'Urgent': '🔴'
            }
            
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{priority_color[announcement['priority']]} {announcement['title']}**")
                    st.write(announcement['content'])
                    
                with col2:
                    st.write(f"**Category:** {announcement['category']}")
                    st.write(f"**Published:** {announcement['publish_date']}")
                    
                with col3:
                    st.write(f"**Priority:** {announcement['priority']}")
                    st.write(f"**Expires:** {announcement['expiry_date']}")
                
                st.markdown("---")
    else:
        st.info("📢 No announcements yet. Create one using the form above.")

with tab2:
    st.subheader("📅 Unified Calendar")
    
    # Calendar overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Upcoming Events (All Areas)**")
        
        # Sample unified calendar data
        calendar_data = {
            'Date': ['2024-07-25', '2024-07-26', '2024-07-27', '2024-07-28', '2024-07-30'],
            'Event': ['Summer Concert', 'Parish Meeting', 'District Clean-up', 'Youth Workshop', 'Community Lunch'],
            'Area': ['Culture', 'Church', 'District', 'Culture', 'Church'],
            'Time': ['19:00', '19:30', '09:00', '16:00', '12:00'],
            'Location': ['Main Hall', 'Church Hall', 'Neighborhood', 'Youth Room', 'Community Kitchen'],
            'Organizer': ['Maria K.', 'Pastor Weber', 'Hans Q.', 'Anna M.', 'Volunteer Team']
        }
        
        calendar_df = pd.DataFrame(calendar_data)
        
        # Color-code by area
        def color_area(val):
            colors = {
                'Culture': 'background-color: #FFE4E1',
                'Church': 'background-color: #E6F3FF', 
                'District': 'background-color: #E8F5E8',
                'Community': 'background-color: #FFF8DC'
            }
            return colors.get(val, '')
        
        styled_df = calendar_df.style.map(color_area, subset=['Area'])
        st.dataframe(styled_df, use_container_width=True)
    
    with col2:
        st.metric("This Week's Events", "5")
        st.metric("Active Areas", "3")
        st.metric("Total Participants", "180")
        
        # Event distribution
        area_counts = calendar_df['Area'].value_counts()
        fig = px.pie(
            values=area_counts.values,
            names=area_counts.index,
            title="Events by Area"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Calendar filters
    with st.expander("🔍 Calendar Filters"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            area_filter = st.multiselect("Filter by Area", 
                ["Culture", "Church", "District", "Community"], 
                default=["Culture", "Church", "District", "Community"])
        
        with col2:
            date_from = st.date_input("From Date", value=datetime.now().date())
            
        with col3:
            date_to = st.date_input("To Date", value=datetime.now().date() + timedelta(days=30))

with tab3:
    st.subheader("📊 Cross-Area Analytics")
    
    # Combined metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Active Users", "89")
        st.metric("Weekly Engagement", "73%")
        
    with col2:
        st.metric("Cross-Area Events", "12")
        st.metric("Collaboration Rate", "85%")
        
    with col3:
        st.metric("Total Volunteers", "45")
        st.metric("Resource Sharing", "67%")
        
    with col4:
        st.metric("Community Reach", "324")
        st.metric("Impact Score", "8.4/10")
    
    # Analytics charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Activity by area
        activity_data = {
            'Area': ['Culture', 'Church', 'District', 'Community'],
            'Events': [15, 12, 8, 10],
            'Participants': [180, 95, 67, 85],
            'Volunteers': [12, 8, 15, 10]
        }
        
        activity_df = pd.DataFrame(activity_data)
        
        fig1 = px.bar(
            activity_df,
            x='Area',
            y=['Events', 'Volunteers'],
            title="Activity Overview by Area",
            barmode='group'
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Collaboration network
        collaboration_data = {
            'Partnership': ['Culture-Church', 'Church-District', 'District-Community', 'Culture-Community'],
            'Joint Events': [4, 6, 8, 3],
            'Shared Resources': [12, 15, 20, 8]
        }
        
        collab_df = pd.DataFrame(collaboration_data)
        
        fig2 = px.scatter(
            collab_df,
            x='Joint Events',
            y='Shared Resources',
            size='Joint Events',
            color='Partnership',
            title="Area Collaboration Matrix"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Success metrics
    st.subheader("🎯 Success Metrics")
    
    metrics_data = {
        'KPI': ['Community Engagement', 'Event Attendance', 'Volunteer Retention', 'Resource Efficiency', 'Cross-Area Collaboration'],
        'Current': ['73%', '85%', '91%', '67%', '78%'],
        'Target': ['80%', '90%', '95%', '75%', '85%'],
        'Trend': ['↗️', '↗️', '→', '↗️', '↗️']
    }
    
    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(metrics_df, use_container_width=True)

with tab4:
    st.subheader("🔧 Community Tools")
    
    # Tool categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Communication Tools**")
        
        if st.button("📧 Send Newsletter", use_container_width=True):
            st.info("Newsletter composer would open here")
            
        if st.button("📱 SMS Broadcast", use_container_width=True):
            st.info("SMS broadcast tool would open here")
            
        if st.button("📋 Survey Creator", use_container_width=True):
            st.info("Survey creation tool would open here")
            
        if st.button("📊 Feedback Forms", use_container_width=True):
            st.info("Feedback form builder would open here")
    
    with col2:
        st.write("**Management Tools**")
        
        if st.button("👥 User Management", use_container_width=True):
            st.info("User management panel would open here")
            
        if st.button("📈 Report Generator", use_container_width=True):
            st.info("Report generation tool would open here")
            
        if st.button("🔄 Data Export", use_container_width=True):
            st.info("Data export utilities would open here")
            
        if st.button("⚙️ System Settings", use_container_width=True):
            st.info("System configuration would open here")
    
    # Quick stats
    st.subheader("📈 Quick Statistics")
    
    quick_stats = {
        'Metric': ['Messages Sent Today', 'Active Sessions', 'Data Updates', 'System Uptime'],
        'Value': ['23', '12', '7', '99.9%'],
        'Change': ['+15%', '+8%', '+2', '→']
    }
    
    stats_df = pd.DataFrame(quick_stats)
    st.dataframe(stats_df, use_container_width=True)
    
    # System health
    with st.expander("🔍 System Health"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Database Status", "✅ Healthy")
            st.metric("API Response", "45ms")
            
        with col2:
            st.metric("Active Users", "23")
            st.metric("Memory Usage", "67%")
            
        with col3:
            st.metric("Error Rate", "0.02%")
            st.metric("Last Backup", "2h ago")

# === Footer ===
st.markdown("---")
st.info("💡 **Community Dashboard** - Central hub for communication and collaboration across all Lukas areas. Data updates in real-time.")
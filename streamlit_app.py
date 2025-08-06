import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os

# === Page Configuration ===
st.set_page_config(
    page_title="Lukas Dashboard",
    page_icon="🕊️",
    layout="wide"
)

# === Load Configuration with Error Handling ===
config_path = "config/authenticator.yaml"

try:
    if not os.path.exists(config_path):
        st.error("❌ Configuration file not found!")
        st.code("Expected path: config/authenticator.yaml")
        st.stop()
    
    with open(config_path, 'r', encoding='utf-8') as file:
        config = yaml.load(file, Loader=SafeLoader)
        
    if not config or 'credentials' not in config:
        st.error("❌ Invalid configuration file!")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Error loading configuration: {e}")
    st.stop()

# === Initialize Authenticator (Compatible with older version) ===
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
except Exception as e:
    st.error(f"❌ Authentication error: {e}")
    st.stop()

# === Login Interface (Fixed for stable version) ===
try:
    name, authentication_status, username = authenticator.login('Login', 'main')
except Exception as e:
    st.error(f"❌ Login method error: {e}")
    st.info("Trying alternative login method...")
    try:
        # Alternative for newer versions
        result = authenticator.login(location='main')
        if result and len(result) == 3:
            name, authentication_status, username = result
        else:
            name, authentication_status, username = None, None, None
    except:
        name, authentication_status, username = None, None, None

if authentication_status is False:
    st.error("❌ Login failed - Please check username and password")
    
elif authentication_status is None:
    st.warning("🔐 Please log in")
    with st.expander("ℹ️ Demo Accounts", expanded=False):
        st.info("""
        **Available Test Accounts:**
        - Admin: `admin_user` / `admin123`
        - Culture: `kultur_maria` / `kultur123`  
        - District: `quartier_hans` / `quartier123`
        """)
        
elif authentication_status:
    # === Successful Login ===
    try:
        authenticator.logout('Logout', 'sidebar')
    except:
        try:
            authenticator.logout(location='sidebar')
        except:
            st.sidebar.button("Logout (manual)")
    
    st.sidebar.success(f"Welcome, {name} 👋")
    
    # === Get User Role ===
    try:
        role = config['credentials']['usernames'][username]['role']
        st.sidebar.info(f"Role: {role.title()}")
    except KeyError:
        st.error("❌ User role not found!")
        st.stop()

    # === Main Navigation ===
    st.title("📊 LUKAS IMPACT DASHBOARD")
    st.markdown("*Wir für Lukas e.V. | Karlsruhe*")
    st.markdown("---")

    # === Role-based Navigation ===
    if role == "admin":
        st.subheader("🔧 Administrator Area")
        st.success("You have full access to all modules")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎭 Culture Dashboard", use_container_width=True):
                st.switch_page("pages/1_Kultur.py")
            if st.button("⛪ Church Dashboard", use_container_width=True):
                st.switch_page("pages/2_Kirche.py")
                
        with col2:
            if st.button("🏘️ District Dashboard", use_container_width=True):
                st.switch_page("pages/3_Quartier.py")
            if st.button("💬 Community Dashboard", use_container_width=True):
                st.switch_page("pages/4_Community.py")
                
    elif role == "kultur":
        st.subheader("🎭 Culture Area")
        if st.button("🎶 Go to Culture Dashboard", use_container_width=True):
            st.switch_page("pages/1_Kultur.py")
            
    elif role == "quartier":
        st.subheader("🏘️ District Area")
        if st.button("🏡 Go to District Dashboard", use_container_width=True):
            st.switch_page("pages/3_Quartier.py")
            
    else:
        st.warning("⚠️ Unknown role - Please contact administrator")

    # === Status Information ===
    with st.expander("ℹ️ System Information"):
        st.write(f"**Logged in user:** {name}")
        st.write(f"**Role:** {role}")
        st.write(f"**Username:** {username}")
        
    st.markdown("---")
    st.caption("Dashboard Version 1.0 | Developed for Wir für Lukas e.V.")
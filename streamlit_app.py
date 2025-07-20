import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# === Authentifizierung laden ===
with open("config/authenticator.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# === Login-Fenster ===
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Login fehlgeschlagen")
elif authentication_status is None:
    st.warning("Bitte logge dich ein")
elif authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.success(f"Willkommen, {name} 👋")

    # === Navigation & Rollenprüfung ===
    role = config['credentials']['usernames'][username]['role']

    st.title("📊 LUKAS IMPACT DASHBOARD")

    if role == "admin":
        st.subheader("🧭 Volle Admin-Ansicht (alle Bereiche sichtbar)")
        st.page_link("pages/1_Kultur.py", label="🎶 Kultur", icon="🎭")
        st.page_link("pages/2_Kirche.py", label="⛪ Kirche", icon="🛐")
        st.page_link("pages/3_Quartier.py", label="🏡 Quartier", icon="🏘")
        st.page_link("pages/4_Community.py", label="💬 Kommunikation", icon="💬")
    elif role == "kultur":
        st.page_link("pages/1_Kultur.py", label="🎶 Kultur", icon="🎭")
    elif role == "quartier":
        st.page_link("pages/3_Quartier.py", label="🏡 Quartier", icon="🏘")
    else:
        st.warning("Noch keine Rolle zugewiesen.")

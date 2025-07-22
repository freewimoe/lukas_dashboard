import streamlit as st
import pandas as pd

st.title("🎶 Kultur-Dashboard")

st.markdown("Hier können Sie Daten zu Veranstaltungen analysieren und Prognosen generieren.")

# Platzhalter für CSV-Daten
uploaded_file = st.file_uploader("Lade Veranstaltungsdaten hoch (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

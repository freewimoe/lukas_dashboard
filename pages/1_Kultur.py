import streamlit as st
import pandas as pd
import os

st.title("🎼 Kultur-Dashboard")
st.markdown("Hier können Sie Daten zu Veranstaltungen analysieren und Prognosen generieren.")

# 🔽 CSV-Datei direkt aus dem data/-Ordner laden
file_path = os.path.join("data", "kultur_events.csv")
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.success("📄 Dummy-Daten wurden erfolgreich geladen!")
    st.dataframe(df)
else:
    st.warning("⚠️ Datei 'kultur_events.csv' nicht gefunden.")
    st.error("Die Datei 'kultur_events.csv' ist nicht im 'data/'-Ordner vorhanden. Bitte stellen Sie sicher, dass die Datei existiert.")
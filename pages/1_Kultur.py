import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score, mean_absolute_error
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Kultur Dashboard", 
    page_icon="🎭", 
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🎭 Kultur-Dashboard - Event Analytics")
st.markdown("**Analysiere Veranstaltungsdaten und erstelle Prognosen für kulturelle Events**")

# Sidebar for data source and settings
with st.sidebar:
    st.header("📊 Datenquelle & Einstellungen")
    
    # Data upload options
    data_source = st.radio(
        "Datenquelle wählen:",
        ["📁 CSV-Datei hochladen", "📋 Vorhandene Daten verwenden"]
    )
    
    if data_source == "📁 CSV-Datei hochladen":
        uploaded_file = st.file_uploader("CSV-Datei auswählen", type="csv")
        data_loaded = uploaded_file is not None
        if data_loaded:
            try:
                df_raw = pd.read_csv(uploaded_file)
                st.success(f"✅ Datei geladen: {len(df_raw)} Einträge")
            except Exception as e:
                st.error(f"❌ Fehler beim Laden: {e}")
                data_loaded = False
    else:
        # Use existing data
        try:
            # Try both possible CSV files
            if pd.io.common.file_exists("data/kultur_events.csv"):
                df_raw = pd.read_csv("data/kultur_events.csv")
            elif pd.io.common.file_exists("data/kultur.csv") and not pd.read_csv("data/kultur.csv").empty:
                df_raw = pd.read_csv("data/kultur.csv")
            else:
                raise FileNotFoundError("No valid data file found")
            data_loaded = True
            st.info(f"📋 Vorhandene Daten: {len(df_raw)} Events")
            
            # Show column info
            st.markdown("**📊 Vorhandene Spalten:**")
            for col in df_raw.columns:
                st.text(f"• {col}")
                
        except FileNotFoundError:
            st.error("❌ data/kultur_events.csv nicht gefunden")
            data_loaded = False
        except Exception as e:
            st.error(f"❌ Fehler: {e}")
            data_loaded = False

# Main content
if data_loaded:
    # Data preprocessing - adapt to your column structure
    try:
        df = df_raw.copy()
        
        # Rename columns to match expected format
        column_mapping = {
            'date': 'Datum',
            'title': 'Veranstaltung', 
            'category': 'Kategorie',
            'visitors': 'Teilnehmer',
            'ticket_price': 'Ticket_Preis',
            'venue': 'Veranstaltungsort',
            'organizer': 'Organisator',
            'duration_min': 'Dauer_Min'
        }
        
        # Apply renaming if columns exist
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df[new_col] = df[old_col]
        
        # Convert date
        df['Datum'] = pd.to_datetime(df['Datum'])
        
        # Calculate derived metrics (estimates since we don't have costs/revenue)
        df['Einnahmen_Geschätzt'] = df['Teilnehmer'] * df.get('Ticket_Preis', 10)  # Default 10€ if no price
        df['Kosten_Geschätzt'] = df['Einnahmen_Geschätzt'] * 0.3  # Estimate 30% costs
        df['Gewinn_Geschätzt'] = df['Einnahmen_Geschätzt'] - df['Kosten_Geschätzt']
        df['ROI_Geschätzt'] = (df['Gewinn_Geschätzt'] / df['Kosten_Geschätzt']) * 100
        
        # Additional time features
        df['Monat'] = df['Datum'].dt.month
        df['Wochentag'] = df['Datum'].dt.dayofweek
        df['Jahr'] = df['Datum'].dt.year
        df['Saison'] = df['Datum'].dt.month.map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Frühling', 4: 'Frühling', 5: 'Frühling',
            6: 'Sommer', 7: 'Sommer', 8: 'Sommer',
            9: 'Herbst', 10: 'Herbst', 11: 'Herbst'
        })
        
        data_processed = True
        
    except Exception as e:
        st.error(f"❌ Fehler bei der Datenverarbeitung: {e}")
        st.write("**Vorhandene Spalten:**", df_raw.columns.tolist())
        data_processed = False

    if data_processed:
        # Main dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Dashboard", "📈 Analysen", "🔮 Prognosen", "📋 Rohdaten"
        ])
        
        with tab1:
            st.subheader("🎯 Übersicht")
            
            # KPI metrics in columns
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_participants = df['Teilnehmer'].sum()
                avg_participants = df['Teilnehmer'].mean()
                st.metric(
                    "Gesamtteilnehmer", 
                    f"{total_participants:,}",
                    delta=f"⌀ {avg_participants:.0f} pro Event"
                )
            
            with col2:
                total_events = len(df)
                unique_categories = df['Kategorie'].nunique()
                st.metric(
                    "Anzahl Events", 
                    f"{total_events}",
                    delta=f"{unique_categories} Kategorien"
                )
            
            with col3:
                if 'Ticket_Preis' in df.columns:
                    avg_price = df['Ticket_Preis'].mean()
                    st.metric(
                        "Ø Ticket-Preis", 
                        f"{avg_price:.2f} €",
                        delta=f"Max: {df['Ticket_Preis'].max():.2f} €"
                    )
                else:
                    st.metric("Geschätzte Einnahmen", f"{df['Einnahmen_Geschätzt'].sum():,.0f} €")
            
            with col4:
                if 'Dauer_Min' in df.columns:
                    avg_duration = df['Dauer_Min'].mean()
                    st.metric(
                        "Ø Dauer", 
                        f"{avg_duration:.0f} min",
                        delta=f"{avg_duration/60:.1f}h"
                    )
                else:
                    unique_venues = df['Veranstaltungsort'].nunique() if 'Veranstaltungsort' in df.columns else 0
                    st.metric("Veranstaltungsorte", f"{unique_venues}")
            
            st.divider()
            
            # Main visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                # Participants by category
                category_data = df.groupby('Kategorie')['Teilnehmer'].sum().reset_index().sort_values('Teilnehmer', ascending=False)
                fig_cat = px.bar(
                    category_data,
                    x='Kategorie', y='Teilnehmer',
                    title="🎭 Teilnehmer nach Kategorie",
                    color='Teilnehmer',
                    color_continuous_scale='viridis',
                    text='Teilnehmer'
                )
                fig_cat.update_traces(texttemplate='%{text}', textposition='outside')
                fig_cat.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_cat, use_container_width=True)
            
            with col2:
                # Timeline of participants
                monthly_data = df.groupby(df['Datum'].dt.to_period('M')).agg({
                    'Teilnehmer': 'sum',
                    'Veranstaltung': 'count'
                }).reset_index()
                monthly_data['Datum'] = monthly_data['Datum'].astype(str)
                
                fig_timeline = px.line(
                    monthly_data, x='Datum', y='Teilnehmer',
                    title="📈 Teilnehmerentwicklung über Zeit",
                    markers=True,
                    line_shape='spline'
                )
                fig_timeline.update_layout(height=400)
                st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Additional visualizations based on available data
            if 'Veranstaltungsort' in df.columns:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Top venues
                    venue_data = df.groupby('Veranstaltungsort')['Teilnehmer'].sum().reset_index().sort_values('Teilnehmer', ascending=False).head(8)
                    fig_venue = px.bar(
                        venue_data, y='Veranstaltungsort', x='Teilnehmer',
                        title="🏛️ Top Veranstaltungsorte",
                        orientation='h',
                        color='Teilnehmer',
                        color_continuous_scale='plasma'
                    )
                    st.plotly_chart(fig_venue, use_container_width=True)
                
                with col2:
                    # Organizers
                    if 'Organisator' in df.columns:
                        organizer_data = df.groupby('Organisator')['Teilnehmer'].sum().reset_index().sort_values('Teilnehmer', ascending=False).head(8)
                        fig_org = px.pie(
                            organizer_data, values='Teilnehmer', names='Organisator',
                            title="🎪 Teilnehmer nach Organisator"
                        )
                        st.plotly_chart(fig_org, use_container_width=True)
        
        with tab2:
            st.subheader("📈 Detaillierte Analysen")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Time series analysis
                df_sorted = df.sort_values('Datum')
                fig_detailed = px.scatter(
                    df_sorted, x='Datum', y='Teilnehmer',
                    color='Kategorie', size='Dauer_Min' if 'Dauer_Min' in df.columns else None,
                    title="🎯 Event-Performance über Zeit",
                    hover_data=['Veranstaltung', 'Veranstaltungsort'] if 'Veranstaltungsort' in df.columns else ['Veranstaltung'],
                    size_max=20
                )
                fig_detailed.update_layout(height=500)
                st.plotly_chart(fig_detailed, use_container_width=True)
            
            with col2:
                st.subheader("📊 Top Events")
                
                # Top events by participants
                top_events = df.nlargest(10, 'Teilnehmer')[['Veranstaltung', 'Kategorie', 'Teilnehmer', 'Datum']]
                
                for idx, (_, row) in enumerate(top_events.iterrows(), 1):
                    st.markdown(f"""
                    **{idx}. {row['Veranstaltung'][:30]}{'...' if len(row['Veranstaltung']) > 30 else ''}**  
                    📂 {row['Kategorie']} | 👥 {row['Teilnehmer']} | 📅 {row['Datum'].strftime('%d.%m.%Y')}
                    """)
                    st.markdown("---")
            
            # Seasonal analysis
            st.subheader("🌸 Saisonale und Wochentag-Analyse")
            col1, col2 = st.columns(2)
            
            with col1:
                seasonal_data = df.groupby('Saison')['Teilnehmer'].mean().reset_index()
                fig_seasonal = px.bar(
                    seasonal_data, x='Saison', y='Teilnehmer',
                    title="🌺 Ø Teilnehmer nach Saison",
                    color='Teilnehmer',
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig_seasonal, use_container_width=True)
            
            with col2:
                # Day of week analysis
                weekday_names = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
                weekday_data = df.groupby('Wochentag')['Teilnehmer'].mean().reset_index()
                weekday_data['Tag'] = weekday_data['Wochentag'].map(dict(enumerate(weekday_names)))
                
                fig_weekday = px.bar(
                    weekday_data, x='Tag', y='Teilnehmer',
                    title="📅 Ø Teilnehmer nach Wochentag",
                    color='Teilnehmer',
                    color_continuous_scale='plasma'
                )
                fig_weekday.update_xaxes(tickangle=45)
                st.plotly_chart(fig_weekday, use_container_width=True)
        
        with tab3:
            st.subheader("🔮 ML-basierte Prognosen")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("### 🎯 Teilnehmer-Prognose")
                
                # ML Model preparation
                le_kategorie = LabelEncoder()
                df_ml = df.copy()
                df_ml['Kategorie_encoded'] = le_kategorie.fit_transform(df_ml['Kategorie'])
                
                # Features for the model
                features = ['Kategorie_encoded', 'Monat', 'Wochentag']
                if 'Dauer_Min' in df.columns:
                    features.append('Dauer_Min')
                
                X = df_ml[features]
                y_teilnehmer = df_ml['Teilnehmer']
                
                # Train model
                model_teilnehmer = LinearRegression()
                model_teilnehmer.fit(X, y_teilnehmer)
                
                # Model performance
                r2_teilnehmer = r2_score(y_teilnehmer, model_teilnehmer.predict(X))
                
                st.markdown(f"""
                **🤖 Modell-Performance:**
                - Teilnehmer R²: {r2_teilnehmer:.3f}
                - Features: {len(features)}
                """)
                
                # Prediction interface
                st.markdown("### 🎮 Prognose-Parameter")
                prognose_kategorie = st.selectbox("🎭 Kategorie", df['Kategorie'].unique())
                prognose_monat = st.slider("📅 Monat", 1, 12, 7, help="1=Januar, 12=Dezember")
                prognose_wochentag = st.slider("📆 Wochentag", 0, 6, 5, help="0=Montag, 6=Sonntag")
                
                if 'Dauer_Min' in df.columns:
                    prognose_dauer = st.slider("⏱️ Dauer (Min)", int(df['Dauer_Min'].min()), int(df['Dauer_Min'].max()), int(df['Dauer_Min'].mean()))
                
                if st.button("🔮 Prognose erstellen", type="primary"):
                    # Encode selected category
                    kategorie_encoded = le_kategorie.transform([prognose_kategorie])[0]
                    
                    # Make prediction
                    if 'Dauer_Min' in df.columns:
                        pred_features = [[kategorie_encoded, prognose_monat, prognose_wochentag, prognose_dauer]]
                    else:
                        pred_features = [[kategorie_encoded, prognose_monat, prognose_wochentag]]
                    
                    pred_teilnehmer = model_teilnehmer.predict(pred_features)[0]
                    
                    # Display results
                    st.markdown("### 📊 Prognose-Ergebnis")
                    st.success(f"**Prognostizierte Teilnehmer:** {max(0, pred_teilnehmer):.0f}")
                    
                    # Additional insights based on historical data
                    similar_events = df[df['Kategorie'] == prognose_kategorie]
                    if len(similar_events) > 0:
                        avg_similar = similar_events['Teilnehmer'].mean()
                        comparison = ((pred_teilnehmer - avg_similar) / avg_similar) * 100
                        
                        st.info(f"""
                        **Vergleich zu ähnlichen Events:**
                        - Durchschnitt {prognose_kategorie}: {avg_similar:.0f} Teilnehmer
                        - Prognose ist {abs(comparison):.1f}% {'höher' if comparison > 0 else 'niedriger'}
                        """)
            
            with col2:
                st.markdown("### 📈 Trend-Analyse")
                
                # Show trends by category
                trend_data = df.groupby(['Jahr', 'Kategorie'])['Teilnehmer'].mean().reset_index()
                
                if len(trend_data) > 0:
                    fig_trends = px.line(
                        trend_data, x='Jahr', y='Teilnehmer',
                        color='Kategorie', 
                        title="📈 Teilnehmer-Trends nach Kategorie",
                        markers=True
                    )
                    st.plotly_chart(fig_trends, use_container_width=True)
                
                # Monthly distribution
                monthly_avg = df.groupby('Monat')['Teilnehmer'].mean().reset_index()
                month_names = ['Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun',
                              'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
                monthly_avg['Monat_Name'] = monthly_avg['Monat'].map(dict(enumerate(month_names, 1)))
                
                fig_monthly = px.line(
                    monthly_avg, x='Monat_Name', y='Teilnehmer',
                    title="📅 Durchschnittliche Teilnehmer nach Monat",
                    markers=True
                )
                st.plotly_chart(fig_monthly, use_container_width=True)
        
        with tab4:
            st.subheader("📋 Rohdaten & Export")
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_kategorie = st.multiselect("🎭 Filter Kategorie", df['Kategorie'].unique())
                filter_jahr = st.multiselect("📅 Filter Jahr", sorted(df['Jahr'].unique()))
            with col2:
                min_participants = st.number_input("👥 Min. Teilnehmer", value=0)
                max_participants = st.number_input("👥 Max. Teilnehmer", value=int(df['Teilnehmer'].max()))
            with col3:
                if 'Veranstaltungsort' in df.columns:
                    filter_venue = st.multiselect("🏛️ Filter Veranstaltungsort", df['Veranstaltungsort'].unique())
                else:
                    filter_venue = []
            
            # Apply filters
            filtered_df = df.copy()
            if filter_kategorie:
                filtered_df = filtered_df[filtered_df['Kategorie'].isin(filter_kategorie)]
            if filter_jahr:
                filtered_df = filtered_df[filtered_df['Jahr'].isin(filter_jahr)]
            if filter_venue and 'Veranstaltungsort' in df.columns:
                filtered_df = filtered_df[filtered_df['Veranstaltungsort'].isin(filter_venue)]
            
            filtered_df = filtered_df[
                (filtered_df['Teilnehmer'] >= min_participants) & 
                (filtered_df['Teilnehmer'] <= max_participants)
            ]
            
            st.markdown(f"**📊 Angezeigt: {len(filtered_df)} von {len(df)} Events**")
            
            # Display relevant columns
            display_columns = ['Datum', 'Veranstaltung', 'Kategorie', 'Teilnehmer']
            if 'Veranstaltungsort' in df.columns:
                display_columns.append('Veranstaltungsort')
            if 'Organisator' in df.columns:
                display_columns.append('Organisator')
            if 'Ticket_Preis' in df.columns:
                display_columns.append('Ticket_Preis')
            if 'Dauer_Min' in df.columns:
                display_columns.append('Dauer_Min')
            
            # Display data
            st.dataframe(
                filtered_df[display_columns].sort_values('Datum', ascending=False),
                use_container_width=True,
                height=400
            )
            
            # Export options
            col1, col2 = st.columns(2)
            with col1:
                csv_data = filtered_df[display_columns].to_csv(index=False)
                st.download_button(
                    "📥 Gefilterte Daten als CSV",
                    csv_data,
                    "kultur_daten_gefiltert.csv",
                    "text/csv"
                )
            
            with col2:
                # Summary statistics
                summary_stats = filtered_df[['Teilnehmer']].describe()
                if 'Ticket_Preis' in df.columns:
                    summary_stats = pd.concat([summary_stats, filtered_df[['Ticket_Preis']].describe()], axis=1)
                
                summary_csv = summary_stats.to_csv()
                st.download_button(
                    "📊 Statistik-Summary",
                    summary_csv,
                    "kultur_statistik.csv",
                    "text/csv"
                )

else:
    st.info("👆 Bitte wähle eine Datenquelle im Sidebar, um zu beginnen.")
    
    st.markdown("""
    ## 📋 Unterstützte CSV-Formate
    
    Das Dashboard erkennt automatisch folgende Spalten:
    
    | Deine Spalte | Dashboard verwendet | Beschreibung |
    |--------------|-------------------|--------------|
    | `date` | Datum | Event-Datum |
    | `title` | Veranstaltung | Name des Events |
    | `category` | Kategorie | Art der Veranstaltung |
    | `visitors` | Teilnehmer | Anzahl Besucher |
    | `ticket_price` | Ticket-Preis | Preis pro Ticket |
    | `venue` | Veranstaltungsort | Ort des Events |
    | `organizer` | Organisator | Verantwortlicher |
    | `duration_min` | Dauer | Event-Dauer in Minuten |
    
    ### 🎯 Dashboard Features:
    - 📊 **Automatische Datenanalyse** mit deinen vorhandenen Spalten
    - 🤖 **Machine Learning** für Teilnehmer-Prognosen
    - 📈 **Trend-Analysen** nach Zeit, Kategorie, Ort
    - 🔍 **Interaktive Filter** und Datenexport
    """)
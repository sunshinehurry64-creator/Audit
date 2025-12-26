import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="Quantum Audit Dashboard 2025", layout="wide")

st.title("🛡️ Quantum Readiness Audit Dashboard")
st.markdown("Analisis kesiapan kriptografi institusi Indonesia menghadapi era Pasca-Kuantum[cite: 185].")

# Sidebar untuk Input
st.sidebar.header("Upload Data Hasil Audit")
uploaded_file = st.sidebar.file_uploader("Upload CSV hasil scanner", type=["csv"])

if uploaded_file:
    df = pd.DataFrame(pd.read_csv(uploaded_file))

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Website Diaudit", len(df))
    col2.metric("Quantum-Safe (A+)", len(df[df['grade'] == 'A+']))
    col3.metric("Classically Secure (A)", len(df[df['grade'] == 'A']))
    col4.metric("At Risk (C)", len(df[df['grade'] == 'C']))

    st.divider()

    # Visualisasi
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Distribusi Grade Keamanan")
        fig_grade = px.pie(df, names='grade', color='grade', 
                           color_discrete_map={'A+':'#00CC96', 'A':'#636EFA', 'B':'#FECB52', 'C':'#EF553B'})
        st.plotly_chart(fig_grade)

    with c2:
        st.subheader("Kesiapan PQC")
        fig_pqc = px.bar(df, x='pqc_status', color='pqc_status', barmode='group')
        st.plotly_chart(fig_pqc)

    # Tabel Data
    st.subheader("Detail Temuan Audit")
    st.dataframe(df.style.highlight_max(axis=0, subset=['key_size']))

else:
    st.info("Silakan jalankan scanner.py terlebih dahulu untuk mendapatkan file hasil_audit_2025.csv")
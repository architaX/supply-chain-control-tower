import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supply Chain Control Tower", layout="wide")

st.title("🚀 Supply Chain Control Tower")
st.markdown("Real-time monitoring and Supplier Risk Analysis")

# --- Sidebar Configuration ---
API_URL = "http://127.0.0.1:8000"

# --- Metrics Section ---
st.header("Key Performance Indicators")
col1, col2, col3 = st.columns(3)

try:
    otif_res = requests.get(f"{API_URL}/otif").json()
    delay_res = requests.get(f"{API_URL}/avg-delay").json()
    
    col1.metric("OTIF Score", otif_res['value'])
    col2.metric("Avg Delivery Days", f"{delay_res['value']} Days")
    col3.metric("System Status", "Connected ✅")
except:
    st.error("Could not connect to FastAPI. Is uvicorn running?")

# --- Risk Analysis Section ---
st.divider()
st.header("Supplier Risk Assessment (ML)")

supplier_id = st.number_input("Enter Supplier ID to analyze", min_value=1, max_value=100, value=1)

if st.button("Run AI Risk Prediction"):
    risk_res = requests.get(f"{API_URL}/supplier-risk/{supplier_id}")
    if risk_res.status_code == 200:
        data = risk_res.json()
        risk = data['risk_assessment']
        
        if risk == "High Risk":
            st.error(f"⚠️ Supplier {supplier_id} is classified as: {risk}")
        else:
            st.success(f"✅ Supplier {supplier_id} is classified as: {risk}")
            
        # Show stats in a table
        st.write("Supplier Performance Averages:")
        st.table(pd.DataFrame([data['stats']]))
    else:
        st.warning("Supplier data not found.")

# --- Visualizations ---
st.divider()
st.header("Delivery Performance Overview")
df = pd.read_csv("data/Transactions.csv")
fig = px.histogram(df[df['Type']=='Purchase'], x="Actual_Delivery_Days", 
                   title="Distribution of Delivery Times",
                   color_discrete_sequence=['#636EFA'])
st.plotly_chart(fig, use_container_width=True)
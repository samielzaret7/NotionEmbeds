import streamlit as st
import requests

# 🔐 Load secrets
NOTION_TOKEN = st.secrets["notion_token"]
DATABASE_ID = st.secrets["database_id"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
}

def get_metrics():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    payload = {
    "sorts": [
        {
            "timestamp": "created_time",
            "direction": "descending"
        }
    ],
    "page_size": 1
}

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if "results" not in data or not data["results"]:
        return "N/A", "N/A"

    result = data["results"][0]
    props = result["properties"]

    # 🧮 Total Hours (formula string)
    hours = props['Total Hours']['formula']['string'] if props["Total Hours"]["formula"]["string"] else "N/A"

    # 💵 Total Income (number)
    income_val = props['Total Income']['rollup']['number']
    income = f"${income_val:,.2f}" if income_val is not None else "N/A"

    return hours, income

# UI
st.set_page_config(layout="wide")
hours, income = get_metrics()

col1, col2 = st.columns(2)
with col1:
    st.metric("⏱️ Total Hours", hours)
with col2:
    st.metric("💵 Total Income", income)

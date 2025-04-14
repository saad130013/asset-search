
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# تحميل البيانات
df = pd.read_excel("assetv4.xlsx", header=1)

# دالة تنظيف
def normalize(value):
    if pd.isna(value):
        return ""
    return str(value).strip().replace('\u200f', '').replace('\u202a', '').replace('\xa0', '').replace(" ", "")

# إعداد الصفحة
st.set_page_config(page_title="Asset Lookup System", layout="wide", page_icon="📁")
st.title("🔍 Asset Lookup System")

# البحث متعدد المعايير
st.sidebar.header("🔎 Filters")

tag_number = st.sidebar.text_input("Tag Number")
entity = st.sidebar.selectbox("Entity", [""] + sorted(df["Entity"].dropna().unique().astype(str)))
city = st.sidebar.selectbox("City", [""] + sorted(df["City"].dropna().unique().astype(str)))
min_cost = st.sidebar.number_input("Minimum Cost", min_value=0, value=0)
max_life = st.sidebar.number_input("Max Useful Life", min_value=0, value=100)

# تطبيق الفلاتر
filtered_df = df.copy()

if tag_number:
    filtered_df = filtered_df[filtered_df["Tag number"].astype(str).apply(normalize) == normalize(tag_number)]
if entity:
    filtered_df = filtered_df[filtered_df["Entity"].astype(str) == entity]
if city:
    filtered_df = filtered_df[filtered_df["City"].astype(str) == city]
if min_cost > 0:
    filtered_df = filtered_df[pd.to_numeric(filtered_df["Cost"], errors='coerce') >= min_cost]
if max_life < 100:
    filtered_df = filtered_df[pd.to_numeric(filtered_df["Useful Life"], errors='coerce') <= max_life]

if not filtered_df.empty:
    record = filtered_df.iloc[0]
    st.success("✅ Asset found. See details below:")

    # معلومات الأصل العامة
    general_info = {
        "Tag Number": record.get("Tag number", "N/A"),
        "Asset Description": record.get("Asset Description", "N/A"),
        "Entity": record.get("Entity", "N/A"),
        "Entity Code": record.get("Entity Code", "N/A"),
        "Cost": record.get("Cost", "N/A"),
        "Useful Life": record.get("Useful Life", "N/A"),
        "Remaining Life": record.get("Remaining Life", "N/A"),
        "City": record.get("City", "N/A"),
        "Region": record.get("Region", "N/A"),
        "National Address ID": record.get("National Address ID", "N/A"),
        "Building Number": record.get("Building Number", "N/A"),
        "Floors Number": record.get("Floors Number", "N/A"),
        "Room/office Number": record.get("Room/office Number", "N/A"),
        "Geographical Coordinates": record.get("Geographical Coordinates", "N/A"),
        "Valuation Method": record.get("Valuation Method", "N/A"),
        "Comments": record.get("Comments", "N/A")
    }

    # معلومات التصنيف المحاسبي
    accounting_info = {
        "Level 1 Code": record.get("Level 1 FA Module Code", "N/A"),
        "Level 1 Desc (AR)": record.get("Level 1 FA Module - Arabic Description", "N/A"),
        "Level 1 Desc (EN)": record.get("Level 1 FA Module - English Description", "N/A"),
        "Level 2 Code": record.get("Level 2 FA Module Code", "N/A"),
        "Level 2 Desc (AR)": record.get("Level 2 FA Module - Arabic Description", "N/A"),
        "Level 2 Desc (EN)": record.get("Level 2 FA Module - English Description", "N/A"),
        "Level 3 Code": record.get("Level 3 FA Module Code", "N/A"),
        "Level 3 Desc (AR)": record.get("Level 3 FA Module - Arabic Description", "N/A"),
        "Level 3 Desc (EN)": record.get("Level 3 FA Module - English Description", "N/A"),
        "Accounting Group Code": record.get("accounting group Code", "N/A"),
        "Accounting Group Desc (AR)": record.get("accounting group Arabic Description", "N/A"),
        "Accounting Group Desc (EN)": record.get("accounting group English Description", "N/A"),
        "Asset Code for Accounting": record.get("Asset Code For Accounting Purpose", "N/A")
    }

    st.subheader("📋 General Asset Information")
    st.dataframe(pd.DataFrame(general_info.items(), columns=["Field", "Value"]))

    st.subheader("📊 Accounting Classification")
    st.dataframe(pd.DataFrame(accounting_info.items(), columns=["Field", "Value"]))

    # عرض الخريطة التفاعلية
    coords = record.get("Geographical Coordinates")
    if isinstance(coords, str) and "," in coords:
        try:
            lat, lon = map(float, coords.split(","))
            m = folium.Map(location=[lat, lon], zoom_start=16)
            folium.Marker([lat, lon], tooltip="Asset Location").add_to(m)
            st.subheader("🗺️ Asset Location on Map")
            st_folium(m, width=700, height=500)
        except:
            st.warning("⚠️ Could not parse coordinates.")
else:
    st.warning("🔍 No matching assets found. Adjust your filters and try again.")

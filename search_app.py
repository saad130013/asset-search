
import streamlit as st
import pandas as pd

# تحميل البيانات مع تحديد الصف 1 كرأس
df = pd.read_excel("assetv4.xlsx", header=1)

# اسم العمود الصحيح
search_column = 'Tag number'

# دالة تنظيف
def normalize(value):
    if pd.isna(value):
        return ""
    return str(value).strip().replace('\u200f', '').replace('\u202a', '').replace('\xa0', '').replace(" ", "")

# إعداد الصفحة
st.set_page_config(page_title="Asset Lookup System", layout="centered", page_icon="📁")
st.title("🔍 Asset Lookup System")

# إدخال رقم الأصل
asset_id = st.text_input("📌 Enter Tag Number:")

if asset_id:
    asset_id_clean = normalize(asset_id)
    df['__normalized__'] = df[search_column].apply(normalize)
    result = df[df['__normalized__'] == asset_id_clean]

    if not result.empty:
        st.success("✅ Asset found. Details below:")
        record = result.iloc[0]
        fields = {
            "Asset Description": record.get("Asset Description", "N/A"),
            "Tag Number": record.get(search_column, "N/A"),
            "Entity": record.get("Entity", "N/A"),
            "City": record.get("City", "N/A"),
            "Cost": record.get("Cost", "N/A"),
            "Useful Life": record.get("Useful Life", "N/A"),
            "Remaining Life": record.get("Remaining Life", "N/A"),
            "National Address ID": record.get("National Address ID", "N/A"),
        }

        for key, value in fields.items():
            st.write(f"**{key}**: {value}")
    else:
        st.error("❌ No asset found with that number.")

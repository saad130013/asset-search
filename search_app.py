
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

def render_table(data_dict, title):
    html = f"<h3 style='color:#2c3e50;'>{title}</h3><table style='width:100%; direction:rtl; border-collapse:collapse;'>"
    html += "<tr style='background-color:#f3f3f3;'><th style='padding:10px;border:1px solid #ccc;'>المعلومة</th><th style='padding:10px;border:1px solid #ccc;'>القيمة</th></tr>"
    for key, value in data_dict.items():
        html += f"<tr><td style='padding:10px;border:1px solid #ccc;'>{key}</td><td style='padding:10px;border:1px solid #ccc;'>{value}</td></tr>"
    html += "</table><br>"
    return html

# واجهة المستخدم
st.set_page_config(page_title="Asset Lookup System", layout="wide", page_icon="📁")
st.title("🔍 نظام البحث عن الأصول")

# البحث متعدد المعايير
st.sidebar.header("🔎 خيارات البحث")

tag_number = st.sidebar.text_input("رقم الأصل")
entity = st.sidebar.selectbox("الجهة", [""] + sorted(df["Entity"].dropna().unique().astype(str)))
city = st.sidebar.selectbox("المدينة", [""] + sorted(df["City"].dropna().unique().astype(str)))
min_cost = st.sidebar.number_input("الحد الأدنى للتكلفة", min_value=0, value=0)
max_life = st.sidebar.number_input("الحد الأقصى للعمر الإنتاجي", min_value=0, value=100)

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

# عرض التفاصيل
if not filtered_df.empty:
    record = filtered_df.iloc[0]

    general_info = {
        "رقم الأصل": record.get("Tag number", "N/A"),
        "وصف الأصل": record.get("Asset Description", "N/A"),
        "الجهة": record.get("Entity", "N/A"),
        "رمز الجهة": record.get("Entity Code", "N/A"),
        "التكلفة": record.get("Cost", "N/A"),
        "العمر الإنتاجي": record.get("Useful Life", "N/A"),
        "العمر المتبقي": record.get("Remaining Life", "N/A"),
        "المدينة": record.get("City", "N/A"),
        "المنطقة": record.get("Region", "N/A"),
        "رقم المبنى": record.get("Building Number", "N/A"),
        "رقم الدور": record.get("Floors Number", "N/A"),
        "رقم الغرفة / المكتب": record.get("Room/office Number", "N/A"),
        "العنوان الوطني": record.get("National Address ID", "N/A"),
        "طريقة التقييم": record.get("Valuation Method", "N/A"),
        "الإحداثيات الجغرافية": record.get("Geographical Coordinates", "N/A"),
        "ملاحظات": record.get("Comments", "N/A")
    }

    classification_info = {
        "رمز التصنيف - المستوى الأول": record.get("Level 1 FA Module Code", "N/A"),
        "الوصف (عربي) - المستوى الأول": record.get("Level 1 FA Module - Arabic Description", "N/A"),
        "الوصف (إنجليزي) - المستوى الأول": record.get("Level 1 FA Module - English Description", "N/A"),
        "رمز التصنيف - المستوى الثاني": record.get("Level 2 FA Module Code", "N/A"),
        "الوصف (عربي) - المستوى الثاني": record.get("Level 2 FA Module - Arabic Description", "N/A"),
        "الوصف (إنجليزي) - المستوى الثاني": record.get("Level 2 FA Module - English Description", "N/A"),
        "رمز التصنيف - المستوى الثالث": record.get("Level 3 FA Module Code", "N/A"),
        "الوصف (عربي) - المستوى الثالث": record.get("Level 3 FA Module - Arabic Description", "N/A"),
        "الوصف (إنجليزي) - المستوى الثالث": record.get("Level 3 FA Module - English Description", "N/A"),
        "رمز المجموعة المحاسبية": record.get("accounting group Code", "N/A"),
        "الوصف (عربي) - المجموعة المحاسبية": record.get("accounting group Arabic Description", "N/A"),
        "الوصف (إنجليزي) - المجموعة المحاسبية": record.get("accounting group English Description", "N/A"),
        "رمز الأصل لغرض المحاسبة": record.get("Asset Code For Accounting Purpose", "N/A")
    }

    # عرض الجداول
    st.markdown(render_table(general_info, "📋 معلومات الأصل العامة"), unsafe_allow_html=True)
    st.markdown(render_table(classification_info, "📊 التصنيف المحاسبي"), unsafe_allow_html=True)

    # عرض الخريطة التفاعلية
    coords = record.get("Geographical Coordinates")
    if isinstance(coords, str) and "," in coords:
        try:
            lat, lon = map(float, coords.split(","))
            m = folium.Map(location=[lat, lon], zoom_start=16)
            folium.Marker([lat, lon], tooltip="موقع الأصل").add_to(m)
            st.subheader("🗺️ موقع الأصل على الخريطة")
            st_folium(m, width=700, height=500)
        except:
            st.warning("⚠️ تعذر تحليل الإحداثيات.")
else:
    st.warning("🔍 لم يتم العثور على أصول مطابقة. يرجى تعديل الفلاتر.")

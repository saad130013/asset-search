
import streamlit as st
import pandas as pd

# قراءة البيانات من ملف Excel بعد تصحيح الرأس
df = pd.read_excel("assetv4.xlsx", header=2)

# اسم العمود الذي يحتوي على رقم الأصل
search_column = 'رقم الأصل الفريد بالجهة (الرقم المستخدم حاليا للأصل او رقم تسلسلي)'

st.set_page_config(page_title="البحث عن أصل", layout="centered", page_icon="🔍")
st.title("نظام البحث عن الأصول")

asset_id = st.text_input("📌 أدخل رقم الأصل")

if asset_id:
    result = df[df[search_column].astype(str) == asset_id.strip()]
    
    if not result.empty:
        st.success("✅ تم العثور على الأصل:")
        st.dataframe(result)
    else:
        st.error("❌ لم يتم العثور على الأصل بهذا الرقم.")


import streamlit as st
import pandas as pd

# تحميل البيانات من ملف Excel
df = pd.read_excel("assetv4.xlsx", header=2)

# اسم عمود رقم البطاقة (TAG NUMBER)
search_column = 'رقم البطاقة'

# إعداد الصفحة
st.set_page_config(page_title="نظام البحث عن الأصول", layout="centered", page_icon="📁")
st.title("🔍 نظام البحث عن الأصول")

# إدخال رقم الأصل
asset_id = st.text_input("📌 أدخل رقم الأصل:")

# عند البحث
if asset_id:
    asset_id_clean = asset_id.strip()
    result = df[df[search_column].astype(str).str.strip() == asset_id_clean]

    if not result.empty:
        st.success("✅ تم العثور على الأصل. التفاصيل:")
        record = result.iloc[0]
        fields = {
            "Asset Description": record.get("وصف الأصل", "N/A"),
            "Asset Number": record.get(search_column, "N/A"),
            "Department": record.get("القسم أو الإدارة المسؤولة", "N/A"),
            "Entity": record.get("اسم الجهة", "N/A"),
            "City": record.get("المدينة", "N/A"),
            "Cost": record.get("التكلفة", "N/A"),
            "Useful Life": record.get("العمر الإنتاجي", "N/A"),
            "Remaining Life": record.get("العمر المتبقي", "N/A"),
            "Location": record.get("العنوان الوطني", "N/A"),
            "Manufacturer": record.get("المصنع", "N/A"),
        }

        for key, value in fields.items():
            st.write(f"**{key}**: {value}")
    else:
        st.error("❌ لم يتم العثور على الأصل بهذا الرقم.")


import streamlit as st
import pandas as pd

# تحميل البيانات
df = pd.read_excel("assetv4.xlsx", header=2)

# اسم العمود المستخدم للبحث
search_column = 'رقم البطاقة'

# دالة تنظيف وتطبيع القيم
def normalize(value):
    if pd.isna(value):
        return ""
    return str(value).strip().replace('\u200f', '').replace('\u202a', '').replace('\xa0', '').replace(" ", "")

# إعداد الصفحة
st.set_page_config(page_title="نظام البحث عن الأصول", layout="centered", page_icon="📁")
st.title("🔍 نظام البحث عن الأصول")

# إدخال رقم الأصل
asset_id = st.text_input("📌 أدخل رقم الأصل:")

if asset_id:
    asset_id_clean = normalize(asset_id)
    df['__normalized__'] = df[search_column].apply(normalize)
    result = df[df['__normalized__'] == asset_id_clean]

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

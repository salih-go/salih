import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# مسار ملف JSON
json_file_path = r'C:\Users\Windows10\Desktop\oo\payments_data.json'

def load_data():
    if os.path.exists(json_file_path) and os.path.getsize(json_file_path) > 0:
        with open(json_file_path, 'r') as f:
            return pd.DataFrame(json.load(f))
    else:
        return pd.DataFrame(columns=["amount_try", "exchange_rate", "amount_usd", "amount_iqd", "timestamp"])

def save_data(data):
    # تعديل القيم الصحيحة لتحفظ كصحيحة دون إضافة .0
    for col in ["amount_try", "exchange_rate", "amount_usd", "amount_iqd"]:
        data[col] = data[col].apply(lambda x: int(x) if int(x) == x else x)
    with open(json_file_path, 'w') as f:
        json.dump(data.to_dict(orient='records'), f, ensure_ascii=False, indent=4)

def main():
    st.title("نظام تسجيل المدفوعات")
    page = st.sidebar.selectbox("اختر الصفحة", ["إدخال معلومات الدفع", "عرض تفاصيل الدفع", "تعديل أو حذف طلب"])

    if page == "إدخال معلومات الدفع":
        payment_entry_page()
    elif page == "عرض تفاصيل الدفع":
        payment_display_page()
    elif page == "تعديل أو حذف طلب":
        modify_or_delete_page()

def payment_entry_page():
    st.header("إدخال معلومات الدفع")
    amount_try = st.text_input("المبلغ بالليرة التركية")
    exchange_rate = st.text_input("سعر الصرف للدولار")
    amount_usd = st.text_input("المبلغ بالدولار")
    amount_iqd = st.text_input("المبلغ بالدينار العراقي")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("حفظ المعلومات"):
        if amount_try and exchange_rate and amount_usd and amount_iqd:
            new_data = pd.DataFrame({
                "amount_try": [float(amount_try)],
                "exchange_rate": [float(exchange_rate)],
                "amount_usd": [float(amount_usd)],
                "amount_iqd": [float(amount_iqd)],
                "timestamp": [timestamp]
            })
            data = load_data()
            data = pd.concat([data, new_data], ignore_index=True)
            save_data(data)
            st.success("تم حفظ المعلومات بنجاح!")
        else:
            st.error("الرجاء ملء جميع الحقول.")

def payment_display_page():
    st.header("عرض تفاصيل الدفع")
    data = load_data()
    if not data.empty:
        data.rename(columns={
            'amount_try': 'المبلغ بالليرة التركية',
            'exchange_rate': 'سعر الصرف',
            'amount_usd': 'المبلغ بالدولار',
            'amount_iqd': 'المبلغ بالدينار العراقي',
            'timestamp': 'التاريخ والوقت'
        }, inplace=True)
        st.dataframe(data)

def modify_or_delete_page():
    st.header("تعديل أو حذف طلب")
    data = load_data()
    if not data.empty:
        options = [f"طلب رقم {i + 1}" for i in range(len(data))]
        selected_order = st.selectbox("اختر الطلب", options)
        if selected_order:
            index = options.index(selected_order)
            order = data.iloc[index]

            amount_try = st.text_input("المبلغ بالليرة التركية", value=order["amount_try"])
            exchange_rate = st.text_input("سعر الصرف للدولار", value=order["exchange_rate"])
            amount_usd = st.text_input("المبلغ بالدولار", value=order["amount_usd"])
            amount_iqd = st.text_input("المبلغ بالدينار العراقي", value=order["amount_iqd"])

            if st.button("تحديث المعلومات"):
                data.at[index, "amount_try"] = float(amount_try)
                data.at[index, "exchange_rate"] = float(exchange_rate)
                data.at[index, "amount_usd"] = float(amount_usd)
                data.at[index, "amount_iqd"] = float(amount_iqd)
                save_data(data)
                st.success("تم تحديث المعلومات بنجاح!")
                st.rerun()

            if st.button("حذف الطلب"):
                data = data.drop(index)
                save_data(data)
                st.success("تم حذف الطلب بنجاح!")
                st.rerun()
    else:
        st.info("لم يتم إدخال أي مدفوعات بعد.")

if __name__ == "__main__":
    main()

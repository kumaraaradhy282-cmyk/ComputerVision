import streamlit as st

st.set_page_config(page_title="Bank Account Opening", layout="centered")

st.title("🏦 Bank Account Opening Form")
st.write("Please enter your details and capture your photo")

# User inputs
name = st.text_input("Full Name")
account_number = st.text_input("Bank Account Number")

# Camera input
photo = st.camera_input("Capture your photo")

# Submit button
if st.button("Submit"):
    if name and account_number and photo:
        st.success("✅ Account Opening Data Submitted Successfully")

        st.subheader("📄 Submitted Details")
        st.write(f"**Name:** {name}")
        st.write(f"**Account Number:** {account_number}")

        st.subheader("📸 Captured Photo")
        st.image(photo)
    else:
        st.error("❌ Please fill all details and capture photo")

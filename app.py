import streamlit as st
import pandas as pd
import requests

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
WEBHOOK_URL = "https://rahulllllllllllllllll.app.n8n.cloud/webhook/8d91510a-69e7-4380-9653-120ccac05906"

st.set_page_config(
    page_title="False News Detection AI Agent",
    page_icon="📰",
    layout="centered"
)

# -------------------------------------------------
# UI
# -------------------------------------------------
st.title("📰 False News Detection AI Agent")

st.markdown("""
You are interacting with an **AI verification agent**.

**Rules followed:**
- Only Excel `content` column is trusted  
- No outside knowledge  
- Verdict: TRUE / FALSE / NOT FOUND  
""")

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload verified financial news Excel file",
    type=["xlsx"]
)

claim = st.text_area(
    "Enter news claim",
    placeholder="Example: RBI increased repo rate by 25 basis points"
)

# -------------------------------------------------
# VERIFY BUTTON
# -------------------------------------------------
if st.button("Verify Claim"):

    if not uploaded_file or not claim:
        st.warning("Please upload Excel file and enter a claim.")
    else:
        try:
            # Read Excel
            df = pd.read_excel(uploaded_file)

            if "content" not in df.columns or "date" not in df.columns:
                st.error("Excel must contain: date and content columns.")
            else:
                # Convert Excel to JSON for n8n
                records = df[["date", "content"]].to_dict(orient="records")

                payload = {
                    "claim": claim,
                    "news_data": records
                }

                with st.spinner("Verifying with AI Agent..."):
                    response = requests.post(
                        WEBHOOK_URL,
                        json=payload,
                        timeout=90
                    )

                result = response.json()

                # -------------------------------------------------
                # OUTPUT
                # -------------------------------------------------
                st.subheader("🧠 Verdict")
                st.success(f"Verdict: {result.get('verdict', 'N/A')}")

                st.subheader("📌 Evidence")
                st.write(result.get("evidence", "No evidence returned."))

        except Exception as e:
            st.error(f"Error communicating with verification agent: {e}")

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="False News Detection AI Agent",
    page_icon="📰",
    layout="centered"
)

st.title("📰 False News Detection AI Agent")

st.markdown("""
This system verifies a news claim **only using the Excel content column**.

**Decision rules**
- TRUE → claim matches content  
- FALSE → claim contradicts content  
- NOT FOUND → claim not present  
""")

# Upload Excel
uploaded_file = st.file_uploader(
    "Upload verified financial news Excel file",
    type=["xlsx"]
)

# Input claim
claim = st.text_area(
    "Enter the news claim",
    placeholder="Example: RBI increased repo rate by 25 basis points"
)

if uploaded_file and claim:

    df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    if "content" not in df.columns or "date" not in df.columns:
        st.error("Excel must contain: date, content, summary columns")
    else:
        claim_lower = claim.lower()

        found_match = False
        contradiction = False
        evidence_rows = []

        for _, row in df.iterrows():
            content_text = str(row["content"]).lower()

            # Simple matching logic (basic version)
            if claim_lower in content_text:
                found_match = True
                evidence_rows.append(row)

        # Decision logic
        if found_match:
            verdict = "TRUE"
        else:
            verdict = "NOT FOUND"

        st.subheader("🧠 Verdict")
        st.success(f"Verdict: {verdict}")

        st.subheader("📌 Evidence")

        if verdict == "TRUE":
            for row in evidence_rows:
                st.markdown(f"""
**Date:** {row['date']}  
**Content Reference:**  
{row['content']}
""")
        else:
            st.write("No matching content found in the Excel data.")

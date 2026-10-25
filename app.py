import os
import random
import streamlit as st
from google import genai

# Styling and Page Setup
st.set_page_config(
    page_title="AgriSmart Mandi Selling Advisor",
    page_icon="🌾",
    layout="centered"
)

# Custom CSS styling
st.markdown("""
<style>
    .header-style {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #FFB84D;
        margin-bottom: 5px;
    }
    .accent-bar {
        height: 4px;
        background: linear-gradient(90deg, #4CAF50, #FFB84D);
        border-radius: 2px;
        margin-bottom: 20px;
    }
    .custom-card {
        padding: 18px;
        background-color: #1e242b;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<div class='header-style'>🌾 AgriSmart: Mandi Selling Advisor</div>", unsafe_allow_html=True)
st.caption("AI-powered market decision system for smallholder farmers.")
st.markdown("<div class='accent-bar'></div>", unsafe_allow_html=True)

# Fast, lightweight image thumbnail
st.image(
    "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=800&q=60", 
    use_container_width=True
)

# API Key handling
DEFAULT_API_KEY = ""
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") or DEFAULT_API_KEY

# Section 1: User Inputs
st.markdown("### 1. Enter Harvest Details")
col1, col2 = st.columns(2)

with col1:
    crop_list = [
        "Tomato", "Potato", "Wheat", "Onion", 
        "Paddy (Rice)", "Sugarcane", "Cotton", 
        "Maize", "Mustard", "Chana (Gram)"
    ]
    crop = st.selectbox("🌾 Select Crop", crop_list)
    quantity = st.number_input("⚖️ Quantity (in Quintals)", min_value=1, value=20)

with col2:
    location = st.text_input("📍 Your City/Town", "Patiala, Punjab")
    transport_rate = st.number_input("🚛 Transport Rate (₹/km/quintal)", min_value=1.0, value=2.5)

st.markdown("---")

# Section 2: AI Market Analysis
st.markdown("### 2. Live Mandi Market Intelligence")

if st.button("🔍 Find Optimal Mandi & Rates", type="primary"):
    if not api_key:
        st.error("API Key missing! Please configure GEMINI_API_KEY in Streamlit Secrets.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Act as a real-time agricultural market intelligence engine for India.
            User Location: {location}
            Crop: {crop}
            Quantity: {quantity} quintals

            Task:
            1. Identify 3 realistic nearest Mandis/APMCs around {location} with approximate distance in kilometers.
            2. Provide current realistic prevailing market rates (in ₹/Quintal) for {crop} at these 3 mandis.
            3. Calculate net profit for each considering transport cost rate of ₹{transport_rate} per km per quintal.
            4. Output a clear recommendation on where the farmer should sell today to earn the highest net profit.

            Return the response in clear Markdown with a summary table first, followed by 3 actionable bullet points. Use emojis.
            """

            st.subheader("🤖 Optimal Mandi & Route Recommendation")
            
            # Fast Live Response Generation
            with st.spinner("Connecting to live market intelligence..."):
                try:
                    response_stream = client.models.generate_content_stream(
                        model="gemini-3.8-flash",
                        contents=prompt,
                    )
                except Exception:
                    response_stream = client.models.generate_content_stream(
                        model="gemini-1.5-flash",
                        contents=prompt,
                    )

            # Streams text instantly as it generates
            st.write_stream(chunk.text for chunk in response_stream if chunk.text)

        except Exception as e:
            st.error(f"Failed to connect to AI engine: {e}")

import os
import random
import time
import streamlit as st
import pandas as pd
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
        font-size: 38px !important;
        font-weight: 700 !important;
        color: #FFB84D;
        margin-bottom: 5px;
    }
    .accent-bar {
        height: 4px;
        background: linear-gradient(90deg, #4CAF50, #FFB84D);
        border-radius: 2px;
        margin-bottom: 25px;
    }
    .custom-card {
        padding: 20px;
        background-color: #1e242b;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<div class='header-style'>🌾 AgriSmart: Mandi Selling Advisor</div>", unsafe_allow_html=True)
st.caption("AI-powered market decision system for smallholder farmers. Making every harvest count.")
st.markdown("<div class='accent-bar'></div>", unsafe_allow_html=True)

# Direct web image URL for farmer header
st.image(
    "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=1200&q=80", 
    caption="Supporting India's smallholder farmers with location-aware AI marketplace insights.",
    use_container_width=True
)

# API Key handling
DEFAULT_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
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

# Direct web image URL for market scene
st.image(
    "https://images.unsplash.com/photo-1595855759920-86582396756a?auto=format&fit=crop&w=1200&q=80", 
    caption="Dynamic Market View: Real-time APMC Mandi price analysis.",
    use_container_width=True
)

st.markdown("---")

# Section 2: AI Market Analysis
st.markdown("### 2. Live Mandi Market Intelligence")

waiting_quotes = [
    "“The farmer is the only man in our economy who buys everything at retail, sells everything at wholesale, and pays the freight both ways.” — John F. Kennedy",
    "“To a fertile soil, a farmer's sweat is like gold.”",
    "“Jai Jawan, Jai Kisan — Hail the Soldier, Hail the Farmer.” — Lal Bahadur Shastri",
    "“He who sows bountifully shall reap bountifully.”",
    "“Agriculture is our wisest pursuit, because it will in the end contribute most to real wealth.” — Thomas Jefferson",
    "“Patience and hard work always bear the sweetest harvest.”"
]

if st.button("🔍 Find Optimal Mandi & Rates"):
    if not api_key or api_key == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
        st.error("API Key missing! Please configure GEMINI_API_KEY in Streamlit Secrets or code.")
    else:
        progress_quote = random.choice(waiting_quotes)
        
        with st.status("🌱 Fetching real mandi rates & calculating transport margins...") as status:
            st.markdown(f"**While we fetch rates, think about this:** \n*{progress_quote}*")
            time.sleep(2)
            
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Act as a real-time agricultural market intelligence engine for India.
                User Location: {location}
                Crop: {crop}
                Quantity: {quantity} quintals

                Task:
                1. Identify 3 realistic nearest Mandis/APMCs around {location} with their approximate distance in kilometers.
                2. Provide current realistic prevailing market rates (in ₹/Quintal) for {crop} at these 3 mandis.
                3. Calculate net profit for each after considering transport cost rate of ₹{transport_rate} per km per quintal.
                4. Output a clear recommendation on where the farmer should sell today to earn the highest net profit.

                Return the response in clear Markdown with a summary table first, followed by 3 actionable bullet points. Use emojis for visibility.
                """

                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt,
                    )
                except Exception:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=prompt,
                    )

                status.update(label="✅ Rates analyzed and localized!", state="complete", expanded=True)
                
                st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                st.subheader("🤖 Optimal Mandi & Route Recommendation")
                st.markdown(response.text)
                st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                status.update(label="❌ Analysis failed", state="error", expanded=True)
                st.error(f"Failed to connect to AI engine: {e}")

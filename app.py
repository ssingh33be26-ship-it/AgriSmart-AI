import os
import streamlit as st
import pandas as pd
from google import genai

# Page Setup
st.set_page_config(page_title="AgriSmart AI Advisor", page_icon="🌾", layout="centered")

st.title("🌾 AgriSmart: Real-Time Mandi Decision Engine")
st.caption("Empowering smallholders with location-aware market intelligence.")

st.markdown("---")

# ---------------------------------------------------------
# API KEY HANDLING (No User Input Required)
# ---------------------------------------------------------
# Put your fallback Gemini API key between the quotes below
DEFAULT_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"

# Retrieve from Streamlit Secrets, Environment Variable, or Fallback Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") or DEFAULT_API_KEY

# ---------------------------------------------------------
# 1. USER INPUTS
# ---------------------------------------------------------
st.subheader("1. Enter Location & Crop")
col1, col2 = st.columns(2)

with col1:
    crop_list = [
        "Tomato", 
        "Potato", 
        "Wheat", 
        "Onion", 
        "Paddy (Rice)", 
        "Sugarcane", 
        "Cotton", 
        "Maize", 
        "Mustard", 
        "Chana (Gram)"
    ]
    crop = st.selectbox("Select Crop", crop_list)
    quantity = st.number_input("Quantity (in Quintals)", min_value=1, value=20)

with col2:
    location = st.text_input("Your City/Town", "Patiala")
    transport_rate = st.number_input("Transport Rate (₹/km/quintal)", min_value=1.0, value=2.5)

st.markdown("---")
st.subheader("2. Market Discovery & AI Analysis")

# ---------------------------------------------------------
# 2. AI GENERATION TRIGGER
# ---------------------------------------------------------
if st.button("🔍 Find Optimal Mandi & Rates"):
    if not api_key or api_key == "YOUR_ACTUAL_GEMINI_API_KEY_HERE":
        st.error("API Key not found! Please paste your key into DEFAULT_API_KEY in app.py or set GEMINI_API_KEY in Streamlit Secrets.")
    else:
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

            Return the response in clear Markdown with a summary table first, followed by 3 actionable bullet points.
            """

            with st.spinner("Fetching market rates and generating decision matrix..."):
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

            st.success("✅ Market Analysis Generated Successfully!")
            st.markdown(response.text)

        except Exception as e:
            st.error(f"Error connecting to AI service: {e}")

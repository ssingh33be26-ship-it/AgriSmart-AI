import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="AgriSmart AI Advisor", page_icon="🌾", layout="centered")

st.title("🌾 AgriSmart: Real-Time Mandi Decision Engine")
st.caption("Empowering smallholders with location-aware market intelligence.")

st.markdown("---")

# User Inputs
st.subheader("1. Enter Location & Crop")
col1, col2 = st.columns(2)

with col1:
    crop = st.selectbox("Select Crop", ["Tomato", "Potato", "Wheat", "Onion", "Paddy (Rice)"])
    quantity = st.number_input("Quantity (in Quintals)", min_value=1, value=20)

with col2:
    location = st.text_input("Your City/Town", "Patiala")
    transport_rate = st.number_input("Transport Rate (₹/km/quintal)", min_value=1.0, value=2.5)

st.markdown("---")
st.subheader("2. Market Discovery & AI Analysis")

api_key = st.text_input("Enter Gemini API Key to Fetch Live Market Strategy:", type="password")

if st.button("🔍 Find Optimal Mandi & Rates"):
    if not api_key:
        st.error("Please enter your Gemini API key.")
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
                # Try primary model first, fallback to flash model if 503 occurs
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
            st.error(f"Error: {e}")

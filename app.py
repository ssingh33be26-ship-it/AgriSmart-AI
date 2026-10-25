import os
import streamlit as st
from google import genai

# Styling and Page Setup
st.set_page_config(
    page_title="AgriSmart Mandi Advisor",
    page_icon="🌾",
    layout="centered"
)

# Clean CSS
st.markdown("""
<style>
    .header-style { font-size: 34px !important; font-weight: 700 !important; color: #FFB84D; }
    .accent-bar { height: 4px; background: linear-gradient(90deg, #4CAF50, #FFB84D); margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='header-style'>🌾 AgriSmart: Mandi Selling Advisor</div>", unsafe_allow_html=True)
st.caption("AI-powered market decision system for smallholder farmers.")
st.markdown("<div class='accent-bar'></div>", unsafe_allow_html=True)

# Lightweight compressed header image
st.image(
    "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=600&q=50", 
    use_container_width=True
)

# Retrieve API Key from Streamlit Secrets or Environment
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# Section 1: Inputs
st.markdown("### 1. Enter Harvest Details")
col1, col2 = st.columns(2)

with col1:
    crop_list = ["Tomato", "Potato", "Wheat", "Onion", "Paddy (Rice)", "Sugarcane", "Cotton", "Maize", "Mustard", "Chana (Gram)"]
    crop = st.selectbox("🌾 Select Crop", crop_list)
    quantity = st.number_input("⚖️ Quantity (Quintals)", min_value=1, value=20)

with col2:
    location = st.text_input("📍 Your City/Town", "Patiala, Punjab")
    transport_rate = st.number_input("🚛 Transport Rate (₹/km/quintal)", min_value=1.0, value=2.5)

st.markdown("---")
st.markdown("### 2. Live Mandi Market Intelligence")

if st.button("🔍 Find Optimal Mandi & Rates", type="primary"):
    if not api_key:
        st.error("API Key missing! Please set GEMINI_API_KEY in Streamlit Cloud Secrets.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Act as a real-time agricultural market intelligence engine for India.
            User Location: {location}
            Crop: {crop}
            Quantity: {quantity} quintals

            Task:
            1. Identify 3 realistic nearest Mandis/APMCs around {location} with distance in km.
            2. Provide current realistic prevailing market rates (in ₹/Quintal) for {crop}.
            3. Calculate net profit for each considering transport rate of ₹{transport_rate}/km/quintal.
            4. Output a clear recommendation on where to sell today for maximum profit.

            Return response in clean Markdown with a summary table first, followed by 3 actionable bullet points with emojis. Keep concise.
            """

            # Display streamed output immediately
            with st.chat_message("assistant", avatar="🤖"):
                # Use gemini-1.5-flash for maximum speed / lowest latency
                response_stream = client.models.generate_content_stream(
                    model="gemini-1.5-flash",
                    contents=prompt,
                )
                
                # Renders text instantly line-by-line
                st.write_stream(chunk.text for chunk in response_stream if chunk.text)

        except Exception as e:
            st.error(f"Error: {e}")

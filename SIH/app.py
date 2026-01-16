import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
from gtts import gTTS
import base64
from streamlit_extras.metric_cards import style_metric_cards

# -------------------------
# SAMPLE CROPS DATA
# -------------------------
crops = [
    {"name": "Wheat", "yield": 3.2, "profit": 45000, "sustainability": 8, "risk": 0.25, "rotation": ["Pulses", "Mustard"]},
    {"name": "Rice", "yield": 2.8, "profit": 38000, "sustainability": 6, "risk": 0.40, "rotation": ["Pulses", "Vegetables"]},
    {"name": "Mustard", "yield": 2.5, "profit": 50000, "sustainability": 9, "risk": 0.20, "rotation": ["Wheat", "Vegetables"]},
    {"name": "Barley", "yield": 2.0, "profit": 30000, "sustainability": 7, "risk": 0.30, "rotation": ["Maize", "Mustard"]},
    {"name": "Maize", "yield": 3.0, "profit": 42000, "sustainability": 8, "risk": 0.22, "rotation": ["Potato", "Pulses"]},
]

def recommend_crops(soil, ph, rainfall, temp, prev_crop):
    return random.sample(crops, 3)  # random for demo

def text_to_speech(text, lang="hi"):
    tts = gTTS(text=text, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)
    with open(filename, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f'<audio autoplay controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'


# -------------------------
# STREAMLIT PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Crop Advisor", page_icon="🌱", layout="wide")
st.title("🌱 AI-Powered Crop Recommendation System / AI संचालित फसल अनुशंसा प्रणाली")
st.markdown(
    """
    <style>
        /* Background */
        
        .main, .block-container {
            background-color: #121212 !important;
            color: #ffffff !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }

        /* Streamlit primary buttons */
        button[kind="primary"] {
            background-color: #4CAF50 !important;
            color: #ffffff !important;
            border: 1px solid #388E3C !important;
        }

        /* Streamlit secondary buttons */
        button[kind="secondary"] {
            background-color: #333333 !important;
            color: #ffffff !important;
            border: 1px solid #555555 !important;
        }

        /* Hover effect for buttons */
        button:hover {
            opacity: 0.9;
        }

        /* Metric card text */
        .stMetric > div {
            background-color: #1E1E1E !important;
            color: #E0E0E0 !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------
# MAIN TABS
# -------------------------
main_tabs = st.tabs(["🏠 Home", "🌱 Recommend"])

# ========== HOME TAB ==========
with main_tabs[0]:
    st.subheader("📈 Top 3 Crops Trending in Market / शीर्ष 3 फसलें")

    trending = sorted(crops, key=lambda x: (x["profit"], x["sustainability"]), reverse=True)[:3]
    for crop in trending:
        st.write(f"**{crop['name']}** → Profit: ₹{crop['profit']} | Sustainability: {crop['sustainability']}/10")

    st.markdown("---")
    st.subheader("📊 Factor Analysis / कारक विश्लेषण")

    # Initialize state
    if "factor" not in st.session_state:
        st.session_state["factor"] = "Temperature"

    # Button row with colors
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🌡 Temperature", type="primary" if st.session_state["factor"]=="Temperature" else "secondary"):
            st.session_state["factor"] = "Temperature"
    with col2:
        if st.button("🌧 Rainfall", type="primary" if st.session_state["factor"]=="Rainfall" else "secondary"):
            st.session_state["factor"] = "Rainfall"
    with col3:
        if st.button("☁️ Cloud %", type="primary" if st.session_state["factor"]=="Cloud Percentage" else "secondary"):
            st.session_state["factor"] = "Cloud Percentage"
    with col4:
        if st.button("💰 Crop Price", type="primary" if st.session_state["factor"]=="Current Crop Price Prediction" else "secondary"):
            st.session_state["factor"] = "Current Crop Price Prediction"

    # Show graph based on selected button
    factor = st.session_state["factor"]

    if factor == "Temperature":
        values = [random.randint(20, 40) for _ in trending]
        ylabel = "Temperature (°C)"
    elif factor == "Rainfall":
        values = [random.randint(50, 200) for _ in trending]
        ylabel = "Rainfall (mm)"
    elif factor == "Cloud Percentage":
        values = [random.randint(10, 90) for _ in trending]
        ylabel = "Cloud %"
    else:
        values = [crop["profit"] + random.randint(-5000, 5000) for crop in trending]
        ylabel = "Predicted Price (₹)"

    fig, ax = plt.subplots(figsize=(4, 2.5), dpi=30)
    ax.bar([c["name"] for c in trending], values, width=0.4, color=["#4CAF50", "#2196F3", "#FFC107"])
    ax.set_ylabel(ylabel)
    ax.set_title(factor)
    st.pyplot(fig, use_container_width=False)

# ========== RECOMMEND TAB ==========
with main_tabs[1]:
    st.subheader("🌱 AI Crop Recommendation / फसल अनुशंसा")

    col1, col2 = st.columns(2)
    with col1:
        soil = st.selectbox("Soil Type / मिट्टी का प्रकार", 
                            ["Alluvial", "Black", "Red", "Sandy", "Laterite"])
        # changed from slider → number_input
        ph = st.number_input("Soil pH / मिट्टी का pH", min_value=3.5, max_value=9.0, value=6.5, step=0.1)
        rainfall = st.number_input("Rainfall (mm) / वर्षा (mm)", 0, 500, 120)
    with col2:
        temp = st.number_input("Temperature (°C) / तापमान (°C)", 5, 45, 25)
        prev_crop = st.selectbox("Previous Crop / पिछली फसल", 
                                 ["None", "Wheat", "Rice", "Maize", "Mustard", "Barley"])
    run = st.button("🚀 Recommend Crops / फसल सुझाएँ")

    if run:
        results = recommend_crops(soil, ph, rainfall, temp, prev_crop)
        df = pd.DataFrame(results)

        # Subtabs for outputs
        sub_tabs = st.tabs([
            "🌾 Recommendations / अनुशंसाएँ", 
            "📊 Smart Economics / स्मार्ट अर्थशास्त्र", 
            "🌍 Crop Rotation / फसल चक्र", 
            "🔊 Voice Assistant / वॉयस असिस्टेंट"
        ])

        # ========== Recommendations ==========
        with sub_tabs[0]:
            st.subheader("🌾 Recommended Crops for You / 🌾 आपके लिए अनुशंसित फसलें")
            for crop in results:
                with st.container():
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("🌱 Crop", crop["name"])
                    col2.metric("Yield (t/ha)", crop["yield"])
                    col3.metric("Profit (₹)", f"{crop['profit']}")
                    col4.metric("Sustainability", f"{crop['sustainability']}/10")
            style_metric_cards(background_color="#040404", border_color="#E0E0E0", border_left_color="#4CAF50")

        # ========== Smart Economics ==========
        with sub_tabs[1]:
            st.subheader("📊 Smart Economics Insights / स्मार्ट अर्थशास्त्र अंतर्दृष्टि")

            for crop in results:
                if crop["risk"] < 0.25:
                    risk_level = "🟢 Low / कम"
                elif crop["risk"] < 0.4:
                    risk_level = "🟡 Medium / मध्यम"
                else:
                    risk_level = "🔴 High / उच्च"

                score = round(crop["profit"] / (crop["risk"]*100000), 2)

                with st.container():
                    col1, col2, col3 = st.columns(3)
                    col1.metric("💰 Profit (₹)", crop["profit"])
                    col2.metric("⚠️ Risk", risk_level)
                    col3.metric("📈 Smart Score", score)

            style_metric_cards(
                background_color="#1E1E1E",
                border_color="#E0E0E0",
                border_left_color="#1565C0"
            )

        # ========== Crop Rotation ==========
        with sub_tabs[2]:
            st.subheader("🌍 Smart Crop Rotation Planner / स्मार्ट फसल चक्र योजनाकार")

            for crop in results:
                rotation_list = ", ".join(crop["rotation"])
                
                html_card = f"""<div style="padding:16px;border-radius:12px;border:1px solid #ddd;
                                            margin-bottom:12px;background-color:#1E1E1E;
                                            color:#000000;
                                            box-shadow:0 2px 6px rgba(0,0,0,0.05);">
                    <h4 style="margin:0;color:#2E7D32;">🌱 {crop['name']}</h4>
                    <p style="margin:6px 0;color:#E0E0E0">🔄 After harvesting <b>{crop['name']}</b>, rotate with → <b>{rotation_list}</b></p>
                    <p style="margin:6px 0;font-size:13px;color:#E0E0E0;">✅ This improves soil fertility and reduces pest risk.</p>
                </div>"""
                
                st.markdown(html_card, unsafe_allow_html=True)

        # ========== Voice Assistant ==========
        with sub_tabs[3]:
            st.subheader("🔊 Voice Assistant")
            response_text = f"आपके खेत के लिए सबसे अच्छे फसल हैं {results[0]['name']}, {results[1]['name']} और {results[2]['name']}."
            st.markdown(text_to_speech(response_text, lang="hi"), unsafe_allow_html=True)
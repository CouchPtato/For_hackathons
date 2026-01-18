import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Aadhaar Severity Analyzer",
    layout="wide"
)

df = pd.read_csv("district_severity_app_data.csv")

DISTRICT_NORMALIZATION = {

    # ANDHRA PRADESH / TELANGANA (legacy spellings)
    "K.V. Rangareddy": "K.V.Rangareddy",
    "Karim Nagar": "Karimnagar",
    "Mahabub Nagar": "Mahbubnagar",
    "Ananthapur": "Anantapur",
    "Ananthapuramu": "Anantapur",

    # BIHAR
    "Samstipur": "Samastipur",
    "Sheikpura": "Sheikhpura",

    # CHHATTISGARH
    "Janjgir - Champa": "Janjgir-Champa",

    # DADRA & NAGAR HAVELI / DAMAN & DIU
    "Dadra & Nagar Haveli": "Dadra And Nagar Haveli",

    # GUJARAT
    "Banas Kantha": "Banaskantha",
    "Sabar Kantha": "Sabarkantha",
    "Surendra Nagar": "Surendranagar",
    "Panch Mahals": "Panchmahals",
    "Ahmadabad": "Ahmedabad",

    # HARYANA
    "Yamuna Nagar": "Yamunanagar",

    # HIMACHAL PRADESH
    "Lahul & Spiti": "Lahul And Spiti",

    # KARNATAKA (if present later)
    "Bangalore": "Bengaluru",
    "Bellary": "Ballari",
    "Belgaum": "Belagavi",

    # KERALA
    "Trivandrum": "Thiruvananthapuram",
    "Quilon": "Kollam",

    # MAHARASHTRA
    "Poona": "Pune",
    "Bombay": "Mumbai",

    # TAMIL NADU (from your screenshot)
    "Viluppuram": "Villupuram",
    "Tirupattur": "Tirupathur",

    # PUDUCHERRY
    "Pondicherry": "Puducherry"
}

df["state"] = df["state"].str.strip().str.title()
df["district"] = df["district"].str.strip().str.title()

df["district"] = df["district"].replace(DISTRICT_NORMALIZATION)

df = df.drop_duplicates(subset=["state", "district"])

def performance_badge(label):
    if label == "Excellent":
        st.success("🟢 Excellent – Aadhaar services operating efficiently")
    elif label == "Good":
        st.info("🔵 Good – Healthy Aadhaar operations")
    elif label == "Needs Attention":
        st.warning("🟠 Needs Attention – Rising operational pressure")
    else:
        st.error("🔴 Critical – Immediate intervention required")

def explain_ratios(bio_ratio, demo_ratio):
    explanations = []

    if bio_ratio < 1.0:
        explanations.append(
            "🟢 **Low biometric ratio**: Biometric capture is working efficiently with minimal re-attempts."
        )
    elif bio_ratio < 2.0:
        explanations.append(
            "🔵 **Moderate biometric ratio**: Some biometric updates are occurring, within normal range."
        )
    else:
        explanations.append(
            "🔴 **High biometric ratio**: Frequent biometric updates suggest capture failures, aging biometrics, or device issues."
        )

    if demo_ratio < 1.0:
        explanations.append(
            "🟢 **Low demographic ratio**: Population is stable with few address or demographic changes."
        )
    elif demo_ratio < 2.0:
        explanations.append(
            "🔵 **Moderate demographic ratio**: Normal level of address or demographic updates."
        )
    else:
        explanations.append(
            "🔴 **High demographic ratio**: Indicates migration, frequent address changes, or data corrections."
        )

    return explanations

def change_driver(bio_ratio, demo_ratio):
    if bio_ratio > demo_ratio * 1.3:
        return "Biometric-driven issues"
    elif demo_ratio > bio_ratio * 1.3:
        return "Demographic / migration-driven changes"
    else:
        return "Mixed operational stress"

def recommendations(performance, driver_type):
    recs = {}

    if performance in ["Excellent", "Good"]:
        recs["maintain"] = "Maintain current Aadhaar workflows"
        recs["replicate"] = "Use this district as a best-practice reference"
        recs["monitor"] = "Continue periodic monitoring"
        return list(recs.values())

    recs["capacity"] = "Increase Aadhaar update capacity temporarily"
    recs["mobile"] = "Deploy mobile Aadhaar vans"
    recs["monitor"] = "Monitor update-to-enrolment ratios regularly"

    if driver_type == "Biometric-driven issues":
        recs["device"] = "Audit and replace biometric devices"
        recs["iris"] = "Promote iris-based authentication"

    if driver_type == "Demographic / migration-driven changes":
        recs["camp"] = "Organize mobile demographic update camps"
        recs["process"] = "Simplify address update processes"

    if performance == "Critical":
        recs["audit"] = "Immediate operational audit required"

    return list(recs.values())

st.sidebar.header("🔎 Explore Districts")

view_mode = st.sidebar.radio(
    "Select view",
    [
        "All Districts",
        "Excellent / Good",
        "Needs Attention / Critical"
    ]
)

filtered_df = df.copy()

if view_mode == "Excellent / Good":
    filtered_df = filtered_df[filtered_df["performance"].isin(["Excellent", "Good"])]
elif view_mode == "Needs Attention / Critical":
    filtered_df = filtered_df[filtered_df["performance"].isin(["Needs Attention", "Critical"])]


st.title("🆔 Aadhaar Severity & Action Analyzer")

st.markdown(
    """
Explore **district-level Aadhaar performance**,  
identify **what type of changes are driving severity**,  
and understand **what actions can be taken**.
"""
)

left, right = st.columns([1, 2])

with left:
    states = sorted(filtered_df["state"].unique())
    state = st.selectbox("Select State", states)

    districts = (
        filtered_df[filtered_df["state"] == state]["district"]
        .sort_values()
        .unique()
    )

    district = st.selectbox("Select District", districts)

row = filtered_df[
    (filtered_df["state"] == state) &
    (filtered_df["district"] == district)
].iloc[0]

with right:
    st.subheader(f"📍 {row['district']}, {row['state']}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Severity Score", f"{row['severity']:.2f}")
    col2.metric("Biometric Ratio", f"{row['biometric_ratio']:.2f}")
    col3.metric("Demographic Ratio", f"{row['demo_ratio']:.2f}")

    st.markdown("### 📊 What these ratios indicate")

    for line in explain_ratios(
        row["biometric_ratio"],
        row["demo_ratio"]
    ):
        st.write(line)

    st.markdown(f"### Performance: **{row['performance']}**")
    performance_badge(row["performance"])

    st.markdown("### 🧠 Likely cause")
    driver = change_driver(row["biometric_ratio"], row["demo_ratio"])
    st.write(driver)

    st.markdown("### 🛠 Recommended actions")
    for rec in recommendations(row["performance"], driver):
        st.write(f"• {rec}")

st.caption(
    "UIDAI Data-driven Innovation Hackathon | "
    "Interactive Aadhaar decision-support tool"
)

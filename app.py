import streamlit as st

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Cyber Incident Response Assistant", layout="wide")

# ---------------------------
# LANGUAGE SELECTOR
# ---------------------------
language = st.selectbox(
    "Select Language / భాష ఎంచుకోండి",
    ["English", "Telugu"]
)

# ---------------------------
# TRANSLATIONS
# ---------------------------
translations = {
    "English": {
        "title": "Cyber Incident Response Assistant",
        "describe": "Describe your cybersecurity issue below:",
        "input": "Enter your issue here:",
        "analyze": "Analyze Incident",
        "incident_detected": "Incident Detected",
        "risk_score": "Risk Score",
        "urgency": "Urgency",
        "immediate": "Immediate Actions",
        "short_term": "Short-Term Actions",
        "prevention": "Preventive Measures",
        "education": "Cyber Safety Educational Resources",
        "not_recognized": "Incident type not recognized. Please refine your description.",
        "footer": "This assistant provides guided recommendations and does not replace professional cybersecurity services."
    },
    "Telugu": {
        "title": "సైబర్ సంఘటన ప్రతిస్పందన సహాయకుడు",
        "describe": "మీ సైబర్ భద్రత సమస్యను క్రింద వివరించండి:",
        "input": "మీ సమస్యను ఇక్కడ నమోదు చేయండి:",
        "analyze": "సంఘటనను విశ్లేషించండి",
        "incident_detected": "గుర్తించిన సంఘటన",
        "risk_score": "ప్రమాద స్కోరు",
        "urgency": "తక్షణ అవసరం",
        "immediate": "తక్షణ చర్యలు",
        "short_term": "తదుపరి చర్యలు",
        "prevention": "భవిష్యత్ రక్షణ చర్యలు",
        "education": "సైబర్ భద్రత విద్యా వనరులు",
        "not_recognized": "సంఘటన గుర్తించబడలేదు. దయచేసి వివరంగా నమోదు చేయండి.",
        "footer": "ఈ సహాయకుడు సూచనలు మాత్రమే ఇస్తుంది. ఇది నిపుణుల సేవలను ప్రత్యామ్నాయం కాదు."
    }
}

# ---------------------------
# INCIDENT DATABASE
# ---------------------------
incident_database = {

    "Account Compromise": {
        "severity_score": 85,
        "keywords": ["hacked", "password changed", "account stolen", "login issue", "email hacked","suspicious login","unknown login"],
        "immediate": [
            "Reset password immediately",
            "Enable multi-factor authentication (MFA)",
            "Revoke all active sessions"
        ],
        "short_term": [
            "Check recovery email and phone number",
            "Inform contacts about possible misuse"
        ],
        "prevention": [
            "Use a password manager",
            "Avoid reusing passwords"
        ]
    },

    "Phishing Attack": {
        "severity_score": 60,
        "keywords": ["phishing", "suspicious email", "fake link", "scam email","clicked link"],
        "immediate": [
            "Do not click any more links",
            "Report the email to IT/admin",
            "Delete the suspicious message"
        ],
        "short_term": [
            "Change passwords if credentials were entered",
            "Monitor account activity"
        ],
        "prevention": [
            "Verify sender email addresses",
            "Avoid clicking unknown links"
        ]
    },

    "Malware Infection": {
        "severity_score": 75,
        "keywords": ["virus", "malware", "infected", "slow system","unknown program"],
        "immediate": [
            "Disconnect device from internet",
            "Run antivirus scan immediately",
            "Avoid accessing sensitive accounts"
        ],
        "short_term": [
            "Update operating system",
            "Remove suspicious programs"
        ],
        "prevention": [
            "Install trusted antivirus software",
            "Avoid downloading unknown files"
        ]
    },

    "Ransomware Attack": {
        "severity_score": 95,
        "keywords": ["ransomware", "files encrypted", "locked files"],
        "immediate": [
            "Disconnect device from network immediately",
            "Do NOT pay the ransom",
            "Report to cybersecurity authorities"
        ],
        "short_term": [
            "Restore files from backup if available",
            "Consult IT security professionals"
        ],
        "prevention": [
            "Maintain regular backups",
            "Keep systems updated"
        ]
    },

    "Lost / Stolen Device": {
        "severity_score": 80,
        "keywords": ["lost phone", "stolen laptop", "device stolen", "phone missing"],
        "immediate": [
            "Change passwords for important accounts",
            "Enable remote wipe if available",
            "Report the device loss to authorities"
        ],
        "short_term": [
            "Monitor financial accounts",
            "Inform organization if it is a work device"
        ],
        "prevention": [
            "Enable device encryption",
            "Use device tracking features"
        ]
    }
}

# ---------------------------
# SESSION STATE
# ---------------------------
if "matched_incident" not in st.session_state:
    st.session_state.matched_incident = None

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

# ---------------------------
# HEADER
# ---------------------------
st.title("🛡 " + translations[language]["title"])
st.write(translations[language]["describe"])

# ---------------------------
# INPUT
# ---------------------------
user_input = st.text_area(translations[language]["input"])

if st.button(translations[language]["analyze"]):
    st.session_state.analysis_done = True
    st.session_state.matched_incident = None

    user_input = user_input.lower()

    for incident, details in incident_database.items():
        for keyword in details["keywords"]:
            if keyword in user_input:
                st.session_state.matched_incident = incident
                break

# ---------------------------
# RESULTS
# ---------------------------
if st.session_state.analysis_done:

    if st.session_state.matched_incident:

        incident = st.session_state.matched_incident
        details = incident_database[incident]
        score = details["severity_score"]

        if score >= 90:
            level = "Critical"
            urgency = "Immediate action required!" if language == "English" else "తక్షణ చర్య అవసరం!"
        elif score >= 70:
            level = "High"
            urgency = "Urgent attention needed." if language == "English" else "త్వరిత చర్య అవసరం."
        elif score >= 50:
            level = "Medium"
            urgency = "Moderate risk." if language == "English" else "మధ్యస్థ ప్రమాదం."
        else:
            level = "Low"
            urgency = "Monitor the situation." if language == "English" else "పరిస్థితిని గమనించండి."

        col1, col2 = st.columns(2)

        with col1:
            st.subheader(translations[language]["incident_detected"])
            st.write(incident)

        with col2:
            st.metric(translations[language]["risk_score"], f"{score}/100")

        if level == "Critical":
            st.error(f"Severity Level: {level}")
        elif level == "High":
            st.warning(f"Severity Level: {level}")
        elif level == "Medium":
            st.info(f"Severity Level: {level}")
        else:
            st.success(f"Severity Level: {level}")

        st.write(f"**{translations[language]['urgency']}:**", urgency)

        st.markdown("---")

        st.subheader(translations[language]["immediate"])
        for i, step in enumerate(details["immediate"]):
            st.checkbox(step, key=f"{incident}_immediate_{i}")

        st.subheader(translations[language]["short_term"])
        for i, step in enumerate(details["short_term"]):
            st.checkbox(step, key=f"{incident}_short_{i}")

        st.subheader(translations[language]["prevention"])
        for i, step in enumerate(details["prevention"]):
            st.checkbox(step, key=f"{incident}_prevent_{i}")

        # ---------------------------
        # DYNAMIC EDUCATIONAL VIDEOS
        # ---------------------------
        st.markdown("---")
        st.subheader("📺 " + translations[language]["education"])

        if incident == "Account Compromise":
            st.markdown("### 🔐 How to Recover a Hacked Account")
            st.video("https://www.youtube.com/watch?v=VpJv9c2vxd4")

        elif incident == "Phishing Attack":
            st.markdown("### 🎣 How to Identify Phishing Emails")
            st.video("https://www.youtube.com/watch?v=VpJv9c2vxd4")

        elif incident == "Malware Infection":
            st.markdown("### 🦠 Understanding Malware & Removal")
            st.video("https://www.youtube.com/watch?v=VpJv9c2vxd4")

        elif incident == "Ransomware Attack":
            st.markdown("### 🛑 What To Do During Ransomware")
            st.video("https://www.youtube.com/watch?v=VpJv9c2vxd4")

        elif incident == "Lost / Stolen Device":
            st.markdown("### 📱 What To Do If Device Is Stolen")
            st.video("https://www.youtube.com/watch?v=VpJv9c2vxd4")

    else:
        st.error(translations[language]["not_recognized"])

st.markdown("---")
st.caption(translations[language]["footer"])

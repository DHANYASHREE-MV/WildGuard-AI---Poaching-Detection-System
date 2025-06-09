import streamlit as st
from PIL import Image
from backend import detect_objects
from twilio.rest import Client

# Streamlit UI Setup
st.set_page_config(page_title="Wild Guard AI", layout="centered")
st.markdown("<h1 style='text-align: center; color: white;'>🛡️ WildGuard AI - Poaching Detection System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>AI patrol because extinction can't wait</h4>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: lightgreen;'>Drag. Drop. Done.</h5>", unsafe_allow_html=True)

# Twilio credentials from Streamlit secrets
TWILIO_ACCOUNT_SID = st.secrets["twilio"]["account_sid"]
TWILIO_AUTH_TOKEN = st.secrets["twilio"]["auth_token"]
TWILIO_FROM_NUMBER = st.secrets["twilio"]["from_number"]
TWILIO_TO_NUMBER = st.secrets["twilio"]["to_number"]

# Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to send SMS
def send_alert_sms():
    try:
        message = client.messages.create(
            body="🚨 Poacher detected! Please take immediate action.",
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        st.success("✅ SMS alert sent successfully!")
    except Exception as e:
        st.error(f"❌ Failed to send SMS: {e}")

# Function to make voice call
def make_alert_call():
    try:
        call = client.calls.create(
            twiml='<Response><Say voice="alice">Alert! A poacher has been detected. Take immediate action.</Say></Response>',
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
        st.success("📞 Call alert initiated!")
    except Exception as e:
        st.error(f"❌ Failed to initiate call: {e}")

# Upload multiple images
uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Run detection
if uploaded_files:
    if st.button("Run Detection on All"):
        alert_sent = False
        for idx, uploaded_file in enumerate(uploaded_files):
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Uploaded Image {idx + 1}", use_column_width=True)

            with st.spinner(f"Processing Image {idx + 1}..."):
                result_img, found_poacher = detect_objects(image)
                st.image(result_img, caption=f"Detection Result {idx + 1}", use_column_width=True)

                if found_poacher:
                    st.warning(f"🚨 Poacher Detected in Image {idx + 1}!")
                    if not alert_sent:
                        send_alert_sms()
                        make_alert_call()
                        alert_sent = True
                else:
                    st.success(f"✅ No Poacher Detected in Image {idx + 1}.")

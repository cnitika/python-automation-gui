import os
import zipfile

# Define the full automation GUI code
full_code = '''
import streamlit as st
import pyttsx3
import speech_recognition as sr
import smtplib
import pywhatkit
import psutil
import cv2
import subprocess
from twilio.rest import Client

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"
TWILIO_ACCOUNT_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+123456789"
YOUR_PHONE_NUMBER = "+919999999999"

engine = pyttsx3.init()

def speak(text):
    st.toast(text)
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        return command.lower()
    except sr.UnknownValueError:
        speak("Could not understand. Try again.")
        return None

def send_email():
    to = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message")
    if st.button("Send Email"):
        try:
            msg = f"Subject: {subject}\\n\\n{body}"
            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.starttls()
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.sendmail(EMAIL_ADDRESS, to, msg)
            st.success("✅ Email sent!")
        except Exception as e:
            st.error(f"❌ Failed: {e}")

def send_whatsapp():
    number = st.text_input("Phone Number (+91...)")
    message = st.text_input("Message")
    hour = st.number_input("Hour (24hr)", 0, 23)
    minute = st.number_input("Minute", 0, 59)
    if st.button("Send WhatsApp"):
        try:
            pywhatkit.sendwhatmsg(number, message, int(hour), int(minute))
            st.success("📤 WhatsApp message scheduled.")
        except Exception as e:
            st.error(f"❌ Failed: {e}")

def send_sms():
    msg = st.text_input("SMS Message")
    if st.button("Send SMS"):
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=msg,
                from_=TWILIO_PHONE_NUMBER,
                to=YOUR_PHONE_NUMBER
            )
            st.success(f"📱 SMS sent. SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ Failed: {e}")

def make_call():
    if st.button("Make Phone Call"):
        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            call = client.calls.create(
                twiml='<Response><Say>This is a test call from Streamlit app.</Say></Response>',
                from_=TWILIO_PHONE_NUMBER,
                to=YOUR_PHONE_NUMBER
            )
            st.success(f"📞 Call placed. SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Failed: {e}")

def google_search():
    query = st.text_input("Search Query")
    if st.button("Search Google"):
        pywhatkit.search(query)
        st.success("🔍 Search opened in browser.")

def show_ram():
    ram = psutil.virtual_memory()
    st.info(f"Total: {ram.total / 1e+9:.2f} GB")
    st.info(f"Used: {ram.used / 1e+9:.2f} GB")
    st.info(f"Available: {ram.available / 1e+9:.2f} GB")

def take_photo():
    if st.button("Capture Photo"):
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite("captured_photo.jpg", frame)
            cam.release()
            st.image("captured_photo.jpg", caption="Captured Photo", channels="BGR")
        else:
            st.error("❌ Failed to capture photo.")
        cam.release()
        cv2.destroyAllWindows()

def run_linux_command():
    command = st.text_input("Enter Linux Command", value="ls -la")
    if st.button("Execute Linux Command"):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            st.code(output.decode())
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Command failed:\\n{e.output.decode()}")

def run_docker_command():
    command = st.text_input("Enter Docker Command", value="docker ps")
    if st.button("Run Docker Command"):
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            st.code(output.decode())
        except subprocess.CalledProcessError as e:
            st.error(f"❌ Docker command failed:\\n{e.output.decode()}")

def voice_command_router(command):
    if "email" in command:
        send_email()
    elif "whatsapp" in command:
        send_whatsapp()
    elif "sms" in command:
        send_sms()
    elif "call" in command:
        make_call()
    elif "search" in command or "google" in command:
        google_search()
    elif "ram" in command:
        show_ram()
    elif "photo" in command or "camera" in command:
        take_photo()
    elif "linux" in command:
        run_linux_command()
    elif "docker" in command:
        run_docker_command()
    else:
        speak("Sorry, command not recognized.")

def main():
    st.set_page_config(page_title="Automation Dashboard", layout="centered")
    st.title("🧠 Python Automation Dashboard")
    st.caption("Streamlit GUI + Voice + Docker + Linux + Email + WhatsApp")

    choice = st.sidebar.radio("Choose Task", (
        "🔊 Voice Command",
        "📧 Send Email",
        "💬 Send WhatsApp",
        "📱 Send SMS",
        "📞 Make Call",
        "🔍 Google Search",
        "🧠 Check RAM",
        "📸 Take Photo",
        "🐧 Run Linux Command",
        "🐳 Run Docker Command"
    ))

    if choice == "📧 Send Email":
        send_email()
    elif choice == "💬 Send WhatsApp":
        send_whatsapp()
    elif choice == "📱 Send SMS":
        send_sms()
    elif choice == "📞 Make Call":
        make_call()
    elif choice == "🔍 Google Search":
        google_search()
    elif choice == "🧠 Check RAM":
        show_ram()
    elif choice == "📸 Take Photo":
        take_photo()
    elif choice == "🐧 Run Linux Command":
        run_linux_command()
    elif choice == "🐳 Run Docker Command":
        run_docker_command()
    elif choice == "🔊 Voice Command":
        if st.button("🎤 Start Listening"):
            command = recognize_speech()
            if command:
                voice_command_router(command)

if __name__ == "__main__":
    main()
'''


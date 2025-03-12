import streamlit as st
import re
import random
import string

# Page Configuration
st.set_page_config(page_title="Password Strength Checker", page_icon="🔐", layout="centered")

# Custom CSS for Modern UI
st.markdown("""
    <style>
        body {
            background-color: #121212;
        }
        .stApp {
            background-color: #1E1E1E;
            color: white;
            padding: 20px;
            border-radius: 10px;
        }
        .title {
            text-align: center;
            color: #00ADB5;
            font-size: 30px;
            font-weight: bold;
        }
        .subtitle {
            text-align: center;
            color: #EEEEEE;
            font-size: 18px;
            margin-bottom: 20px;
        }
        .password-input {
            width: 100%;
            padding: 12px;
            font-size: 16px;
            border-radius: 8px;
            border: 2px solid #00ADB5;
            background-color: #222831;
            color: white;
        }
        .convert-button {
            background-color: #00ADB5;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px;
            width: 100%;
            text-align: center;
            cursor: pointer;
            margin-top: 10px;
        }
        .convert-button:hover {
            background-color: #008C9E;
        }
        .password-strength {
            font-weight: bold;
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            font-size: 16px;
        }
        .strong {
            background-color: #4CAF50; /* Green */
            color: white;
        }
        .medium {
            background-color: #FFC107; /* Yellow */
            color: black;
        }
        .weak {
            background-color: #F44336; /* Red */
            color: white;
        }
        .suggestions {
            background-color: #2C2F33;
            padding: 10px;
            border-radius: 10px;
            color: #CCCCCC;
        }
    </style>
""", unsafe_allow_html=True)

# Title & Description
st.markdown("<h1 class='title'>🔐 Password Strength Checker</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Check your password strength or generate a secure one instantly! 🔒</h3>", unsafe_allow_html=True)

# Function to Generate a Strong Password
def generate_strong_password(length=12):
    while True:
        password = ''.join(random.choices(
            string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*()",
            k=length
        ))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()" for c in password)):
            return password

# Generate Password Button
if st.button("🔄 Suggest a Strong Password", help="Click to generate a strong password"):
    suggested_password = generate_strong_password()
    st.session_state["password"] = suggested_password  

# Password Input Field
password = st.text_input("Enter your password:", type="password", value=st.session_state.get("password", ""), key="password_input")

# Function to Check Password Strength
def check_password_strength(password):
    feedback = []
    score = 0

    # Length Check
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("❗ Password should be at least **12 characters long**.")

    # Upper & Lower Case Check
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❗ Password should **contain both uppercase and lowercase letters**.")

    # Digit Check
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("❗ Password should **contain at least one number**.")

    # Special Character Check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("❗ Password should **contain at least one special character** [!@#$%^&*()].")

    return score, feedback

# Display Strength and Suggestions
if password:
    score, feedback = check_password_strength(password)

    # Password Strength Levels
    strength_text = ""
    strength_class = ""
    
    if score == 4:
        strength_text = "✅ **Very Strong Password! 🔥**"
        strength_class = "strong"
    elif score == 3:
        strength_text = "⚠ **Medium Strength Password!** Try making it stronger."
        strength_class = "medium"
    else:
        strength_text = "🚨 **Weak Password!** Consider improving it."
        strength_class = "weak"

    st.markdown(f"<div class='password-strength {strength_class}'>{strength_text}</div>", unsafe_allow_html=True)

    # Display Suggestions
    if feedback:
        st.markdown("<h4 style='color:#00ADB5;'>🔧 How to Improve Your Password:</h4>", unsafe_allow_html=True)
        st.markdown("<div class='suggestions'>", unsafe_allow_html=True)
        for tip in feedback:
            st.write(tip)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("📝 Start by entering a password or **click the button** to generate one!")

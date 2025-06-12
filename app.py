import streamlit as st
import re
import string
import pandas as pd
from joblib import load
from collections import Counter
import math

# --- Load ML model and label encoder ---
model = load("password_strength_model_logit_improved.joblib")  # Updated model
label_encoder = load("label_encoder.joblib")

# --- Load common passwords from your custom dataset ---
@st.cache_data
def load_common_passwords():
    df = pd.read_csv("password_dataset.csv")
    return set(df['password'].str.lower())

# --- Feature extractor (matches model training) ---
def extract_features(pwd):
    return [
        len(pwd),
        sum(c.isdigit() for c in pwd),
        sum(c.isupper() for c in pwd),
        sum(c.islower() for c in pwd),
        sum(c in string.punctuation for c in pwd),
        int(any(c.isdigit() for c in pwd)),
        int(any(c.isupper() for c in pwd)),
        int(any(c.islower() for c in pwd)),
        int(any(c in string.punctuation for c in pwd)),
    ]

# --- Rule-based password validation ---
def validate_with_rules(password, common_passwords):
    if not re.match(r'^[a-z]', password):
        return "Must start with a lowercase letter."
    if not any(c.isupper() for c in password):
        return " Must include at least one uppercase letter."
    if not re.search(r'\d', password):
        return " Must include at least one digit."
    if not re.search(r'[!@#$%^&*]', password):
        return " Must include at least one special character (!@#$%^&*)."
    if password.lower() in common_passwords:
        return " Password is too common (used in dataset)."
    
    return "✅ Passed all basic checks!"

# --- Entropy estimation ---
def estimate_entropy(password):
    if not password:
        return 0
    freq = Counter(password)
    probs = [v / len(password) for v in freq.values()]
    entropy = -sum(p * math.log2(p) for p in probs)
    return round(entropy * len(password), 2)

# --- Crack time estimators ---
def estimate_crack_time(entropy_bits, guesses_per_second):
    total_guesses = 2 ** entropy_bits
    seconds = total_guesses / guesses_per_second
    return seconds_to_human_readable(seconds)

def seconds_to_human_readable(seconds):
    units = [("years", 60*60*24*365), ("days", 60*60*24), ("hours", 60*60),
             ("minutes", 60), ("seconds", 1)]
    for name, count in units:
        if seconds >= count:
            return f"{int(seconds // count)} {name}"
    return "less than 1 second"

# --- Main Streamlit app ---
def main():
    st.title("🔐 Password Strength Checker")
    st.markdown("This tool evaluates your password using:")
    st.markdown("- ✅ **Rule-based checks**")
    st.markdown("- 🧠 **Machine Learning classification**")
    st.markdown("- 🛡️ **Entropy and Crack Time Estimation**")

    password = st.text_input("🔑 Enter your password:", type="password")

    if password:
        common_passwords = load_common_passwords()

        # Rule-based check
        rule_result = validate_with_rules(password, common_passwords)
        st.subheader(" Rule Check Result")
        st.write(rule_result)

        if "✅" in rule_result:
            # ML Prediction
            features = extract_features(password)
            pred = model.predict([features])[0]
            label = label_encoder.inverse_transform([pred])[0]
            confidence = model.predict_proba([features])[0][pred]

            st.subheader("🧠 ML Prediction")
            st.success(f"**{label}** ({confidence:.1%} confidence)")

            # Entropy & Crack Time
            entropy_bits = estimate_entropy(password)
            online_time = estimate_crack_time(entropy_bits, 1_000)              # 1K guesses/sec
            offline_time = estimate_crack_time(entropy_bits, 10_000_000_000)    # 10B guesses/sec

            st.subheader("🛡️ Crack Time Estimation")
            st.markdown(f"- **Online attack**: {online_time}")
            st.markdown(f"- **Offline attack**: {offline_time}")
            st.markdown(f"- **Estimated entropy**: {entropy_bits} bits")
        else:
            st.warning("⚠️ Password must pass all rule checks before ML and entropy analysis is run.")

# --- Run the app ---
if __name__ == "__main__":
    main()

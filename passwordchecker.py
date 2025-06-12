import pandas as pd
import re
import string
from joblib import load

# Load trained model
model = load("password_strength_model.joblib")
label_encoder = load("label_encoder.joblib")  # If you used label encoding for 'strength'

# Load custom dataset (not used for training here, just for common password checking)
df = pd.read_csv("password_dataset.csv")
common_passwords = set(df['password'].str.lower())

# Feature extractor (must match training exactly)
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

# Rule-based password validator
def validate_password(password):
    if not re.match(r'^[a-z]', password):
        return False, " Must start with a lowercase letter."
    if not re.search(r'\d', password):
        return False, " Must include at least one digit."
    if not re.search(r'[!@#$%^&*]', password):
        return False, " Must include at least one special character (!@#$%^&*)."
    if password.lower() in common_passwords:
        return False, " Password is too common (from training dataset)."

    features = extract_features(password)
    pred = model.predict([features])[0]
    label = label_encoder.inverse_transform([pred])[0]
    return True, f" Passed all rules. ML says: {label}"

# Main
def main():
    password = input("🔐 Enter a password to validate: ")
    is_valid, message = validate_password(password)
    print(message)

if __name__ == "__main__":
    main()

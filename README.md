# PassGuardML
PassGuard ML  is a hybrid password strength evaluation system combining rule-based validation, machine learning classification, entropy analysis, and crack time estimation. Trained on a custom-engineered dataset with 9+ handcrafted features, the model is deployed via Streamlit for real-time intelligent password analysis.
Key Features:
-  Rule-based password validation (start with lowercase, must contain digit, special character, etc.)
-  ML-based classification using logistic regression
-  Entropy estimation and crack time calculation
-  Trained on a custom password dataset with labeled strength levels
-  Streamlit web app for real-time password analysis
 Tech Stack
- Python
- Scikit-learn
- Pandas / NumPy
- Streamlit
- Joblib
How to Run
```bash
# Clone the repository
git clone https://github.com/yourusername/passguard-ml.git
cd passguard-ml

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```
  Project structure
 ```
passguard-ml/
├── app.py                      # Streamlit frontend
├── model_training.ipynb        # Notebook for training the ML model
├── password_dataset.csv        # Custom dataset with 9+ features
├── password_strength_model_logit_improved.joblib  # Trained model
├── label_encoder.joblib        # Label encoder for predictions
├── requirements.txt
└── README.md
```
 How It Works
- Extracts features like length, digit count, case mix, special chars, and entropy.
- Passes them into a trained logistic regression model.
- Displays the prediction (Weak / Medium / Strong) along with confidence.
- Calculates estimated time to crack using entropy (online/offline attack).
  
Future Improvements
- Add keyboard pattern detection.
- Use stronger ML models like XGBoost or RandomForest
- Deploy online using Streamlit Cloud

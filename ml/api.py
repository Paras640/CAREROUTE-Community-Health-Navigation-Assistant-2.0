from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os

app = FastAPI(title="CareRoute ML API", description="API for Decision Tree Disease Predictions")

# Allow local browser-based API tools to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define paths relative to this file
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'model.pkl')
encoder_path = os.path.join(base_dir, 'label_encoder.pkl')
features_path = os.path.join(base_dir, 'feature_names.pkl')

try:
    model = joblib.load(model_path)
    label_encoder = joblib.load(encoder_path)
    feature_names = joblib.load(features_path)
    print(f"Model loaded successfully. Knows {len(feature_names)} features and {len(label_encoder.classes_)} diseases.")
except FileNotFoundError:
    model = None
    label_encoder = None
    feature_names = []
    print("Warning: Artifacts not found. Run train_model.py first.")

@app.get("/")
def read_root():
    return {"status": "CareRoute ML API is running."}

@app.post("/predict")
async def predict(request: Request):
    """
    Expects a JSON payload where keys are symptom names (from the 377 training features)
    and values are 1 (present) or 0 (absent).
    Any symptoms not provided are automatically set to 0.

    Example: {"headache": 1, "fever": 1, "chills": 1}
    Returns: {"disease": "viral fever"}
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model artifacts are missing. Add the training dataset and run "
            "`python ml/train_model.py` from the repository root.",
        )

    user_symptoms = await request.json()
    if not isinstance(user_symptoms, dict):
        raise HTTPException(status_code=400, detail="Request body must be a JSON object.")

    # Build full feature vector initialized to 0
    input_data = {feat: 0 for feat in feature_names}

    # Fill in symptoms provided by user
    matched = 0
    for sym, val in user_symptoms.items():
        if sym in input_data:
            input_data[sym] = val
            matched += 1

    # Convert to DataFrame in the exact column order the model expects
    df = pd.DataFrame([input_data])

    # Predict numeric class and decode to disease string
    prediction_num = model.predict(df)[0]
    disease_name = label_encoder.inverse_transform([prediction_num])[0]

    return {
        "disease": disease_name,
        "symptoms_matched": matched,
    }

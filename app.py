import joblib
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI

model = joblib.load("model/dropout-lgbm-model.pkl")
features = joblib.load("model/features.pkl")

app = FastAPI(title="Student Dropout Prediction")

#Input design. Frontend sends only what it knows
class StudentInput(BaseModel):
    data: dict

def prediction_label(pred):
    if pred==1:
        return "Dropout"
    else:
        return "Not Dropout"

def risk_label(proba):
    if proba>=0.6:
        return "High Risk"
    elif proba>=0.2:
        return "Medium Risk"
    else:
        return "Low Risk"
    
#API enpoint
@app.post("/predict")
def predict_output(input: StudentInput):
    sample = {f: 0 for f in features}

    for key, value in input.data.items():
        if key in sample: 
            sample[key] = value

#Convert into 2D input with correct column order
    df = pd.DataFrame([sample])
    df = df.reindex(columns=features, fill_value=0)

#Actual model prediction
    proba = model.predict_proba(df)[0][1]

    THRESHOLD = 0.2 #modified threshold
    prediction = int(proba>=THRESHOLD)

#Return everything useful
    return {
    "dropout_probability" : round(proba,3),
    "prediction": prediction_label(prediction),
    "risk_category": risk_label(proba)
    }
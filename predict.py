#Check prediction
import joblib
import pandas as pd

model = joblib.load("dropout-lgbm-model.pkl")
features = joblib.load("features.pkl")

THRESHOLD = 0.2

def risk_bucket(p):
    if p>=0.6:
        return "High Risk"
    elif p>=0.3:
        return "Medium Risk"
    else:
        return "Low Risk"

#Replace all columns with 0
sample = {f: 0 for f in features}

#Fill in whatever user has sent
sample["Age at enrollment"] = 21
sample["Tuition fees up to date"] = 1
sample["Curricular units 1st sem (approved)"] = 3
sample["Curricular units 1st sem (grade)"] = 11.5
sample["Curricular units 2nd sem (approved)"] = 2
sample["Curricular units 2nd sem (grade)"] = 10.0

input_df = pd.DataFrame([sample])
input_df = input_df.reindex(columns=features, fill_value=0)

proba = model.predict_proba(input_df)[0][1]

print("Probability:",proba)
print("Risk: ",risk_bucket(proba))

#Works. Now use same logic in API
import pandas as pd
import matplotlib.pyplot as plt

#def risk_bucket(p):
#    if p>=0.6:
#       return "High Risk"
#    elif p>=0.2:
#        return "Medium Risk"
#    else:
#        return "Low Risk"

df = pd.read_csv('data.csv',sep=';')
#Feature encoding not needed since all data already numerical

df["dropout"] = df["Target"].map({
    "Dropout": 1,
    "Graduate": 0,
    "Enrolled": 0
})

df = df.drop(columns=["Target"])
df = df.drop(columns=["International","Educational special needs"])#Dropped some features - simplified trees

X = df.drop(columns=["dropout"])
y = df["dropout"]

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,stratify=y,random_state=42)

from lightgbm import LGBMClassifier
model = LGBMClassifier(
    n_estimators=200,
    learning_rate=0.05,
     random_state=42
)

model.fit(X_train,y_train)
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:,1]#roc_auc uses probabilities
#Threshold tuning
for t in [0.2,0.3,0.4,0.5]:
    y_pred = (y_proba >=t ).astype(int)
    #print(t)
    #print(classification_report(y_test,y_pred))
y_pred_tuned = (y_proba >=0.2).astype(int)

from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix,classification_report
print("ROC AUC score: ",roc_auc_score(y_test,y_proba))
print(confusion_matrix(y_test,y_pred_tuned))
print(classification_report(y_test,y_pred_tuned))

#Feature Importance - Which features affected the result most
imp = pd.DataFrame({
    "feature":X.columns,
    "importance":model.feature_importances_
}).sort_values(by="importance",ascending=False)

plt.barh(
    imp["feature"][:],
    imp["importance"][:]
)
plt.gca().invert_yaxis()
plt.show()

#Save model artifacts
import joblib

joblib.dump(model,"dropout-lgbm-model.pkl")
joblib.dump(X.columns.tolist(),"features.pkl")





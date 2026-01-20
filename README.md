Imported Student Dropout Prediction UCI Machine Learning Repository
Did exploratory data analysis on the dataset
Understood what each feature meant and denoted
Target column was categorical so encoded it
Used tran test split on the data to split into training and testing data
Used a LightGBM Classifier to classify students into Dropout and Not Dropout classes
LightGBM is used because
- it predicts probabilities
- it learns from the decision tree it creates so results produced are very accurate
Used ROC AUC score to check correctness of the model
Ran a feature importance test on the model
Plotted the top 10 most important features on bar graph using matplotlib
Dropped columns not needed as they created noise
Saved the model using joblib
Created a Streeamlit dashboard to take inputs and display result
Connected it to the API and displayed risk level, prediction and prediction probability

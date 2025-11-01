# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# 1. Load dataset
df = pd.read_csv('engine_data.csv')

print("Dataset loaded successfully!")
print(df.head())

# 2. Define features (X) and target (y)
X = df[['Engine rpm', 'Lub oil pressure', 'Fuel pressure', 'Coolant pressure',
        'lub oil temp', 'Coolant temp']]
y = df['Engine Condition']

# 3. Split into training & testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train a Random Forest Classifier
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate model performance
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\nModel Accuracy: {acc*100:.2f}%\n")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 6. Save trained model
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\n Model trained and saved successfully as 'model.pkl'!")


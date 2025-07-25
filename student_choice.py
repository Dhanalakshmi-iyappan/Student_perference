# -*- coding: utf-8 -*-
"""student_choice.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CfSM0SJsQkxZvM3WopP8jwFzQBa0F_EB
"""

# Install required packages if not already installed
!pip install xgboost lightgbm catboost scikit-learn pandas

# Step 1: Load the Data
import pandas as pd

columns = pd.read_csv("columns.csv")
responses = pd.read_csv("responses.csv")

# Optional: set column names if `columns.csv` is metadata
# responses.columns = columns['column_name']

# Step 2: Preprocessing
responses.dropna(inplace=True)  # Remove missing values

# Example: Assuming the last column is the target
X = responses.iloc[:, :-1]
y = responses.iloc[:, -1]

# Encode categorical features if any
from sklearn.preprocessing import LabelEncoder

for col in X.select_dtypes(include=['object']).columns:
    X[col] = LabelEncoder().fit_transform(X[col])

# Encode target if it's categorical
if y.dtype == 'object':
    y = LabelEncoder().fit_transform(y)

# Step 3: Train-test Split
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

from xgboost import XGBClassifier
from sklearn.ensemble import AdaBoostClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

models = {
    "XGBoost": XGBClassifier(eval_metric='logloss'),
    "AdaBoost": AdaBoostClassifier(),
    "CatBoost": CatBoostClassifier(verbose=0),

}

# Train and evaluate
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"{name} Accuracy: {acc:.4f}")

import re

def clean_column(col):
    return re.sub(r'[^\w]', '_', str(col))  # Replace non-word characters with underscores

X_train.columns = [clean_column(col) for col in X_train.columns]
X_test.columns = X_train.columns
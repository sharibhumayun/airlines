# -*- coding: utf-8 -*-
"""app.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fQzo4--qVABFSZ-cRHjPnxXF-7NdOOX9
"""

!pip install streamlit
import streamlit as st
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
import numpy as np

# Load and preprocess the data
def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/sharibhumayun/airlines/main/airline_passenger_satisfaction.csv')
    label_enc = LabelEncoder()
    data['Satisfaction'] = label_enc.fit_transform(data['Satisfaction'])
    categorical_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
    return data

# Preprocess the data
def preprocess_data(data):
    X = data[['Departure and Arrival Time Convenience', 'Ease of Online Booking', 'Check-in Service',
              'Online Boarding', 'Gate Location', 'On-board Service', 'Seat Comfort', 'Leg Room Service',
              'Cleanliness', 'Food and Drink', 'In-flight Service', 'In-flight Wifi Service',
              'In-flight Entertainment', 'Baggage Handling']]
    y = data['Satisfaction']

    # Define preprocessing pipeline
    preprocess_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    X = preprocess_pipeline.fit_transform(X)

    return X, y, preprocess_pipeline

# Train the model
def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model

# Predict satisfaction
def predict_satisfaction(model, input_data, preprocess_pipeline):
    input_df = pd.DataFrame([input_data])
    input_df = preprocess_pipeline.transform(input_df)  # Apply the same preprocessing
    prediction = model.predict(input_df)
    return 'Satisfied' if prediction[0] == 1 else 'Neutral or Dissatisfied'

# Main function to run the Streamlit app
def main():
    st.title("Airline Passenger Satisfaction Prediction")

    st.write("Please enter the details to predict satisfaction:")

    input_data = {
        'Departure and Arrival Time Convenience': st.number_input('Departure and Arrival Time Convenience', min_value=0, max_value=5, value=3),
        'Ease of Online Booking': st.number_input('Ease of Online Booking', min_value=0, max_value=5, value=3),
        'Check-in Service': st.number_input('Check-in Service', min_value=0, max_value=5, value=3),
        'Online Boarding': st.number_input('Online Boarding', min_value=0, max_value=5, value=3),
        'Gate Location': st.number_input('Gate Location', min_value=0, max_value=5, value=3),
        'On-board Service': st.number_input('On-board Service', min_value=0, max_value=5, value=3),
        'Seat Comfort': st.number_input('Seat Comfort', min_value=0, max_value=5, value=3),
        'Leg Room Service': st.number_input('Leg Room Service', min_value=0, max_value=5, value=3),
        'Cleanliness': st.number_input('Cleanliness', min_value=0, max_value=5, value=3),
        'Food and Drink': st.number_input('Food and Drink', min_value=0, max_value=5, value=3),
        'In-flight Service': st.number_input('In-flight Service', min_value=0, max_value=5, value=3),
        'In-flight Wifi Service': st.number_input('In-flight Wifi Service', min_value=0, max_value=5, value=3),
        'In-flight Entertainment': st.number_input('In-flight Entertainment', min_value=0, max_value=5, value=3),
        'Baggage Handling': st.number_input('Baggage Handling', min_value=0, max_value=5, value=3),
    }

    if st.button('Predict Satisfaction'):
        data = load_data()
        X, y, preprocess_pipeline = preprocess_data(data)
        model = train_model(X, y)
        result = predict_satisfaction(model, input_data, preprocess_pipeline)
        st.success(f'The predicted satisfaction is: {result}')

if __name__ == "__main__":
    main()


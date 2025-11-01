import streamlit as st
import numpy as np
import pickle
import os

# Load model
if os.path.exists('model.pkl'):
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
else:
    st.warning("Model file not found. Running in demo mode without predictions.")
    model = None

# Customized feature ranges based on your dataset
custom_ranges = {
    'Engine rpm': (61.0, 2239.0),
    'Lub oil pressure': (0.003384, 7.265566),
    'Fuel pressure': (0.003187, 21.138326),
    'Coolant pressure': (0.002483, 7.478505),
    'lub oil temp': (71.321974, 89.580796),
    'Coolant temp': (61.673325, 195.527912)
}

# Feature Descriptions
feature_descriptions = {
    'Engine rpm': 'Revolutions per minute of the engine.',
    'Lub oil pressure': 'Pressure of the lubricating oil.',
    'Fuel pressure': 'Pressure of the fuel.',
    'Coolant pressure': 'Pressure of the coolant.',
    'lub oil temp': 'Temperature of the lubricating oil.',
    'Coolant temp': 'Temperature of the coolant.'
}

def main():
    st.title("🚚 Predictive Maintenance System for Logistics Fleet")
    st.markdown("Monitor vehicle engine parameters and predict maintenance needs in real-time.")

    # Sidebar info
    st.sidebar.title("Feature Descriptions")
    for feature, description in feature_descriptions.items():
        st.sidebar.markdown(f"**{feature}:** {description}")

    # Input sliders
    engine_rpm = st.slider("Engine RPM", *custom_ranges['Engine rpm'])
    lub_oil_pressure = st.slider("Lub Oil Pressure (bar)", *custom_ranges['Lub oil pressure'])
    fuel_pressure = st.slider("Fuel Pressure (bar)", *custom_ranges['Fuel pressure'])
    coolant_pressure = st.slider("Coolant Pressure (bar)", *custom_ranges['Coolant pressure'])
    lub_oil_temp = st.slider("Lubrication Oil Temperature (°C)", *custom_ranges['lub oil temp'])
    coolant_temp = st.slider("Coolant Temperature (°C)", *custom_ranges['Coolant temp'])

    # Predict button
    if st.button("Predict Engine Condition"):
        if model:
            result, confidence = predict_condition(engine_rpm, lub_oil_pressure, fuel_pressure,
                                                  coolant_pressure, lub_oil_temp, coolant_temp)

            if result == 0:
                st.success(f"✅ Engine Condition: Normal\n\nConfidence: {(1.0 - confidence):.2%}")
            else:
                st.warning(f"⚠️ Engine Condition: Faulty / Maintenance Required\n\nConfidence: {confidence:.2%}")
        else:
            st.error("Model not loaded — please train or place 'model.pkl' in the project folder.")

    if st.button("Reset Values"):
        st.experimental_rerun()

def predict_condition(engine_rpm, lub_oil_pressure, fuel_pressure, coolant_pressure, lub_oil_temp, coolant_temp):
    input_data = np.array([[engine_rpm, lub_oil_pressure, fuel_pressure, coolant_pressure, lub_oil_temp, coolant_temp]])
    prediction = model.predict(input_data)
    confidence = model.predict_proba(input_data)[:, 1]
    return prediction[0], confidence[0]

if __name__ == "__main__":
    main()

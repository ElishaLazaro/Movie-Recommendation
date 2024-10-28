from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import os

# Create a Blueprint instance
routes_bp = Blueprint('routes_bp', __name__)

# Define absolute paths to model files
base_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.join(base_dir, 'model')

model_path = os.path.join(model_dir, 'model.pkl')
selected_features_path = os.path.join(model_dir, 'selected_features.pkl')
label_encoders_path = os.path.join(model_dir, 'label_encoders.pkl')
label_encoder_rating_path = os.path.join(model_dir, 'label_encoder_rating.pkl')

# Verify all model files exist before loading
required_files = [
    model_path,
    selected_features_path,
    label_encoders_path,
    label_encoder_rating_path
]

for file_path in required_files:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Required model file not found: {file_path}")

# Load model and encoders
model = joblib.load(model_path)
selected_features = joblib.load(selected_features_path)
label_encoders = joblib.load(label_encoders_path)
le_rating = joblib.load(label_encoder_rating_path)

@routes_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Flask API is running.'})

@routes_bp.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Validate input
    missing_features = [feature for feature in selected_features if feature not in data]
    if missing_features:
        return jsonify({'error': f'Missing features: {missing_features}'}), 400
    
    input_data = []
    for feature in selected_features:
        value = data[feature]
        # Encode categorical features
        if feature in label_encoders:
            le = label_encoders[feature]
            try:
                value = le.transform([value])[0]
            except ValueError:
                return jsonify({'error': f'Invalid value for feature: {feature}'}), 400
        input_data.append(value)
    
    input_array = np.array(input_data).reshape(1, -1)
    
    # Make prediction
    prediction_encoded = model.predict(input_array)[0]
    prediction = le_rating.inverse_transform([prediction_encoded])[0]  # Decode the prediction
    
    return jsonify({'prediction': prediction})

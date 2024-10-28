import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import os

def train_and_evaluate(input_path):
    try:
        # Load preprocessed data
        df = pd.read_csv(input_path)
        print("Preprocessed Data Shape:", df.shape)
        
        # Load selected features
        model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app', 'model')
        selected_features = joblib.load(os.path.join(model_dir, 'selected_features.pkl'))
        print("Selected Features:", selected_features)
        
        X = df[selected_features]
        y = df['Rating']  # Already encoded

        # Check class distribution
        print(y.value_counts())

        # Remove classes with fewer than 2 instances
        min_class_count = 2
        class_counts = y.value_counts()
        classes_to_keep = class_counts[class_counts >= min_class_count].index

        # Filter DataFrame to keep only the relevant classes
        df = df[df['Rating'].isin(classes_to_keep)]

        # Update X and y after filtering
        X = df[selected_features]
        y = df['Rating']

        # Now you can safely split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42, stratify=y)
        print(f"Training Set: {X_train.shape}, Test Set: {X_test.shape}")
        
        # Train model
        model = GaussianNB()
        model.fit(X_train, y_train)
        print("Model training completed.")
        
        # Evaluate model
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc:.2f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        # Save the trained model
        joblib.dump(model, os.path.join(model_dir, 'model.pkl'))
        print("Saved trained model.")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_csv = os.path.join(project_root, 'data', 'preprocessed_imdb-movies-dataset.csv')
    train_and_evaluate(input_csv)

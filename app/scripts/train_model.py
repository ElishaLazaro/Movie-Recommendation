import os
from collections import Counter

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB


def train_and_evaluate(input_path):
    try:
        # Load preprocessed data
        df = pd.read_csv(input_path)
        print("Preprocessed Data Shape:", df.shape)

        # Load selected features
        selected_features = joblib.load(
            os.path.join("app/model", "selected_features.pkl")
        )
        print("Selected Features:", selected_features)

        X = df[selected_features]
        y = df["Id"]  # Assume id is already encoded or binned

        # Check class distribution
        class_counts = Counter(y)
        print("Class distribution in target variable:", class_counts)

        # Adjust split if necessary
        if any(count < 2 for count in class_counts.values()):
            print(
                "Stratification not possible due to classes with fewer than 2 samples."
            )
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.10, random_state=42
            )
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.10, random_state=42, stratify=y
            )

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
        joblib.dump(model, os.path.join("model", "model.pkl"))
        print("Saved trained model.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    input_csv = "data/preprocessed_movie.csv"
    train_and_evaluate(input_csv)

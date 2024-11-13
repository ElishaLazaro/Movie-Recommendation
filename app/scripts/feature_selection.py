import os

import joblib
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2


def select_features(input_path, output_path, k=10):
    try:
        # Load preprocessed data
        df = pd.read_csv(input_path)
        print("Preprocessed Data Shape:", df.shape)

        # Separate features and target
        X = df.drop(columns=["Id"])
        y = df["Id"]

        # Select top k features using Chi-Squared test
        selector = SelectKBest(score_func=chi2, k=k)
        selector.fit(X, y)

        selected_features = X.columns[selector.get_support()]
        print("Selected Features:", list(selected_features))

        # Save selected features
        model_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "model"
        )
        joblib.dump(
            list(selected_features), os.path.join(model_dir, "selected_features.pkl")
        )
        print("Saved selected features.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    input_csv = os.path.join(project_root, "data", "preprocessed_movie.csv")
    select_features(input_csv, input_csv, k=10)  # You can adjust 'k' as needed

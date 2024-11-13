import os

import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_data(input_path, output_path):
    # Load data
    df = pd.read_csv(input_path)
    print("Original Data Shape:", df.shape)
    df = df.drop(columns=["Title"])
    df = df.drop(columns=["Poster"])
    df = df.drop(columns=["Metascore"])
    df = df.drop(columns=["Director"])
    df = df.drop(columns=["Cast"])
    df = df.drop(columns=["Description"])
    df = df.drop(columns=["Review Count"])
    df = df.drop(columns=["Review Title"])
    df = df.drop(columns=["Review"])
    df = df.drop(columns=["Votes"])

    # Drop missing values
    df = df.dropna()
    print("After Dropping Missing Values:", df.shape)

    # Identify categorical features
    categorical_features = [
        "Year",
        "Certificate",
        "Duration (min)",
        "Genre",
        "Rating",
    ]

    # Encode categorical features
    label_encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"Encoded {col}")

    # Save label encoders
    model_dir = os.path.join("app", "model")
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(label_encoders, os.path.join(model_dir, "label_encoders.pkl"))
    print("Saved label encoders.")

    # Encode the target variable 'grade'
    le_grade = LabelEncoder()
    df["Id"] = le_grade.fit_transform(df["Id"])
    joblib.dump(le_grade, os.path.join(model_dir, "label_encoder_id.pkl"))
    print("Encoded and saved label encoder for target variable 'id'.")

    # Save preprocessed data
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")


if __name__ == "__main__":
    input_csv = os.path.join("data", "imdb-movies-dataset.csv")
    output_csv = os.path.join("data", "preprocessed_movie.csv")
    preprocess_data(input_csv, output_csv)

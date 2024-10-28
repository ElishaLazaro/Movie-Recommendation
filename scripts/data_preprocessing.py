import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def preprocess_data(input_path, output_path):
    # Load data
    df = pd.read_csv(input_path)
    print("Original Data Shape:", df.shape)
    df = df.drop(columns=['Id'])
    
    # Drop missing values
    df = df.dropna()
    print("After Dropping Missing Values:", df.shape)

    if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
            print("Dropped 'Unnamed: 0' column.")
    
    # Identify categorical features
    categorical_features = ['Poster','Title','Year','Certificate','Duration (min)',
                            'Genre','Rating','Metascore','Director','Cast','Votes','Description',
                            'Review Count','Review Title','Review'
                        ]
    
    # Encode categorical features
    label_encoders = {}
    for col in categorical_features:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
        print(f"Encoded {col}")
    
    # Save label encoders
    model_dir = os.path.join('app', 'model')
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(label_encoders, os.path.join(model_dir, 'label_encoders.pkl'))
    print("Saved label encoders.")

     # Encode the target variable 'Rating'
    le_rating = LabelEncoder()
    df['Rating'] = le_rating.fit_transform(df['Rating'])
    joblib.dump(le_rating, os.path.join(model_dir, 'label_encoder_rating.pkl'))
    print("Encoded and saved label encoder for target variable 'rating'.")
    
    # Save preprocessed data
    df.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    input_csv = os.path.join('data', 'imdb-movies-dataset.csv')
    output_csv = os.path.join('data', 'preprocessed_imdb-movies-dataset.csv')
    preprocess_data(input_csv, output_csv)

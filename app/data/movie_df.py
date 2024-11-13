import pandas as pd


def get_movie_data() -> pd.DataFrame:
    try:

        with open("./app/data/imdb-movies-dataset.csv", "r", encoding="utf-8") as movie_csv:
            movie_df = pd.read_csv(movie_csv)

            return movie_df

    except:
        return pd.DataFrame()

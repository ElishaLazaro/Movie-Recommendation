from base64 import b64decode
from urllib import parse

from flask import json

from app.data import movie_df as mdf

movie_df = mdf.get_movie_data()


def movie_by_genre(query, limit, offset=5):
    print(query["g"])
    q_genre = json.loads(b64decode(parse.unquote(query["g"])))

    filtered_movies = movie_df[movie_df["Genre"].isin(q_genre)]

    if filtered_movies.shape[0] > offset:
        result = filtered_movies.iloc[offset : offset + limit]
        print(result)
    else:
        result = filtered_movies

    return result.to_json(orient="records")


def movie_by_year(query, limit):
    # Convert the lower and upper bounds of the year range to integers
    q_year_min = int(query["y_min"])
    q_year_max = int(query["y_max"])

    # Filter the DataFrame for movies within the specified year range
    return (
        movie_df[(movie_df["Year"] >= q_year_min) & (movie_df["Year"] <= q_year_max)]
        .head(limit)
        .to_json(orient="records")
    )


def movie_by_rating(query, limit):
    # Convert the lower and upper bounds of the rating range to floats
    q_rating_min = float(query["r_min"])
    q_rating_max = float(query["r_max"])

    # Filter the DataFrame for movies within the specified rating range
    return (
        movie_df[
            (movie_df["Rating"] >= q_rating_min) & (movie_df["Rating"] <= q_rating_max)
        ]
        .head(limit)
        .to_json(orient="records")
    )


def movie_by_metascore(query, limit):
    q_metascore = float(query["s"])
    return (
        movie_df[movie_df["Metascore"] == q_metascore]
        .head(limit)
        .to_json(orient="records")
    )


def movie_most_rated(limit):
    # F
    return (
        movie_df.sort_values("Rating", ascending=False)
        .head(limit)
        .to_json(orient="records")
    )


def movie_profile(query):
    movie_id = int(query["movie_id"])
    return movie_df[movie_df["Id"] == movie_id].to_json(orient="records")

import joblib
import numpy as np
from flask import Blueprint, Response, json, jsonify, redirect, request

from app.scripts import movie_functions

# Create a Blueprint instance
routes_bp = Blueprint("routes_bp", __name__)


# root redirect to index
@routes_bp.get("/")
def redirect_to_index():
    return redirect("/index.html")


@routes_bp.route("/movie", methods=["GET"])
def get_movie() -> Response:
    # instantiate response object
    response = Response()
    # set content-type to json
    response.mimetype = "application/json"

    query = get_query(request)

    q_by = query["by"]
    q_limit = int(query["limit"])

    try:
        # do something...

        df_result = ""

        match q_by:
            case "genre":
                df_result = movie_functions.movie_by_genre(query, q_limit)
            case "year":
                df_result = movie_functions.movie_by_year(query, q_limit)
            case "rating":
                df_result = movie_functions.movie_by_rating(query, q_limit)
            case "metascore":
                df_result = movie_functions.movie_by_metascore(query, q_limit)

        if df_result:
            df_result = json.loads(df_result)

        # end do something...

        # set the status of the response
        response.status = 200
        # encode dict to json
        json_encoded = json.dumps(
            {"message": "Success on retrieving data", "data": df_result}
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response

    except Exception as err:
        # set the status of the response
        response.status = 500
        # encode dict to json
        json_encoded = json.dumps(
            {"message": "There was an error.", "error": err.__str__()}
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response


@routes_bp.route("/movie/top/rated", methods=["GET"])
def get_top_rated() -> Response:
    # instantiate response object
    response = Response()
    # set content-type to json
    response.mimetype = "application/json"

    query = get_query(request)
    q_limit = int(query["limit"])

    try:
        # do something...

        df_result = ""

        df_result = movie_functions.movie_most_rated(q_limit)

        if df_result:
            df_result = json.loads(df_result)

        # end do something...

        # set the status of the response
        response.status = 200
        # encode dict to json
        json_encoded = json.dumps(
            {
                "message": "Success on retrieving data",
                "data": df_result,
            }
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response

    except Exception as err:
        # set the status of the response
        response.status = 500
        # encode dict to json
        json_encoded = json.dumps(
            {"message": "There was an error.", "error": err.__str__()}
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response


@routes_bp.route("/movie/profile", methods=["GET"])
def get_movie_profile() -> Response:
    # instantiate response object
    response = Response()
    # set content-type to json
    response.mimetype = "application/json"

    query = get_query(request)

    try:
        # do something...

        df_result = ""

        df_result = movie_functions.movie_profile(query)

        if df_result:
            df_result = json.loads(df_result)
            df_result = df_result[0]

        # end do something...

        # set the status of the response
        response.status = 200
        # encode dict to json
        json_encoded = json.dumps(
            {"message": "Success on retrieving data", "data": df_result}
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response

    except Exception as err:
        # set the status of the response
        response.status = 500
        # encode dict to json
        json_encoded = json.dumps(
            {"message": "There was an error.", "error": err.__str__()}
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response


@routes_bp.post("/predict")
def predict():
    model = joblib.load("./app/model/model.pkl")
    selected_features = joblib.load("./app/app/model/selected_features.pkl")
    label_encoders = joblib.load("./app/app/model/label_encoders.pkl")
    le_id = joblib.load("./app/app/model/label_encoder_id.pkl")

    # instantiate response object
    response = Response()
    # set content-type to json
    response.mimetype = "application/json"

    try:
        # do something...
        data = request.get_json()

        # Validate input
        missing_features = [
            feature for feature in selected_features if feature not in data
        ]
        if missing_features:
            return jsonify({"error": f"Missing features: {missing_features}"}), 400

        input_data = []
        for feature in selected_features:
            value = data[feature]
            # Encode categorical features
            if feature in label_encoders:
                le = label_encoders[feature]
                try:
                    value = le.transform([value])[0]
                except ValueError:
                    return (
                        jsonify({"error": f"Invalid value for feature: {feature}"}),
                        400,
                    )
            input_data.append(value)

        input_array = np.array(input_data).reshape(1, -1)

        # Make prediction
        prediction_encoded = model.predict(input_array)[0]
        prediction = le_id.inverse_transform([prediction_encoded])[
            0
        ]  # Decode the prediction

        prediction = int(prediction)
        prediction = movie_functions.movie_profile({"movie_id": prediction})
        if prediction:
            prediction = json.loads(prediction)

        # end do something...

        json_encoded = ""
        # set the status of the response
        response.status = 200
        # encode dict to json
        if prediction:
            json_encoded = json.dumps(
                {"message": "Success on retrieving data", "predict": prediction[0]}
            )

        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response

    except Exception as err:
        # set the status of the response
        response.status = 500
        # encode dict to json
        json_encoded = json.dumps(
            {"message": "There was an error.", "error": err.__str__()}
        )
        # set the json_encoded to response
        response.set_data(json_encoded)

        # send the response to the client
        return response


def get_query(request):

    queries = request.query_string.decode("utf-8")
    queries = queries.split("&")

    query_dict = {}

    for query in queries:
        split_qstring = query.split("=")
        query_dict[split_qstring[0]] = split_qstring[1]

    return query_dict

# Gitty --- IBM Summer Project 2019
# Kavan Lam and Nimrah Gill
# July 19, 2019


### Importing required modules ###
from flask import Flask as fk
from flask import jsonify, request
from flask_cors import CORS
from model_predict import *
from model_creation import *


# Initialize the Flask app
app = fk(__name__)
CORS(app)


### Defining all routes for the app ###
@app.route("/make_prediction", methods=["POST"])
def make_prediction():
    issue_text = request.get_json(force=True)
    response = model_prediction(issue_text["git_issue_text"])
    if response != 500:
        return (jsonify({"best_assignees": response[0], "best_teams": response[1]}))
    return "Error occurred during model prediction", 500


@app.route("/make_models")
def make_models():
    accuracy = model_creation()
    if accuracy != 500:
        return (jsonify({"team_accuracy": accuracy[-2], "assignee_accuracy": accuracy[-1]}))
    return "Error occurred during model production", 500


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Constants 
BASE_API_URL = "https://api.langflow.astra.datastax.com" 
LANGFLOW_ID = "d279e60e-480d-43bf-9b92-55733063b9d5"
FLOW_ID = "03f3eff6-f412-4370-8967-df46584100e4"
APPLICATION_TOKEN = os.getenv("APP_TOKEN")
ENDPOINT = "03f3eff6-f412-4370-8967-df46584100e4"  # Endpoint name in flow settings


def run_flow(message: str) -> dict:
    """Function to send a message to the Langflow API and retrieve the response."""
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()  # Raise exception if the request fails
    return response.json()


@app.route("/", methods=["GET"])
def index():
    """Render the index.html page."""
    return render_template("index.html")

@app.route("/insight")
def insight():
    """Render the insight.html page."""
    return render_template("insight.html")

@app.route('/features')
def features():
    # Path to the CSV file
    csv_path = r'static\social_media_data.csv'
    if not os.path.exists(csv_path):
        return "CSV file not found!", 404

    # Read the CSV file
    data = pd.read_csv(csv_path)

    # Convert to a list of dictionaries for Jinja2 compatibility
    data_rows = data.to_dict(orient='records')  # Each row as a dictionary
    data_columns = list(data.columns)  # Column headers

    # Check if data is empty
    if not data_rows or not data_columns:
        return "No data available!", 404

    # Pass data to the template
    return render_template('features.html', data_rows=data_rows, data_columns=data_columns)

@app.route("/about", methods=["GET"])
def about():
    """Render the about.html page."""
    return render_template("about.html")

@app.route("/contact", methods=["GET"])
def contact():
    """Render the contact.html page."""
    return render_template("contact.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    API endpoint for the chatbot.
    Expects JSON input: { "message": "Your question here" }
    Returns JSON response from Langflow API.
    """
    try:
        data = request.get_json()

        if not data or "message" not in data or not data["message"].strip():
            return jsonify({"error": "Invalid request. 'message' field is required."}), 400

        message = data["message"]

        # Call Langflow API
        langflow_response = run_flow(message)

        # Extract the chatbot's response
        response_text = langflow_response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

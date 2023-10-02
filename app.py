from flask import Flask, request, jsonify, render_template
from outscraper import ApiClient
from bs4 import BeautifulSoup
import os

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = os.environ.get("API_KEY")

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_reviews():
    # Get input data from the POST request
    place_id = request.form.get('place_id')
    limit = request.form.get('limit')
    filter = request.form.get('filter')

    try:
        # Initialize the Outscraper API client
        api_client = ApiClient(api_key=API_KEY)

        # Use the library to fetch Google Maps reviews
        results = api_client.google_maps_reviews(place_id, reviews_limit=int(limit), reviews_query= filter)
        print(results)
        review_data = results[0]['reviews_data']
        venue_name = results[0]['name']

        # Return the parsed data as JSON
        return jsonify({"name": venue_name, "reviews": review_data})
    
    except Exception as e:
        # Handle API request errors here
        error_message = str(e)
        return jsonify({'error': error_message}), 500  # Return a 500 Internal Server Error status

if __name__ == '__main__':
    app.run(debug=True)
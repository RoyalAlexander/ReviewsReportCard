from flask import Flask, request, jsonify, render_template
from outscraper import ApiClient

# Replace 'YOUR_API_KEY' with your actual API key
API_KEY = 'Z29vZ2xlLW9hdXRoMnwxMTYwNjM3MDIzMjEyMTM2NTc0ODR8MDllZTg5YjRlMQ'

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_reviews():
    # Get input data from the POST request
    place_id = request.form.get('place_id')
    
    # Default the review limit to 2 if no limit is provided
    limit = request.form.get('limit', 2)
    limit = int(limit)

    try:
        # Initialize the Outscraper API client
        api_client = ApiClient(api_key=API_KEY)

        # Use the library to fetch Google Maps reviews
        results = api_client.google_maps_reviews(place_id, reviews_limit=limit)

        if not results:
            return jsonify({'message': 'Query successful, no matching reviews found.'})

        # Transform the reviews to match your desired structure
        parsed_data = []
        for review in results:
            review_data = {
                'review_author': review.get('review_author', '').strip(),
                'review_rating': int(review.get('review_rating', 0)),
                'review_text': review.get('review_text', '').strip()
            }

            parsed_data.append(review_data)

        # Return the parsed data as JSON
        return jsonify(parsed_data)

    except Exception as e:
        # Handle API request errors here
        error_message = str(e)
        return jsonify({'error': error_message}), 500  # Return a 500 Internal Server Error status

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify, render_template
from outscraper import ApiClient
from bs4 import BeautifulSoup

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
    limit = request.form.get('limit')

    try:
        # Initialize the Outscraper API client
        api_client = ApiClient(api_key=API_KEY)

        # Use the library to fetch Google Maps reviews
        results = api_client.google_maps_reviews(place_id, reviews_limit=int(limit))

        # Parse the HTML response using Beautiful Soup
        soup = BeautifulSoup(results['html'], 'html.parser')

        # Find all review elements on the page
        review_elements = soup.find_all('div', class_='review')

        # Extract data from review elements and store it in a list
        parsed_data = []
        for review_element in review_elements:
            review_author = review_element.find('div', class_='review-author').text.strip()
            review_rating = int(review_element.find('div', class_='review-rating').text.strip())
            review_text = review_element.find('div', class_='review-text').text.strip()

            # Create a dictionary for each review
            review_data = {
                'review_author': review_author,
                'review_rating': review_rating,
                'review_text': review_text
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
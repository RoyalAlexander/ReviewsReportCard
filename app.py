from flask import Flask, request, jsonify, render_template
from outscraper import ApiClient
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
    filter_type = request.form.get('filter_type')
    filter = request.form.get('filter')
    

    try:
        # Initialize the Outscraper API client
        api_client = ApiClient(api_key=API_KEY)

        filter_terms = [term.strip() for term in filter.split(",")]

        all_filtered_terms = []

        if filter_type == "and":
            results = api_client.google_maps_reviews(place_id, reviews_limit=int(limit), reviews_query=filter)
            review_data = results[0]['reviews_data']
            filtered_reviews = [review for review in review_data if all(term.lower() in review['review_text'].lower() for term in filter_terms)]
            all_filtered_terms.extend(filtered_reviews)

        elif filter_type == "or":
            all_filtered_terms = []  # Initialize the list to store all filtered reviews
            limit_remaining = int(limit)  # Initialize the remaining limit

            for term in filter_terms:
                if limit_remaining <= 0:
                    break  # If the limit is reached, exit the loop

                results = api_client.google_maps_reviews(place_id, reviews_limit=limit_remaining, reviews_query=term)
                review_data = results[0]['reviews_data']

                # Filter reviews for the current term
                filtered_reviews = [review for review in review_data if term.lower() in review['review_text'].lower()]

                # Calculate how many reviews can be added from this term
                reviews_to_add = min(len(filtered_reviews), limit_remaining)

                # Add the reviews to the accumulation list
                all_filtered_terms.extend(filtered_reviews[:reviews_to_add])

                # Update the remaining limit
                limit_remaining -= reviews_to_add

        venue_name = results[0]['name']
        reviews_rating = results[0]['rating']
        

        total_rating = sum([review['review_rating'] for review in review_data])
        avg_rating = total_rating / len(review_data) if review_data else 0

        # Return the parsed data as JSON
        return jsonify({"rating": reviews_rating, "avg_rating": avg_rating, "name": venue_name, "reviews": all_filtered_terms})


    
    except Exception as e:
     error_message = str(e)
     return jsonify({'error': error_message}), 500  # Return a 500 Internal Server Error status


if __name__ == '__main__':
    app.run(debug=True)
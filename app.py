# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS # For handling Cross-Origin Resource Sharing
from quotes_manager import QuoteManager
import random

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (important for frontend apps)

# Initialize the QuoteManager to interact with quotes.json
# Make sure quotes.json is in the same directory as app.py
quote_manager = QuoteManager('quotes.json')

# --- API Endpoints ---

@app.route('/api/quotes', methods=['GET'])
def get_all_quotes():
    """
    GET /api/quotes
    Retrieves all quotes.
    """
    quotes = quote_manager.get_all_quotes()
    return jsonify(quotes)

@app.route('/api/quotes/<int:quote_id>', methods=['GET'])
def get_quote_by_id(quote_id):
    """
    GET /api/quotes/<int:quote_id>
    Retrieves a single quote by its ID.
    """
    quote = quote_manager.get_quote_by_id(quote_id)
    if quote:
        return jsonify(quote)
    return jsonify({"error": "Quote not found"}), 404

@app.route('/api/quotes/random', methods=['GET'])
def get_random_quote():
    """
    GET /api/quotes/random
    Retrieves a random quote.
    """
    quotes = quote_manager.get_all_quotes()
    if quotes:
        random_quote = random.choice(quotes)
        return jsonify(random_quote)
    return jsonify({"error": "No quotes available"}), 404

@app.route('/api/quotes', methods=['POST'])
def add_new_quote():
    """
    POST /api/quotes
    Adds a new quote.
    Requires 'author' and 'quote' in the request body.
    Example: {"author": "New Author", "quote": "This is a new quote."}
    """
    data = request.get_json()
    if not data or 'author' not in data or 'quote' not in data:
        return jsonify({"error": "Missing 'author' or 'quote' in request body"}), 400

    author = data['author']
    quote_text = data['quote']

    new_quote = quote_manager.add_quote(author, quote_text)
    if new_quote:
        return jsonify(new_quote), 201 # 201 Created
    return jsonify({"error": "Could not add quote"}), 500 # Internal server error

@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_existing_quote(quote_id):
    """
    PUT /api/quotes/<int:quote_id>
    Updates an existing quote by ID.
    Can update 'author' or 'quote' (or both).
    Example: {"author": "Updated Author"} or {"quote": "Updated quote text."}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided for update"}), 400

    new_author = data.get('author')
    new_quote_text = data.get('quote')

    if not new_author and not new_quote_text:
        return jsonify({"error": "No 'author' or 'quote' field provided for update"}), 400

    updated_quote = quote_manager.update_quote(quote_id, new_author, new_quote_text)
    if updated_quote:
        return jsonify(updated_quote)
    return jsonify({"error": "Quote not found"}), 404

@app.route('/api/quotes/<int:quote_id>', methods=['DELETE'])
def delete_existing_quote(quote_id):
    """
    DELETE /api/quotes/<int:quote_id>
    Deletes a quote by its ID.
    """
    if quote_manager.delete_quote(quote_id):
        return jsonify({"message": "Quote deleted successfully"}), 200
    return jsonify({"error": "Quote not found"}), 404

# --- Basic Health Check / Root ---
@app.route('/')
def home():
    return "Welcome to the Quote API! Visit /api/quotes for data."

# --- Run the Flask app ---
if __name__ == '__main__':
    app.run(debug=True) # debug=True enables auto-reloading and helpful error messages

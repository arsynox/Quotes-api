# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from quotes_manager import QuoteManager
import random

app = Flask(__name__)
CORS(app)

# Initialize the QuoteManager to interact with quotes.json
quote_manager = QuoteManager('quotes.json')

# --- Data for Quote Generation ---
authors_for_generation = [
    "Albert Einstein", "Marie Curie", "Leonardo da Vinci", "Maya Angelou", "Stephen King",
    "Steve Jobs", "Eleanor Roosevelt", "Winston Churchill", "Nelson Mandela", "Walt Disney",
    "Confucius", "Oprah Winfrey", "Theodore Roosevelt", "Mahatma Gandhi", "Ralph Waldo Emerson",
    "Abraham Lincoln", "J.K. Rowling", "Buddha", "Coco Chanel", "Benjamin Franklin",
    "Aristotle", "Martin Luther King Jr.", "Helen Keller", "Zig Ziglar", "Vince Lombardi",
    "Wayne Gretzky", "Friedrich Nietzsche", "Bruce Lee", "George Bernard Shaw", "Anne Frank",
    "Dalai Lama", "Jim Rohn", "Napoleon Hill", "Paulo Coelho", "Mother Teresa",
    "Sun Tzu", "Socrates", "Voltaire", "Plato", "Rumi", "Harriet Tubman",
    "Malala Yousafzai", "Bill Gates", "Colin Powell", "Lao Tzu", "J.R.R. Tolkien",
    "Audrey Hepburn", "Pablo Picasso", "Thomas Edison", "Victor Hugo", "Seneca",
    "Marilyn Monroe", "Stephen Covey", "Amelia Earhart", "Robert Frost", "Franklin D. Roosevelt",
    "Virginia Woolf", "Haruki Murakami", "C.S. Lewis", "Henry Ford", "Wayne Dyer",
    "Leo Tolstoy", "George Eliot", "Walt Whitman", "Rene Descartes", "Anaïs Nin",
    "Muhammad Ali", "Pablo Neruda", "Jane Austen", "Malcom X", "H. Jackson Brown Jr.",
    "Dr. Seuss", "Henry David Thoreau", "Booker T. Washington", "Benjamin Disraeli",
    "Albert Camus", "Mark Twain", "Oscar Wilde", "Charles Darwin", "Isaac Newton",
    "Galileo Galilei", "Alan Turing", "Grace Hopper", "Ada Lovelace", "Nikola Tesla",
    "Carl Sagan", "Neil deGrasse Tyson", "Richard Feynman", "Noam Chomsky", "Angela Davis"
]

themes_for_generation = [
    "imagination", "innovation", "empathy", "authenticity", "perseverance", "dreams",
    "courage", "education", "inspiration", "patience", "happiness", "belief",
    "change", "wisdom", "creation", "growth", "resilience", "understanding",
    "curiosity", "learning", "action", "mindset", "purpose", "love", "strategy",
    "knowledge", "truth", "light", "journey", "success", "failure", "choices",
    "focus", "discipline", "goals", "opportunity", "creativity", "freedom",
    "optimism", "present moment", "future", "past", "work", "beauty", "strength",
    "art", "discovery", "fear", "blossom", "kindness", "potential", "exploration",
    "simplicity", "complexity", "reality", "vision", "passion", "progress", "peace"
]

quote_templates_for_generation = [
    "Focus on your {theme1} and let your {theme2} guide you.",
    "The secret to {theme1} is continuous {theme2}.",
    "Embrace {theme1} as the pathway to {theme2}.",
    "Discover {theme1} within yourself to achieve {theme2}.",
    "True {theme1} comes from sustained {theme2}.",
    "Without {theme1}, there can be no true {theme2}.",
    "The essence of {theme1} lies in its {theme2}.",
    "Cultivate {theme1} to find your inner {theme2}."
]

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
    Adds a new quote provided in the request body.
    Requires 'author' and 'quote' in the request body.
    """
    data = request.get_json()
    if not data or 'author' not in data or 'quote' not in data:
        return jsonify({"error": "Missing 'author' or 'quote' in request body"}), 400

    author = data['author']
    quote_text = data['quote']

    new_quote = quote_manager.add_quote(author, quote_text)
    if new_quote:
        return jsonify(new_quote), 201
    return jsonify({"error": "Could not add quote"}), 500

@app.route('/api/quotes/generate', methods=['POST'])
def generate_and_add_quote():
    """
    POST /api/quotes/generate
    Generates a new random quote and adds it to the collection.
    No request body needed.
    """
    author = random.choice(authors_for_generation)
    theme1 = random.choice(themes_for_generation)
    theme2 = random.choice(themes_for_generation)
    
    while theme1 == theme2 and len(themes_for_generation) > 1:
        theme2 = random.choice(themes_for_generation)
        
    quote_text = random.choice(quote_templates_for_generation).format(theme1=theme1, theme2=theme2)

    new_quote = quote_manager.add_quote(author, quote_text)

    if new_quote:
        return jsonify(new_quote), 201
    return jsonify({"error": "Failed to generate and add quote"}), 500


@app.route('/api/quotes/<int:quote_id>', methods=['PUT'])
def update_existing_quote(quote_id):
    """
    PUT /api/quotes/<int:quote_id>
    Updates an existing quote by ID.
    Can update 'author' or 'quote' (or both).
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

@app.route('/')
def home():
    return "Welcome to the Quote API! Visit /api/quotes for data or /api/quotes/generate to add a new random one."

# --- No app.run() here when deploying with Gunicorn ---
# The __name__ == '__main__' block should only be for local development
# if __name__ == '__main__':
#     app.run(debug=True)

# quotes_manager.py
import json
import os

class QuoteManager:
    """
    A class to manage quotes stored in a JSON file.
    It allows loading, adding, retrieving, updating, and deleting quotes.
    """
    def __init__(self, file_path='quotes.json'):
        self.file_path = file_path
        self.quotes = self._load_quotes()

    def _load_quotes(self):
        """Loads quotes from the JSON file."""
        if not os.path.exists(self.file_path):
            # If the file doesn't exist, create it with an empty array
            with open(self.file_path, 'w') as f:
                json.dump([], f, indent=4)
            return []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    print(f"Warning: {self.file_path} content is not a list. Initializing with an empty list.")
                    return []
                return data
        except json.JSONDecodeError:
            print(f"Warning: {self.file_path} is empty or contains invalid JSON. Starting with an empty list.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while loading quotes: {e}")
            return []

    def _save_quotes(self):
        """Saves the current list of quotes back to the JSON file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.quotes, f, indent=4, ensure_ascii=False) # indent for pretty-printing
        except Exception as e:
            print(f"Error saving quotes to {self.file_path}: {e}")

    def add_quote(self, author: str, quote_text: str):
        """
        Adds a new quote to the collection.
        Assigns the next available ID.
        """
        if not author or not quote_text:
            return None # Indicate failure due to missing data

        # Determine the next ID
        next_id = 1
        if self.quotes:
            # Safely find max_id, handling potential non-dict items or missing 'id'
            max_id = 0
            for q in self.quotes:
                if isinstance(q, dict) and 'id' in q and isinstance(q['id'], int):
                    max_id = max(max_id, q['id'])
            next_id = max_id + 1

        new_quote = {
            "id": next_id,
            "author": author,
            "quote": quote_text
        }
        self.quotes.append(new_quote)
        self._save_quotes()
        return new_quote

    def get_all_quotes(self) -> list:
        """Returns a list of all quotes."""
        return self.quotes

    def get_quote_by_id(self, quote_id: int) -> dict | None:
        """Returns a specific quote by its ID."""
        for quote in self.quotes:
            if isinstance(quote, dict) and quote.get('id') == quote_id:
                return quote
        return None

    def update_quote(self, quote_id: int, new_author: str = None, new_quote_text: str = None) -> dict | None:
        """
        Updates an existing quote by ID.
        Only fields provided (not None) will be updated.
        """
        for quote in self.quotes:
            if isinstance(quote, dict) and quote.get('id') == quote_id:
                if new_author is not None:
                    quote['author'] = new_author
                if new_quote_text is not None:
                    quote['quote'] = new_quote_text
                self._save_quotes()
                return quote
        return None

    def delete_quote(self, quote_id: int) -> bool:
        """Deletes a quote by its ID."""
        initial_len = len(self.quotes)
        self.quotes = [q for q in self.quotes if not (isinstance(q, dict) and q.get('id') == quote_id)]
        if len(self.quotes) < initial_len:
            self._save_quotes()
            return True
        return False

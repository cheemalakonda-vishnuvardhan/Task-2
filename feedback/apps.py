from flask import Flask, render_template, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# The name of the file where feedback will be stored
FEEDBACK_FILE = 'feedback.json'

@app.route('/')
def home():
    """Renders the main feedback form page."""
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    """Handles the form submission and saves data to a JSON file."""
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        email = request.form.get('email')
        rating = request.form.get('rating')
        comments = request.form.get('comments')

        # Create a dictionary for the new feedback entry
        new_feedback = {
            'name': name,
            'email': email,
            'rating': int(rating),
            'comments': comments,
            'timestamp': datetime.now().isoformat()
        }

        # Load existing feedback or create a new list
        feedback_list = []
        if os.path.exists(FEEDBACK_FILE) and os.path.getsize(FEEDBACK_FILE) > 0:
            try:
                with open(FEEDBACK_FILE, 'r') as f:
                    feedback_list = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                feedback_list = []

        # Add the new feedback to the list
        feedback_list.append(new_feedback)

        # Save the updated list to the JSON file
        try:
            with open(FEEDBACK_FILE, 'w') as f:
                json.dump(feedback_list, f, indent=4)
            return 'Feedback submitted successfully!'
        except Exception as e:
            return f'An error occurred: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
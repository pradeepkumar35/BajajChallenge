from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


def extract_alphabets_and_numbers(data):
    alphabets = [char for char in data if isinstance(char, str) and char.isalpha()]
    numbers = [int(num) for num in data if isinstance(num, (int, str)) and str(num).isdigit()]
    highest_lowercase_alphabet = max([char for char in alphabets if char.islower()], default = None)
    return alphabets, numbers, highest_lowercase_alphabet


@app.route('/bfhl', methods=['POST'])
def bfhl():
    try:
        # Parse the incoming JSON request
        request_data = request.get_json()
        if 'data' not in request_data:
            return jsonify({'error': 'Invalid JSON structure. "data" field is required.'}), 400

        data = request_data['data']

        if not isinstance(data, list):
            return jsonify({'error': '"data" should be a list.'}), 400

        # Process the data
        alphabets, numbers, highest_lowercase_alphabet = extract_alphabets_and_numbers(data)

        # Prepare the response
        response = {
            'alphabets': alphabets,
            'numbers': numbers,
            'highest_lowercase_alphabet': highest_lowercase_alphabet
        }

        return jsonify(response)

    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format.'}), 400

    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Mock user data
user_data = {
    'name': 'Juan',
    'languageLevel': 'Intermediate'
}

# Mock initial message
initial_message = {
    'response': 'Welcome to the chat!'
}

@app.route('/userData', methods=['GET'])
def get_user_data():
    return jsonify(user_data)

@app.route('/initialMessage', methods=['GET'])
def get_initial_message():
    return jsonify(initial_message)

@app.route('/juancito', methods=['POST'])
def juancito_response():
    user_message = request.json.get('message')
    # Here you can implement your logic to generate a response
    juancito_reply = f"Juancito says: {user_message}"
    return jsonify({'response': juancito_reply})

if __name__ == '__main__':
    app.run(debug=True)

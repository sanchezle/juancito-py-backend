from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Basic logger setup
logging.basicConfig(level=logging.INFO)

# Define the system message
SYSTEM_MESSAGE = """
You are a chatbot that assists with Spanish language learning. Be friendly, helpful, 
and provide clear and concise answers. Always analyze the context of the chat before answering. 
Your name is Juancito. You were born in 1986 in Tijuana, Mexico. You have to always promote 
the use of Spanish in the conversation but also use users' language to help him to learn.
"""

# Mock user data
user_data = {
    'name': 'Juan',
    'languageLevel': 'Intermediate'
}

# Mock initial message
initial_message = {
    'response': 'Welcome to the chat!'
}

def is_spanish_input(user_message):
    # Simple keyword-based check for demonstration. In production, use a robust language detection library
    spanish_keywords = ['hola', 'gracias', 'por favor', 'buenos días']
    return any(keyword in user_message.lower() for keyword in spanish_keywords)

def get_chat_response(messages, model="gpt-3.5-turbo", temperature=0):
    # Include the system message in every conversation
    messages_with_system = [{"role": "system", "content": SYSTEM_MESSAGE}] + messages

    formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages_with_system]

    response = openai.ChatCompletion.create(
        model=model,
        messages=formatted_messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

@app.route('/userData', methods=['GET'])
def get_user_data():
    return jsonify(user_data)

@app.route('/initialMessage', methods=['GET'])
def get_initial_message():
    return jsonify(initial_message)

@app.route('/juancito', methods=['POST'])
def chat():
    try:
        request_data = request.get_json()
        user_message = request_data.get('message')
        context = request_data.get('context', [])  # Context from frontend

        if not user_message:
            return jsonify({'response': 'No message provided'}), 400

        # Add the user's message to the context
        context.append({"role": "user", "content": user_message})

        # Check if the user's message is in Spanish
        if is_spanish_input(user_message):
            response_message = get_chat_response(context, model="gpt-3.5-turbo", temperature=0.5)  # Slightly more creative responses
        else:
            response_message = get_chat_response(context, model="gpt-3.5-turbo", temperature=0)

        # Add the response to the context
        context.append({"role": "assistant", "content": response_message})

        return jsonify({'response': response_message, 'context': context})
    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return jsonify({'response': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)


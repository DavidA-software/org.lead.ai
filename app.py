from flask import Flask, request, jsonify
from flask_cors import CORS
from chatBot import SchedulingChatbot
import traceback

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
bot = SchedulingChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({'error': 'No text provided'}), 400
        
        print(f"[Flask] Received input: {user_input}")
        
        response = bot.process_input(user_input)
        
        print(f"[Flask] Sending response: {response}")
        
        return jsonify({'response': response}), 200
    
    except Exception as e:
        print(f"[Flask] Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Chatbot is running'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'OrgLead AI Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            '/chat': 'POST - Send chat messages',
            '/health': 'GET - Check API health'
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("Starting OrgLead AI Scheduling Chatbot API")
    print("=" * 60)
    print("API running on: http://localhost:8000")
    print("Endpoints:")
    print("  - POST http://localhost:8000/chat")
    print("  - GET  http://localhost:8000/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000, debug=True)

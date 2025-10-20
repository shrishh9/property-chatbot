from flask import Flask, request, jsonify
from flask_cors import CORS
from query_parser import QueryParser
from property_search import PropertySearch
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Initialize components
parser = QueryParser()
search_engine = PropertySearch('data/merged_properties.csv')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Property Chatbot API is running'})

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    
    Request body:
        {
            "message": "3BHK flat in Pune under ₹1.2 Cr"
        }
    
    Response:
        {
            "summary": "Generated summary",
            "properties": [...],
            "filters": {...},
            "count": 5
        }
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Handle greetings and casual messages
        greetings = ['hi', 'hello', 'hey', 'hii', 'hlo', 'sup', 'yo', 'namaste']
        help_words = ['help', 'how to use', 'what can you do', 'commands']
        
        user_message_lower = user_message.lower()
        
        # Check if it's a greeting
        if user_message_lower in greetings:
            return jsonify({
                'summary': "Hello! 👋 I'm your property search assistant. I can help you find properties based on your requirements. Try asking me things like:\n\n• '3BHK flat in Pune under ₹1.2 Cr'\n• 'Ready to move 2BHK in Mumbai'\n• 'Office space under 50 lakhs'\n\nWhat would you like to search for?",
                'properties': [],
                'filters': {},
                'count': 0,
                'query': user_message
            })
        
        # Check if asking for help
        if any(word in user_message_lower for word in help_words):
            return jsonify({
                'summary': "I can help you find properties! 🏠 You can search by:\n\n• BHK type (1BHK, 2BHK, 3BHK, etc.)\n• Budget (under ₹1.2 Cr, under 50 lakhs)\n• City (Pune, Mumbai, etc.)\n• Status (ready to move, under construction)\n• Property type (office, villa, residential)\n\nJust describe what you're looking for in natural language!",
                'properties': [],
                'filters': {},
                'count': 0,
                'query': user_message
            })
        
        # Parse query
        filters = parser.parse_query(user_message)
        
        # If no meaningful filters were extracted
        if not filters or len(filters) == 0:
            return jsonify({
                'summary': "I couldn't understand your query. 🤔 Please try to include details like:\n\n• Number of BHK (e.g., 2BHK, 3BHK)\n• Budget (e.g., under ₹1.2 Cr)\n• City (e.g., Pune, Mumbai)\n• Status (e.g., ready to move)\n\nFor example: '3BHK flat in Pune under ₹1.2 Cr'",
                'properties': [],
                'filters': {},
                'count': 0,
                'query': user_message
            })
        
        # Search properties
        results = search_engine.search(filters)
        
        # Generate summary
        summary = search_engine.generate_summary(results, filters)
        
        # Prepare response
        response = {
            'summary': summary,
            'properties': results[:10],  # Limit to 10 results
            'filters': filters,
            'count': len(results),
            'query': user_message
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return jsonify({'error': str(e)}), 500

@app.route('/api/properties', methods=['GET'])
def get_all_properties():
    """Get all properties (for testing)"""
    try:
        results = search_engine.search({})
        return jsonify({
            'properties': results[:20],  # Limit to 20 for testing
            'count': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    print("\n🚀 Starting Property Chatbot API...")
    print("📍 API will be available at: http://localhost:5000")
    print("✅ Health check: http://localhost:5000/api/health")
    print("💬 Chat endpoint: http://localhost:5000/api/chat\n")
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)


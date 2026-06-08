import os
import json
from flask import Flask, render_template, request, jsonify, session
import requests
from dotenv import load_dotenv

# Load environment variables and initialize Flask app
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_secret')

# Travel knowledge base loaded from external JSON
DESTINATIONS_DB = {}
dest_file = os.path.join(os.path.dirname(__file__), "data", "all_india_destinations.json")
try:
    with open(dest_file, "r", encoding="utf-8") as f:
        DESTINATIONS_DB = json.load(f)
except Exception as e:
    DESTINATIONS_DB = {}
    print("Warning: failed to load all_india_destinations.json:", e)
    
# Maharashtra-specific data
MAHARASHTRA_DB = {}
maha_file = os.path.join(os.path.dirname(__file__), "data", "maharashtra_destinations.json")
try:
    with open(maha_file, "r", encoding="utf-8") as f:
        MAHARASHTRA_DB = json.load(f)
except Exception as e:
    MAHARASHTRA_DB = {}
    print("Warning: failed to load maharashtra_destinations.json:", e)
 

# System prompt for the chatbot
CHATBOT_SYSTEM_PROMPT = """You are a friendly and knowledgeable travel chatbot assistant specializing in Indian destinations. Your role is to:
1. Help travelers discover amazing places across India
2. Provide detailed travel advice and recommendations for Indian destinations
3. Answer questions about Indian attractions, activities, and best seasons to visit
4. Help plan Indian itineraries and provide budget estimates
5. Suggest Indian destinations based on interests (adventure, relaxation, culture, food, etc.)

Be conversational, helpful, and enthusiastic about exploring India. Use the available destination information to make recommendations.

Available Indian destinations: Goa, Manali, Kashmir, Agra, Jaipur, Delhi, Kerala, Udaipur, Varanasi, Shimla, 
Darjeeling, Ooty, Mysore, Andaman, Pondicherry, Pushkar, Mumbai, Kolkata, Nainital, Rishikesh, Jaisalmer, 
Jodhpur, Ladakh, Dharamshala, Coorg, Meghalaya, Guwahati, Auli, and Alleppey.

Always encourage travelers to explore the diverse beauty of India!"""


@app.route('/')
def index():
    return render_template('chatbot.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chatbot endpoint that processes user messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Initialize chat history in session
        if 'chat_history' not in session:
            session['chat_history'] = []

        # Add user message to history
        session['chat_history'].append({
            'role': 'user',
            'content': user_message
        })

        # Generate bot response
        bot_response = generate_travel_response(user_message, session['chat_history'])

        # Add bot response to history
        session['chat_history'].append({
            'role': 'assistant',
            'content': bot_response
        })
        session.modified = True

        return jsonify({
            'response': bot_response,
            'status': 'success'
        })

    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500


@app.route('/api/chat-history', methods=['GET'])
def get_chat_history():
    """Retrieve chat history for the current session"""
    history = session.get('chat_history', [])
    return jsonify({'history': history})


@app.route('/api/clear-chat', methods=['POST'])
def clear_chat():
    """Clear chat history"""
    session['chat_history'] = []
    session.modified = True
    return jsonify({'status': 'success', 'message': 'Chat cleared'})


@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Get list of all available destinations"""
    destinations = []
    for name, details in DESTINATIONS_DB.items():
        destinations.append({
            'name': name.title(),
            'price': details['price'],
            'duration': details['duration'],
            'image': details['image']
        })
    return jsonify({'destinations': destinations})


@app.route('/api/maharashtra', methods=['GET'])
def get_maharashtra():
    """Get list of Maharashtra-specific destinations"""
    destinations = []
    for name, details in MAHARASHTRA_DB.items():
        destinations.append({
            'name': name.title(),
            'price': details.get('price', 'N/A'),
            'duration': details.get('duration', 'N/A'),
            'image': details.get('image', '')
        })
    return jsonify({'destinations': destinations})


@app.route('/api/destinations/category/<category>', methods=['GET'])
def get_destinations_by_category(category):
    """Get destinations filtered by category (e.g., Beach, Adventure, Mountain, Culture)"""
    destinations = []
    category_lower = category.lower()
    for name, details in DESTINATIONS_DB.items():
        dest_categories = [c.lower() for c in details.get('category', [])]
        if category_lower in dest_categories:
            destinations.append({
                'name': name.title(),
                'price': details.get('price', 'N/A'),
                'duration': details.get('duration', 'N/A'),
                'image': details.get('image', ''),
                'category': details.get('category', [])
            })
    return jsonify({'category': category, 'destinations': destinations, 'count': len(destinations)})


@app.route('/api/destinations/region/<region>', methods=['GET'])
def get_destinations_by_region(region):
    """Get destinations filtered by region"""
    destinations = []
    region_lower = region.lower()
    for name, details in DESTINATIONS_DB.items():
        if region_lower in details.get('region', '').lower():
            destinations.append({
                'name': name.title(),
                'price': details.get('price', 'N/A'),
                'duration': details.get('duration', 'N/A'),
                'image': details.get('image', ''),
                'region': details.get('region', '')
            })
    return jsonify({'region': region, 'destinations': destinations, 'count': len(destinations)})


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get list of all available destination categories"""
    categories = set()
    for dest_info in DESTINATIONS_DB.values():
        for cat in dest_info.get('category', []):
            categories.add(cat)
    return jsonify({'categories': sorted(list(categories))})


@app.route('/api/regions', methods=['GET'])
def get_regions():
    """Get list of all available regions"""
    regions = set()
    for dest_info in DESTINATIONS_DB.values():
        region = dest_info.get('region', '')
        if region:
            regions.add(region)
    return jsonify({'regions': sorted(list(regions))})


def generate_travel_response(user_message: str, chat_history: list) -> str:
    """Generate a travel-focused response based on user input"""
    message_lower = user_message.lower()
    
    # Check for destination mentions
    for dest_key, dest_info in DESTINATIONS_DB.items():
        if dest_key in message_lower:
            return format_destination_response(dest_key, dest_info)
    
    # Respond to common travel queries
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return ("👋 Hello! Welcome to your personal travel assistant! I'm here to help you plan your next adventure. "
                "I can help you find the perfect destination, suggest activities, and provide travel tips. "
                "What kind of trip are you dreaming of? 🌍✈️")
    
    if any(word in message_lower for word in ['recommend', 'suggest', 'best', 'where should', 'destination']):
        if any(word in message_lower for word in ['adventure', 'trekking', 'hiking', 'mountain']):
            return "🏔️ For adventure lovers, I'd highly recommend **Manali**! It offers snow adventures, river rafting, camping, and paragliding. The best time to visit is October to June. Would you like more details about Manali or other adventure destinations?"
        elif any(word in message_lower for word in ['relax', 'beach', 'peace', 'calm', 'quiet']):
            return "🏖️ For relaxation, **Goa** is perfect with its beautiful beaches and water sports. Or if you prefer peaceful mountain vibes, **Manali** is excellent. What appeals to you more - beach or mountains?"
        elif any(word in message_lower for word in ['luxury', 'shopping', 'modern', 'upscale']):
            return "💎 For a luxury experience, **Dubai** is your ideal choice! It offers luxury shopping, the Burj Khalifa, and stunning desert safaris. The best season is November to March. Ready to explore?"
        elif any(word in message_lower for word in ['culture', 'romantic', 'art', 'museum']):
            return "🎨 For culture and romance, I'd suggest **Paris** - the City of Love! It has iconic landmarks, world-class museums, and charming cafes. Best visited April to June. Would you like an itinerary?"
        else:
            return "🌎 I can recommend several amazing destinations: **Goa** (beach paradise), **Manali** (mountain adventure), **Dubai** (luxury), **Paris** (romance & culture), or **Amsterdam** (canals & cycling). What type of experience interests you?"
    
    if any(word in message_lower for word in ['budget', 'price', 'cost', 'expense', 'affordable', 'expensive']):
        return ("💰 Here's a quick budget overview:\n"
                "• **Goa**: ₹12,999 (Budget-friendly)\n"
                "• **Manali**: ₹18,499 (Affordable adventure)\n"
                "• **Amsterdam**: ₹45,000 (Mid-range)\n"
                "• **Dubai**: ₹65,000 (Luxury)\n"
                "• **Paris**: ₹1,10,000 (Premium experience)\n\n"
                "What's your budget range? I can help find the perfect match!")
    
    if any(word in message_lower for word in ['thank', 'thanks', 'grateful', 'appreciate']):
        return "You're welcome! 😊 I'm always here to help with your travel plans. Anything else you'd like to know?"
    
    if any(word in message_lower for word in ['what can you do', 'help', 'how can', 'features', 'capabilities']):
        return ("Here's what I can help you with:\n"
                "✈️ **Find Destinations** - Recommend places based on your interests\n"
                "🎯 **Trip Planning** - Help create itineraries\n"
                "💰 **Budget Guidance** - Estimate costs for different destinations\n"
                "🏨 **Hotel Suggestions** - Recommend accommodations\n"
                "🎨 **Activity Ideas** - Suggest things to do and see\n"
                "📅 **Best Time to Visit** - Tell you when to go\n\n"
                "Just ask me anything travel-related! 🌍")
    
    # Default friendly response
    return ("That's interesting! 🌟 I'd love to help you with travel planning. "
            "You could ask me about:\n"
            "• Destination recommendations\n"
            "• Budget and pricing\n"
            "• Activities and attractions\n"
            "• Best time to visit\n"
            "• Trip planning tips\n\n"
            "What would you like to explore? 🌍✈️")


def format_destination_response(dest_key: str, dest_info: dict) -> str:
    """Format detailed destination information"""
    return (f"🏖️ **{dest_key.title()}** - Your Next Adventure Awaits!\n\n"
            f"📝 **Description:** {dest_info['description']}\n\n"
            f"💰 **Price:** {dest_info['price']}\n"
            f"⏱️ **Duration:** {dest_info['duration']}\n"
            f"🏨 **Hotel:** {dest_info['hotel']}\n"
            f"📅 **Best Time:** {dest_info['best_time']}\n\n"
            f"🎯 **Activities:**\n" + 
            "\n".join([f"  • {activity}" for activity in dest_info['activities']]) +
            f"\n\nWould you like more information or help booking? 🎫")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG', '1') == '1')
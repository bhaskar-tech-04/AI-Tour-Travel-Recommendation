import os
import random
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

# Create Flask app. templates and static live in ../templates
app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"), static_folder=os.path.join(os.path.dirname(__file__), "..", "templates", "static"))

# Simple travel packages database
travel_packages = {
    "goa": {
        "days": "4 Days / 3 Nights",
        "price": "₹12,999",
        "hotel": "Sea View Resort",
        "activities": ["Beach Party", "Water Sports", "Cruise Ride", "Nightlife"],
        "best_time": "November to February"
    },
    "manali": {
        "days": "5 Days / 4 Nights",
        "price": "₹18,499",
        "hotel": "Mountain Paradise Hotel",
        "activities": ["Snow Adventure", "River Rafting", "Camping", "Paragliding"],
        "best_time": "October to June"
    },
    "dubai": {
        "days": "6 Days / 5 Nights",
        "price": "₹65,000",
        "hotel": "Burj Luxury Hotel",
        "activities": ["Desert Safari", "Burj Khalifa Visit", "Luxury Shopping", "Yacht Ride"],
        "best_time": "November to March"
    },
    "paris": {
        "days": "7 Days / 6 Nights",
        "price": "₹1,10,000",
        "hotel": "Eiffel Grand Hotel",
        "activities": ["Eiffel Tower", "River Cruise", "Museum Visit", "Cafe Tour"],
        "best_time": "April to June"
    }
}

# Environment config
UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/search')
def api_search():
    """API: /api/search?destination=goa  -> JSON with image and package"""
    destination = request.args.get('destination', '').strip().lower()
    if not destination:
        return jsonify({'error': 'missing destination parameter'}), 400

    # Get image (fallback to placeholder)
    image = get_destination_image(destination)

    # Get package or generate a suggested package
    package = travel_packages.get(destination)
    if not package:
        package = {
            "days": f"{random.randint(3,7)} Days / {random.randint(2,6)} Nights",
            "price": f"₹{random.randint(15000,90000):,}",
            "hotel": "Premium Stay",
            "activities": ["Sightseeing", "Local Food Tour", "Adventure Activities"],
            "best_time": "All Seasons"
        }

    return jsonify({
        'destination': destination.title(),
        'image': image,
        'package': package
    })


def get_destination_image(destination: str) -> str:
    """Try Unsplash first (if key provided) otherwise return a placeholder Unsplash image search URL."""
    placeholder = f"https://images.unsplash.com/photo-1507525428034-b723cf961d3e"

    if not UNSPLASH_ACCESS_KEY:
        return placeholder

    try:
        url = f"https://api.unsplash.com/search/photos?page=1&query={requests.utils.quote(destination)}&per_page=1&client_id={UNSPLASH_ACCESS_KEY}"
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data['results'][0]['urls']['regular'] if data.get('results') else placeholder
    except Exception:
        return placeholder


if __name__ == '__main__':
    # For local dev: set FLASK_ENV=development or run with flask run
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('FLASK_DEBUG', '1') == '1')
# ✈️ AI Travel Chatbot - Your Personal Travel Assistant

## 🌍 About the Project

The **AI Travel Chatbot** is an intelligent conversational assistant designed to help travelers plan their perfect trip. It's a modern, user-friendly web application built with Flask that engages users in natural conversations to understand their travel preferences and provide personalized recommendations.

## 🎯 What Makes It Special

- **Conversational AI**: Chat naturally about travel - no forms to fill out
- **Smart Recommendations**: Get destination suggestions based on your interests
- **Comprehensive Travel Info**: Budget, activities, best seasons, hotel recommendations
- **Session Management**: Your chat history is saved during your session
- **Beautiful UI**: Modern gradient design with smooth animations

## 🚀 Features

✅ **Intelligent Chatbot** - Natural conversation with travel expertise

✅ **Destination Recommendations** - Smart suggestions based on preferences (adventure, relaxation, culture, luxury)

✅ **Travel Information** - Detailed info on 5+ destinations (Goa, Manali, Dubai, Paris, Amsterdam)

✅ **Budget Guidance** - Clear pricing for different travel packages

✅ **Activity Suggestions** - Personalized activity recommendations

✅ **Best Time to Visit** - Season information for each destination

✅ **Chat History** - Session-based conversation tracking

✅ **Responsive Design** - Works on desktop, tablet, and mobile devices

✅ **Modern UI** - Beautiful gradient design with smooth animations

✅ **Quick Suggestions** - One-click buttons for common queries

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Session Management**: Flask-Session
- **Styling**: Modern CSS with gradients and animations

## 📋 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Tour-Travel-Recommendation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (optional)
   ```
   FLASK_DEBUG=1
   PORT=5000
   SECRET_KEY=your-secret-key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```
   
   The app will be available at `http://localhost:5000/`

## 💬 How to Use

1. Open the chat interface in your browser
2. Click quick suggestion buttons or type your message
3. Ask the chatbot about:
   - Destination recommendations ("Recommend a beach destination")
   - Budget information ("What's your cheapest option?")
   - Specific destinations ("Tell me about Paris")
   - Travel tips ("What can you help with?")
4. Clear chat history anytime with the Clear button

## 🌍 Available Destinations

| Destination | Price | Duration | Best Time |
|------------|-------|----------|-----------|
| **Goa** 🏖️ | ₹12,999 | 4D/3N | Nov-Feb |
| **Manali** 🏔️ | ₹18,499 | 5D/4N | Oct-Jun |
| **Amsterdam** 🚴 | ₹45,000 | 4D/3N | Apr-Sep |
| **Dubai** 💎 | ₹65,000 | 6D/5N | Nov-Mar |
| **Paris** 🗼 | ₹1,10,000 | 7D/6N | Apr-Jun |

## 🎨 Sample Conversations

**User**: "I love adventure and mountains"
**Bot**: Recommends Manali with detailed information about trekking, rafting, and camping

**User**: "What's your most affordable option?"
**Bot**: Provides budget breakdown and recommends Goa as the best budget-friendly destination

**User**: "Tell me about Paris"
**Bot**: Displays comprehensive information including activities, best season, and pricing

---

**Created with ❤️ for travelers worldwide!**

# 🛠 Technologies Used

## 💻 Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

## ⚙ Backend

* Python
* Flask

## 🔗 API Used

* Unsplash API

---

# 📂 Project Structure

```bash id="9njc5x"
travel_project/
│
├── app.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
```

---

# ⚙ Installation & Setup

## 1️⃣ Clone Repository

```bash id="v4b4vz"
git clone https://github.com/yourusername/AI-Tour-Travel-Recommendation.git
```

---

## 2️⃣ Open Project Folder

```bash id="z8s0ow"
cd AI-Tour-Travel-Recommendation
```

---

## 3️⃣ Install Dependencies

```bash id="0pc45v"
pip install -r requirements.txt
```

---

## 4️⃣ Add Unsplash API Key

Get free API key from:

https://unsplash.com/developers

Replace inside `app.py`:

```python id="do73r3"
UNSPLASH_ACCESS_KEY = "37Dx3SKyg_qCBirlsBRXrhcxtXwiMaQ0FkSEmRISJyQ"
```

with your actual API key.

---

# ▶ Run Project

```bash id="ygz5ez"
& "C:\Users\ADMIN\Desktop\AI Tour & Travel Recommendation\.venv\Scripts\python.exe" "C:\Users\ADMIN\Desktop\AI Tour & Travel Recommendation\travel_project\app.py"```

Open browser:

```bash id="zry17n"
(http://10.58.157.49:5000/)```

---

# 🌍 Example Destinations

* Goa
* Manali
* Paris
* Dubai
* Switzerland

---

# 🎯 Problem Statement

Travelers often struggle to:

* Find travel information quickly
* Compare travel packages
* Discover hotels and activities
* Explore destinations visually

This project solves these problems by providing an all-in-one travel recommendation platform.

---

# 📚 Learning Outcomes

Through this project, I learned:

* Flask web development
* REST API integration
* Frontend and backend connectivity
* Dynamic content rendering
* Error handling
* GitHub deployment

---

# 🔮 Future Improvements

* AI Travel Chatbot
* Weather API Integration
* Google Maps Integration
* Hotel Booking System
* Flight Booking API
* User Authentication
* AI Itinerary Generator
* Voice Assistant

---

# 👨‍💻 Author

Bhaskar Harugade

---

# ⭐ Support

If you like this project, give it a ⭐ on GitHub.

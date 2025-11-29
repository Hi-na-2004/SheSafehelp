# 🛡️ SheSafe - Women Safety Application

A comprehensive women safety application with 4 core modules powered by AI/ML for protecting women and ensuring their safety online and offline.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### 1. 🛡️ Online Abuse Detection (Module 1)
- **Toxicity Detection**: Analyze text for harassment, threats, and abuse
- **Multi-category Analysis**: Detects toxicity, severe toxicity, obscene content, threats, insults, and identity attacks
- **Conversation Analysis**: Analyze entire conversations for patterns of abuse
- **Real-time Risk Assessment**: Instant risk level classification (LOW, MEDIUM, HIGH, CRITICAL)
- **Technology**: Uses Detoxify (MIT License) with transformer-based models

### 2. 💝 Mental Health & Emotion Detection (Module 2)
- **Emotion Analysis**: Detects sadness, fear, anger, joy, surprise, and love
- **Mental Health Risk Assessment**: Identifies potential mental health concerns
- **Sentiment Analysis**: Provides overall sentiment (positive/negative)
- **Pattern Detection**: Identifies concerning emotional patterns across conversations
- **Support Recommendations**: Suggests when professional help may be needed
- **Technology**: Uses Transformers library with DistilRoBERTa (MIT/Apache License)

### 3. 📍 Location Safety Scoring (Module 3)
- **Safety Score Calculation**: Real-time safety scoring (0-100) for any location
- **Crime Hotspot Detection**: Identifies nearby high-risk areas
- **Time-based Risk Assessment**: Adjusts safety scores based on time of day
- **Safe Route Finding**: Suggests safer routes between two points
- **Safety Heatmaps**: Visual representation of safety levels in an area
- **Incident Alerts**: Notifies about nearby crime incidents
- **Technology**: Uses geopy, folium for geolocation and mapping

### 4. 🆘 Emergency Alert System (Module 4)
- **Panic Button**: One-touch emergency SOS alert
- **Location Sharing**: Real-time location sharing with trusted contacts
- **SMS Alerts**: Sends emergency alerts via Twilio
- **Emergency Contacts Management**: Add/remove trusted contacts
- **Safety Check-ins**: Regular check-ins with contacts
- **SOS History**: Track all emergency alerts
- **Technology**: Twilio API (MIT License) for SMS notifications

## 🏗️ Architecture

```
SheSafehelp/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── modules/                  # Core AI/ML modules
│   │   ├── toxicity_detector.py  # Module 1: Toxicity detection
│   │   ├── emotion_detector.py   # Module 2: Emotion analysis
│   │   ├── safety_scorer.py      # Module 3: Location safety
│   │   └── sos_system.py         # Module 4: Emergency alerts
│   └── routes/                   # API endpoints
│       ├── toxicity_routes.py
│       ├── emotion_routes.py
│       ├── safety_routes.py
│       └── sos_routes.py
├── frontend/
│   ├── templates/
│   │   └── index.html            # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css         # Responsive styling
│       └── js/
│           └── app.js            # Frontend logic
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd SheSafehelp
```

2. **Create a virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Detoxify (toxicity detection)
- Transformers (emotion analysis)
- Geopy & Folium (location services)
- Twilio (SMS alerts)
- And other required packages

4. **Setup environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
# Twilio Configuration (for SMS alerts)
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development

# Emergency Contacts
EMERGENCY_CONTACTS=+1234567890,+0987654321
```

**Note**: The application will work without Twilio credentials, but SMS alerts will be simulated.

5. **Run the application**
```bash
cd backend
python app.py
```

6. **Access the application**

Open your browser and navigate to:
```
http://localhost:5000
```

## 📱 Usage Guide

### Toxicity Detection
1. Navigate to **Toxicity Check** section
2. Enter text or paste conversation messages
3. Click **Analyze** to get detailed toxicity scores
4. Review risk levels and specific categories

### Mental Health Analysis
1. Go to **Mental Health** section
2. Enter text to analyze emotional state
3. View emotion breakdown and mental health risk assessment
4. Follow recommendations if support is needed

### Location Safety
1. Open **Location Safety** section
2. Use current location or enter coordinates
3. Get safety score and nearby incident reports
4. Use **Find Safe Route** for navigation between points

### Emergency SOS
1. Access **SOS** section
2. Add emergency contacts (phone numbers)
3. Use panic button to send instant alerts
4. Share live location with trusted contacts
5. Send safety check-ins

## 🔌 API Endpoints

### Toxicity Detection
- `POST /api/toxicity/analyze` - Analyze single text
- `POST /api/toxicity/analyze-conversation` - Analyze conversation

### Emotion Detection
- `POST /api/emotion/analyze` - Analyze emotions
- `POST /api/emotion/analyze-conversation` - Analyze conversation emotions

### Safety Scoring
- `POST /api/safety/score` - Get location safety score
- `POST /api/safety/route` - Find safe route
- `POST /api/safety/map` - Generate safety heatmap

### SOS System
- `POST /api/sos/alert` - Send SOS alert
- `POST /api/sos/share-location` - Share location
- `POST /api/sos/checkin` - Send safety check-in
- `GET /api/sos/contacts` - Get emergency contacts
- `POST /api/sos/contacts` - Add emergency contact
- `DELETE /api/sos/contacts/<phone>` - Remove contact

## 🧪 Testing

### Test Toxicity Detection
```python
import requests

response = requests.post('http://localhost:5000/api/toxicity/analyze', 
    json={'text': 'Your text here'})
print(response.json())
```

### Test Emotion Analysis
```python
response = requests.post('http://localhost:5000/api/emotion/analyze',
    json={'text': 'I am feeling worried and scared'})
print(response.json())
```

### Test Safety Scoring
```python
response = requests.post('http://localhost:5000/api/safety/score',
    json={'latitude': 28.6139, 'longitude': 77.2090})
print(response.json())
```

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` file with real credentials
2. **HTTPS**: Use HTTPS in production
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: All inputs are validated and sanitized
5. **Emergency Contacts**: Store securely in production database

## 📚 Technology Stack

### Backend
- **Flask**: Web framework
- **Detoxify**: Toxicity detection (MIT License)
- **Transformers**: Emotion analysis (Apache 2.0)
- **PyTorch**: ML framework
- **Twilio**: SMS notifications (MIT License)
- **Geopy**: Geocoding and distance calculations
- **Folium**: Interactive maps

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript (ES6+)**: Interactive features
- **Font Awesome**: Icons
- **Socket.IO**: Real-time communication

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project uses MIT-licensed components:

- Detoxify: MIT License - https://github.com/unitaryai/detoxify
- Transformers: Apache 2.0 License - https://github.com/huggingface/transformers
- Twilio Python SDK: MIT License
- Flask: BSD-3-Clause License

**This project is safe for commercial use.**

## 🌐 Deployment

### Deploy to Heroku

1. Create `Procfile`:
```
web: cd backend && gunicorn app:app
```

2. Add `gunicorn` to requirements.txt:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
```

### Deploy to AWS/Azure
- Use Docker containerization
- Set up environment variables in platform settings
- Configure HTTPS/SSL certificates
- Set up database for production

## 🆘 Support & Resources

### Crisis Helplines (India)
- **Women Helpline**: 1091
- **Police**: 100
- **National Commission for Women**: 7827-170-170
- **Mental Health Helpline**: 1800-599-0019

### International
- **USA**: 911 (Emergency), 1-800-273-8255 (Crisis)
- **UK**: 999 (Emergency), 0800-689-5652 (Crisis)

## 📞 Contact

For questions or support, please open an issue on GitHub.

## 🎯 Roadmap

- [ ] Mobile app (React Native)
- [ ] Real-time chat monitoring
- [ ] ML model fine-tuning with local crime data
- [ ] Integration with local police databases
- [ ] Multi-language support
- [ ] Voice-activated SOS
- [ ] Wearable device integration
- [ ] Community safety reports

## ⭐ Acknowledgments

This project uses and builds upon several open-source libraries:
- Detoxify by Unitary AI
- Transformers by Hugging Face
- Flask by Pallets
- Twilio SDK

Special thanks to all contributors and the open-source community!

---

**Made with ❤️ for women's safety**

Remember: Your safety matters. Use this tool to stay protected online and offline.

# 🚀 SheSafe - Quick Start Guide

Get up and running with SheSafe in 5 minutes!

## ⚡ Super Quick Start

### Option 1: Automated Setup (Recommended)

**For macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**For Windows:**
```bash
start.bat
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Start the app
cd backend
python app.py
```

### Option 3: Python Setup Script

```bash
python setup.py
cd backend
python app.py
```

## 🌐 Access the Application

Open your browser and go to:
```
http://localhost:5000
```

## 🎯 First Steps

### 1. Test Toxicity Detection
1. Click on **"Toxicity Check"** in the navigation
2. Enter some text: "This is a friendly message"
3. Click **"Analyze"**
4. View the toxicity scores!

### 2. Test Emotion Analysis
1. Navigate to **"Mental Health"**
2. Enter: "I'm feeling happy and excited today!"
3. Click **"Analyze"**
4. See your emotional breakdown

### 3. Test Location Safety
1. Go to **"Location Safety"**
2. Click **"Use My Current Location"** (allow browser permission)
3. Click **"Get Safety Score"**
4. View your area's safety rating

### 4. Setup Emergency SOS
1. Navigate to **"SOS"**
2. Add emergency contacts (phone numbers)
3. Test the features (location sharing, check-ins)

## ⚙️ Twilio Setup (Optional but Recommended)

To enable real SMS alerts:

1. **Sign up for Twilio** (free trial available)
   - Go to https://www.twilio.com/try-twilio
   - Get $15 free credit

2. **Get your credentials**
   - Account SID
   - Auth Token
   - Phone Number

3. **Add to .env file**
```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

4. **Restart the app**
```bash
cd backend
python app.py
```

## 🧪 Test the APIs

### Using cURL

```bash
# Test toxicity detection
curl -X POST http://localhost:5000/api/toxicity/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world"}'

# Test emotion analysis
curl -X POST http://localhost:5000/api/emotion/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "I am so happy today!"}'

# Test safety score
curl -X POST http://localhost:5000/api/safety/score \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.6139, "longitude": 77.2090}'
```

### Using Python

```python
import requests

# Test toxicity
response = requests.post('http://localhost:5000/api/toxicity/analyze',
    json={'text': 'Hello world'})
print(response.json())

# Test emotion
response = requests.post('http://localhost:5000/api/emotion/analyze',
    json={'text': 'I am happy!'})
print(response.json())

# Test safety
response = requests.post('http://localhost:5000/api/safety/score',
    json={'latitude': 28.6139, 'longitude': 77.2090})
print(response.json())
```

## 📱 Features Overview

### 🛡️ Toxicity Detection
- Analyze messages for harassment
- Detect threats and abuse
- Get risk levels (LOW/MEDIUM/HIGH/CRITICAL)

### 💝 Mental Health
- Emotion analysis (sadness, fear, anger, joy)
- Mental health risk assessment
- Support recommendations

### 📍 Location Safety
- Real-time safety scores (0-100)
- Crime hotspot detection
- Safe route finding
- Interactive safety maps

### 🆘 Emergency SOS
- One-touch panic button
- Location sharing via SMS
- Safety check-ins
- Emergency contact management

## 🐛 Troubleshooting

### Models Taking Too Long to Download?
First run downloads AI models (can take 5-10 minutes). Be patient!

### Port 5000 Already in Use?
```bash
# Find and kill the process
lsof -i :5000
kill -9 <PID>
```

### Import Errors?
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Permission Denied?
```bash
chmod +x start.sh
```

### Location Not Working?
- Enable location permissions in browser
- Use HTTPS in production (required for geolocation)

## 📚 Learn More

- **Full Documentation**: See [README.md](README.md)
- **API Reference**: See [API_DOCS.md](API_DOCS.md)
- **Deployment**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## 🆘 Need Help?

1. **Check logs** in terminal where app is running
2. **Test modules**: `python test_modules.py`
3. **Open an issue** on GitHub
4. **Check API health**: http://localhost:5000/api/health

## 🎯 Next Steps

Once you're comfortable:

1. **Add your emergency contacts**
2. **Customize safety zones** (edit crime hotspot data)
3. **Integrate with real crime databases**
4. **Deploy to production** (see DEPLOYMENT.md)
5. **Build mobile app** (React Native)

## 📞 Emergency Resources

### India
- **Police**: 100
- **Women Helpline**: 1091
- **Child Helpline**: 1098
- **Mental Health**: 1800-599-0019

### USA
- **Emergency**: 911
- **Crisis Hotline**: 1-800-273-8255

### UK
- **Emergency**: 999
- **Women's Aid**: 0808-2000-247

---

**Made with ❤️ for women's safety**

Your safety matters. Use this tool responsibly and stay safe! 🛡️


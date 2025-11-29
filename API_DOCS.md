# SheSafe - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication
Currently, no authentication is required for local development. In production, implement API keys or OAuth.

---

## Module 1: Toxicity Detection

### Analyze Single Text
Analyze a single piece of text for toxicity, threats, insults, etc.

**Endpoint:** `POST /toxicity/analyze`

**Request Body:**
```json
{
  "text": "Your text to analyze"
}
```

**Response:**
```json
{
  "scores": {
    "toxicity": 0.05,
    "severe_toxicity": 0.01,
    "obscene": 0.02,
    "threat": 0.01,
    "insult": 0.03,
    "identity_attack": 0.01
  },
  "max_score": 0.05,
  "risk_level": "LOW",
  "is_toxic": false,
  "text_analyzed": "Your text..."
}
```

### Analyze Conversation
Analyze multiple messages to detect patterns of abuse.

**Endpoint:** `POST /toxicity/analyze-conversation`

**Request Body:**
```json
{
  "messages": [
    "First message",
    "Second message",
    "Third message"
  ]
}
```

**Response:**
```json
{
  "message_count": 3,
  "toxic_message_count": 1,
  "toxicity_percentage": 33.33,
  "average_scores": {
    "toxicity": 0.15,
    ...
  },
  "overall_risk_level": "MEDIUM"
}
```

---

## Module 2: Emotion Detection

### Analyze Emotions
Analyze emotional state and mental health indicators.

**Endpoint:** `POST /emotion/analyze`

**Request Body:**
```json
{
  "text": "I'm feeling worried and scared today"
}
```

**Response:**
```json
{
  "emotions": {
    "sadness": 0.45,
    "fear": 0.60,
    "anger": 0.10,
    "joy": 0.05,
    "surprise": 0.03,
    "love": 0.02
  },
  "dominant_emotion": {
    "name": "fear",
    "score": 0.60
  },
  "sentiment": {
    "label": "NEGATIVE",
    "score": 0.89
  },
  "mental_health_risk": {
    "level": "MEDIUM",
    "distress_score": 0.85,
    "positive_score": 0.07,
    "net_score": 0.78
  },
  "needs_support": false
}
```

### Analyze Conversation Emotions
Detect emotional patterns across multiple messages.

**Endpoint:** `POST /emotion/analyze-conversation`

**Request Body:**
```json
{
  "messages": [
    "Message 1",
    "Message 2",
    "Message 3"
  ]
}
```

---

## Module 3: Safety Scoring

### Get Location Safety Score
Get safety score for a specific location.

**Endpoint:** `POST /safety/score`

**Request Body:**
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

**Response:**
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "location_name": "Connaught Place, New Delhi...",
  "safety_score": 75.5,
  "safety_level": "SAFE",
  "crime_risk": 0.25,
  "time_risk_factor": 1.2,
  "nearby_incidents": [
    {
      "type": "theft",
      "severity": "medium",
      "distance_km": 0.5
    }
  ],
  "recommendations": [
    "Generally safe area",
    "Stay aware of surroundings"
  ]
}
```

### Find Safe Route
Find a safe route between two locations.

**Endpoint:** `POST /safety/route`

**Request Body:**
```json
{
  "start_latitude": 28.6139,
  "start_longitude": 77.2090,
  "end_latitude": 28.6500,
  "end_longitude": 77.2300
}
```

**Response:**
```json
{
  "start": {
    "latitude": 28.6139,
    "longitude": 77.2090
  },
  "end": {
    "latitude": 28.6500,
    "longitude": 77.2300
  },
  "distance_km": 4.5,
  "average_safety_score": 72.3,
  "minimum_safety_score": 65.0,
  "overall_route_safety": "MODERATE",
  "waypoints": [...],
  "warnings": [...]
}
```

### Generate Safety Map
Generate an interactive safety heatmap.

**Endpoint:** `POST /safety/map`

**Request Body:**
```json
{
  "latitude": 28.6139,
  "longitude": 77.2090,
  "radius_km": 2
}
```

---

## Module 4: SOS System

### Send SOS Alert
Send emergency alert to all contacts.

**Endpoint:** `POST /sos/alert`

**Request Body:**
```json
{
  "user_name": "Jane Doe",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "message": "Need help urgently",
  "contacts": ["+1234567890"]  // Optional, uses defaults if not provided
}
```

**Response:**
```json
{
  "status": "success",
  "message": "SOS alert sent to 2 contacts",
  "timestamp": "2025-11-29T10:30:00",
  "location_link": "https://www.google.com/maps?q=28.6139,77.2090",
  "contacts_alerted": [
    {
      "contact": "+1234567890",
      "status": "sent"
    }
  ]
}
```

### Share Location
Share current location with contacts.

**Endpoint:** `POST /sos/share-location`

**Request Body:**
```json
{
  "user_name": "Jane Doe",
  "latitude": 28.6139,
  "longitude": 77.2090,
  "contacts": ["+1234567890"]  // Optional
}
```

### Send Safety Check-in
Send safety check-in message.

**Endpoint:** `POST /sos/checkin`

**Request Body:**
```json
{
  "user_name": "Jane Doe",
  "status": "Reached home safely",
  "contacts": ["+1234567890"]  // Optional
}
```

### Get Emergency Contacts
Retrieve list of emergency contacts.

**Endpoint:** `GET /sos/contacts`

**Response:**
```json
{
  "contacts": [
    "+1234567890",
    "+0987654321"
  ]
}
```

### Add Emergency Contact
Add a new emergency contact.

**Endpoint:** `POST /sos/contacts`

**Request Body:**
```json
{
  "phone_number": "+1234567890",
  "name": "Mom"  // Optional
}
```

### Remove Emergency Contact
Remove an emergency contact.

**Endpoint:** `DELETE /sos/contacts/{phone_number}`

**Example:** `DELETE /sos/contacts/+1234567890`

### Get SOS History
Get recent SOS alerts history.

**Endpoint:** `GET /sos/history?limit=10`

**Query Parameters:**
- `limit` (optional): Number of recent events to retrieve (default: 10)

---

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "error": "Error message description"
}
```

Common HTTP status codes:
- `200 OK`: Successful request
- `400 Bad Request`: Invalid input parameters
- `500 Internal Server Error`: Server-side error

---

## Rate Limiting

For production deployment, implement rate limiting:
- 100 requests per minute per IP for general endpoints
- 10 requests per minute for SOS alerts (to prevent abuse)

## Examples Using cURL

### Analyze Toxicity
```bash
curl -X POST http://localhost:5000/api/toxicity/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test message"}'
```

### Get Safety Score
```bash
curl -X POST http://localhost:5000/api/safety/score \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.6139, "longitude": 77.2090}'
```

### Send SOS
```bash
curl -X POST http://localhost:5000/api/sos/alert \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "Jane",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "message": "Emergency"
  }'
```


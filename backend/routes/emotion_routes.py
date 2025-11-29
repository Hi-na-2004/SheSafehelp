"""
API Routes for Emotion Detection Module
"""
from flask import Blueprint, request, jsonify
from modules.emotion_detector import emotion_detector

emotion_bp = Blueprint('emotion', __name__)


@emotion_bp.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotions in text"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = emotion_detector.analyze_emotion(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emotion_bp.route('/analyze-conversation', methods=['POST'])
def analyze_conversation_emotions():
    """Analyze emotions across multiple messages"""
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        result = emotion_detector.analyze_conversation_emotions(messages)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@emotion_bp.route('/check', methods=['GET'])
def check_status():
    """Check if emotion detection is working"""
    return jsonify({
        'status': 'active',
        'emotion_model_loaded': emotion_detector.emotion_classifier is not None,
        'sentiment_model_loaded': emotion_detector.sentiment_analyzer is not None
    })


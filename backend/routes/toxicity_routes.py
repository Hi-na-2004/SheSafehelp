"""
API Routes for Toxicity Detection Module
"""
from flask import Blueprint, request, jsonify
from modules.toxicity_detector import toxicity_detector

toxicity_bp = Blueprint('toxicity', __name__)


@toxicity_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """Analyze text for toxicity"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        result = toxicity_detector.analyze_text(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@toxicity_bp.route('/analyze-conversation', methods=['POST'])
def analyze_conversation():
    """Analyze multiple messages in a conversation"""
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({'error': 'No messages provided'}), 400
        
        result = toxicity_detector.analyze_conversation(messages)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@toxicity_bp.route('/check', methods=['GET'])
def check_status():
    """Check if toxicity detection is working"""
    return jsonify({
        'status': 'active',
        'model_loaded': toxicity_detector.model is not None
    })


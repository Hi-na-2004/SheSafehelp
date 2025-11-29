"""
API Routes for Safety Scoring Module
"""
from flask import Blueprint, request, jsonify
from modules.safety_scorer import safety_scorer
from datetime import datetime

safety_bp = Blueprint('safety', __name__)


@safety_bp.route('/score', methods=['POST'])
def get_safety_score():
    """Get safety score for a location"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        result = safety_scorer.get_location_safety_score(
            float(latitude),
            float(longitude),
            datetime.now()
        )
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@safety_bp.route('/route', methods=['POST'])
def find_safe_route():
    """Find safe route between two points"""
    try:
        data = request.get_json()
        start_lat = data.get('start_latitude')
        start_lng = data.get('start_longitude')
        end_lat = data.get('end_latitude')
        end_lng = data.get('end_longitude')
        
        if None in [start_lat, start_lng, end_lat, end_lng]:
            return jsonify({'error': 'All coordinates required'}), 400
        
        result = safety_scorer.find_safe_route(
            float(start_lat),
            float(start_lng),
            float(end_lat),
            float(end_lng)
        )
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@safety_bp.route('/map', methods=['POST'])
def generate_map():
    """Generate safety heatmap"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius = data.get('radius_km', 2)
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        result = safety_scorer.generate_safety_map(
            float(latitude),
            float(longitude),
            float(radius)
        )
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@safety_bp.route('/check', methods=['GET'])
def check_status():
    """Check if safety scoring is working"""
    return jsonify({
        'status': 'active',
        'crime_hotspots_loaded': len(safety_scorer.crime_hotspots) > 0
    })


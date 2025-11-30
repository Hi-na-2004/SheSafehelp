"""
API Routes for Safety Scoring Module
"""
from flask import Blueprint, request, jsonify
from modules.safety_scorer import safety_scorer
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

safety_bp = Blueprint('safety', __name__)

# Initialize geocoder
geocoder = Nominatim(user_agent="safecircle_app")


def geocode_place(place_name):
    """Convert place name to coordinates"""
    try:
        location = geocoder.geocode(place_name, timeout=10)
        if location:
            return {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'address': location.address
            }
        return None
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        return None


@safety_bp.route('/score', methods=['POST'])
def get_safety_score():
    """Get safety score for a location (by coordinates or place name)"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        place_name = data.get('place_name')
        
        # If place name is provided, geocode it
        if place_name:
            location = geocode_place(place_name)
            if not location:
                return jsonify({'error': f'Could not find location: {place_name}'}), 404
            latitude = location['latitude']
            longitude = location['longitude']
            
        # Check if we have coordinates
        if latitude is None or longitude is None:
            return jsonify({'error': 'Either provide latitude/longitude or place_name'}), 400
        
        result = safety_scorer.get_location_safety_score(
            float(latitude),
            float(longitude),
            datetime.now()
        )
        
        # Add location info if geocoded
        if place_name:
            result['location_name'] = place_name
            result['geocoded_address'] = location['address']
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@safety_bp.route('/geocode', methods=['POST'])
def geocode_location():
    """Convert place name to coordinates"""
    try:
        data = request.get_json()
        place_name = data.get('place_name')
        
        if not place_name:
            return jsonify({'error': 'place_name required'}), 400
        
        location = geocode_place(place_name)
        
        if not location:
            return jsonify({'error': f'Could not find location: {place_name}'}), 404
        
        return jsonify({
            'success': True,
            'place_name': place_name,
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'address': location['address']
        })
    
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


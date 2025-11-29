"""
API Routes for SOS System Module
"""
from flask import Blueprint, request, jsonify
from modules.sos_system import sos_system

sos_bp = Blueprint('sos', __name__)


@sos_bp.route('/alert', methods=['POST'])
def send_sos_alert():
    """Send SOS alert to emergency contacts"""
    try:
        data = request.get_json()
        user_name = data.get('user_name', 'Unknown User')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        message = data.get('message', '')
        contacts = data.get('contacts')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Location coordinates required'}), 400
        
        result = sos_system.send_sos_alert(
            user_name,
            float(latitude),
            float(longitude),
            message,
            contacts
        )
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sos_bp.route('/share-location', methods=['POST'])
def share_location():
    """Share live location with contacts"""
    try:
        data = request.get_json()
        user_name = data.get('user_name', 'Unknown User')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        contacts = data.get('contacts')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Location coordinates required'}), 400
        
        result = sos_system.share_live_location(
            user_name,
            float(latitude),
            float(longitude),
            contacts
        )
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sos_bp.route('/checkin', methods=['POST'])
def safety_checkin():
    """Send safety check-in to contacts"""
    try:
        data = request.get_json()
        user_name = data.get('user_name', 'Unknown User')
        status = data.get('status', 'Safe')
        contacts = data.get('contacts')
        
        result = sos_system.send_safety_checkin(user_name, status, contacts)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sos_bp.route('/history', methods=['GET'])
def get_history():
    """Get SOS history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = sos_system.get_sos_history(limit)
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sos_bp.route('/contacts', methods=['GET'])
def get_contacts():
    """Get emergency contacts"""
    return jsonify({'contacts': sos_system.emergency_contacts})


@sos_bp.route('/contacts', methods=['POST'])
def add_contact():
    """Add emergency contact"""
    try:
        data = request.get_json()
        phone = data.get('phone_number')
        name = data.get('name', '')
        
        if not phone:
            return jsonify({'error': 'Phone number required'}), 400
        
        result = sos_system.add_emergency_contact(phone, name)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sos_bp.route('/contacts/<phone_number>', methods=['DELETE'])
def remove_contact(phone_number):
    """Remove emergency contact"""
    try:
        result = sos_system.remove_emergency_contact(phone_number)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sos_bp.route('/check', methods=['GET'])
def check_status():
    """Check if SOS system is working"""
    return jsonify({
        'status': 'active',
        'twilio_configured': sos_system.client is not None,
        'emergency_contacts_count': len(sos_system.emergency_contacts)
    })


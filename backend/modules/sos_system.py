"""
Module 4: SOS & Emergency Alert System
Uses Twilio for SMS alerts (MIT License reference)
Provides panic button, location sharing, and emergency notifications
"""
import os
from twilio.rest import Client
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class SOSSystem:
    """Emergency SOS and alert system"""
    
    def __init__(self):
        """Initialize SOS system with Twilio"""
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        
        # Initialize Twilio client if credentials available
        if self.twilio_sid and self.twilio_token:
            try:
                self.client = Client(self.twilio_sid, self.twilio_token)
                logger.info("✅ Twilio SOS system initialized")
            except Exception as e:
                logger.error(f"❌ Error initializing Twilio: {e}")
                self.client = None
        else:
            logger.warning("⚠️ Twilio credentials not found - SOS SMS will be simulated")
            self.client = None
        
        # Emergency contacts
        self.emergency_contacts = self._load_emergency_contacts()
        
        # SOS history
        self.sos_history = []
    
    def send_sos_alert(self, user_name, latitude, longitude, message="", contacts=None):
        """
        Send SOS alert to emergency contacts
        
        Args:
            user_name (str): Name of person in distress
            latitude (float): Current latitude
            longitude (float): Current longitude
            message (str): Optional additional message
            contacts (list): Phone numbers to alert
            
        Returns:
            dict: Status of SOS alert
        """
        try:
            # Use provided contacts or default emergency contacts
            recipients = contacts or self.emergency_contacts
            
            if not recipients:
                return {
                    "status": "error",
                    "message": "No emergency contacts configured"
                }
            
            # Create Google Maps link
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            
            # Compose SOS message
            sos_message = self._compose_sos_message(user_name, maps_link, message)
            
            # Send alerts
            results = []
            for contact in recipients:
                result = self._send_sms(contact, sos_message)
                results.append({
                    'contact': contact,
                    'status': result['status'],
                    'message_sid': result.get('message_sid')
                })
            
            # Log SOS event
            sos_event = {
                'timestamp': datetime.now().isoformat(),
                'user_name': user_name,
                'location': {'latitude': latitude, 'longitude': longitude},
                'message': message,
                'contacts_alerted': len(recipients),
                'results': results
            }
            self.sos_history.append(sos_event)
            
            return {
                'status': 'success',
                'message': f'SOS alert sent to {len(recipients)} contacts',
                'timestamp': sos_event['timestamp'],
                'location_link': maps_link,
                'contacts_alerted': results
            }
            
        except Exception as e:
            logger.error(f"Error sending SOS alert: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def share_live_location(self, user_name, latitude, longitude, contacts=None):
        """
        Share live location with trusted contacts
        
        Args:
            user_name (str): User's name
            latitude (float): Current latitude
            longitude (float): Current longitude
            contacts (list): Phone numbers to share with
            
        Returns:
            dict: Status of location sharing
        """
        try:
            recipients = contacts or self.emergency_contacts
            
            if not recipients:
                return {
                    "status": "error",
                    "message": "No contacts configured for location sharing"
                }
            
            maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"
            
            location_message = (
                f"📍 Location Update from {user_name}\n\n"
                f"Current location: {maps_link}\n\n"
                f"Time: {datetime.now().strftime('%I:%M %p, %d %b %Y')}\n\n"
                f"Track location: Follow the link above"
            )
            
            results = []
            for contact in recipients:
                result = self._send_sms(contact, location_message)
                results.append({
                    'contact': contact,
                    'status': result['status']
                })
            
            return {
                'status': 'success',
                'message': f'Location shared with {len(recipients)} contacts',
                'location_link': maps_link,
                'contacts': results
            }
            
        except Exception as e:
            logger.error(f"Error sharing location: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def send_safety_checkin(self, user_name, status, contacts=None):
        """
        Send safety check-in to contacts
        
        Args:
            user_name (str): User's name
            status (str): Safety status message
            contacts (list): Phone numbers to notify
            
        Returns:
            dict: Status of check-in
        """
        try:
            recipients = contacts or self.emergency_contacts
            
            checkin_message = (
                f"✅ Safety Check-in from {user_name}\n\n"
                f"Status: {status}\n"
                f"Time: {datetime.now().strftime('%I:%M %p, %d %b %Y')}\n\n"
                f"All is well!"
            )
            
            results = []
            for contact in recipients:
                result = self._send_sms(contact, checkin_message)
                results.append({
                    'contact': contact,
                    'status': result['status']
                })
            
            return {
                'status': 'success',
                'message': f'Check-in sent to {len(recipients)} contacts',
                'contacts': results
            }
            
        except Exception as e:
            logger.error(f"Error sending check-in: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_sos_history(self, limit=10):
        """
        Retrieve recent SOS history
        
        Args:
            limit (int): Number of recent events to retrieve
            
        Returns:
            list: Recent SOS events
        """
        return self.sos_history[-limit:]
    
    def add_emergency_contact(self, phone_number, name=""):
        """
        Add emergency contact
        
        Args:
            phone_number (str): Contact phone number
            name (str): Contact name (optional)
            
        Returns:
            dict: Status of addition
        """
        try:
            if phone_number not in self.emergency_contacts:
                self.emergency_contacts.append(phone_number)
                self._save_emergency_contacts()
                return {
                    'status': 'success',
                    'message': f'Contact added: {name or phone_number}'
                }
            else:
                return {
                    'status': 'info',
                    'message': 'Contact already exists'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def remove_emergency_contact(self, phone_number):
        """Remove emergency contact"""
        try:
            if phone_number in self.emergency_contacts:
                self.emergency_contacts.remove(phone_number)
                self._save_emergency_contacts()
                return {
                    'status': 'success',
                    'message': 'Contact removed'
                }
            else:
                return {
                    'status': 'error',
                    'message': 'Contact not found'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _send_sms(self, to_number, message):
        """Send SMS via Twilio or simulate if not configured"""
        if self.client and self.twilio_phone:
            try:
                message_obj = self.client.messages.create(
                    body=message,
                    from_=self.twilio_phone,
                    to=to_number
                )
                return {
                    'status': 'sent',
                    'message_sid': message_obj.sid
                }
            except Exception as e:
                logger.error(f"Twilio error: {e}")
                return {
                    'status': 'failed',
                    'error': str(e)
                }
        else:
            # Simulate SMS for testing
            logger.info(f"[SIMULATED SMS] To: {to_number}\nMessage: {message}")
            return {
                'status': 'simulated',
                'message': 'SMS simulated (Twilio not configured)'
            }
    
    @staticmethod
    def _compose_sos_message(user_name, maps_link, additional_message=""):
        """Compose SOS alert message"""
        message = (
            f"🆘 EMERGENCY ALERT 🆘\n\n"
            f"{user_name} needs immediate help!\n\n"
            f"📍 Location: {maps_link}\n\n"
        )
        
        if additional_message:
            message += f"Message: {additional_message}\n\n"
        
        message += (
            f"⏰ Time: {datetime.now().strftime('%I:%M %p, %d %b %Y')}\n\n"
            f"Please check on them immediately!"
        )
        
        return message
    
    def _load_emergency_contacts(self):
        """Load emergency contacts from environment or storage"""
        contacts_env = os.getenv('EMERGENCY_CONTACTS', '')
        if contacts_env:
            return [c.strip() for c in contacts_env.split(',') if c.strip()]
        return []
    
    def _save_emergency_contacts(self):
        """Save emergency contacts (in production, use database)"""
        # This is a placeholder - in production, save to database
        logger.info(f"Emergency contacts updated: {len(self.emergency_contacts)} contacts")


# Initialize global SOS system instance
sos_system = SOSSystem()


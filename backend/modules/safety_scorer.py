"""
Module 3: Crime Prediction & Location Safety Scoring
Uses geolocation analysis and crime data patterns (MIT License references)
Provides safety scores for locations and safe route suggestions
"""
import numpy as np
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import folium
from datetime import datetime, time
import logging
import json

logger = logging.getLogger(__name__)


class SafetyScorer:
    """Location safety scoring and crime prediction"""
    
    def __init__(self):
        """Initialize safety scoring system"""
        self.geolocator = Nominatim(user_agent="shesafe_app")
        
        # Sample crime hotspot data (in production, use real crime database)
        self.crime_hotspots = self._initialize_crime_data()
        
        # Time-based risk factors
        self.time_risk_factors = {
            'night': 1.5,  # 9 PM - 6 AM
            'evening': 1.2,  # 6 PM - 9 PM
            'day': 0.8,     # 6 AM - 6 PM
        }
        
        logger.info("✅ Safety scoring system initialized")
    
    def get_location_safety_score(self, latitude, longitude, current_time=None):
        """
        Calculate safety score for a given location
        
        Args:
            latitude (float): Location latitude
            longitude (float): Location longitude
            current_time (datetime): Time for time-based risk assessment
            
        Returns:
            dict: Safety score and risk factors
        """
        try:
            location = (latitude, longitude)
            
            # Calculate proximity to crime hotspots
            crime_risk = self._calculate_crime_risk(location)
            
            # Time-based risk
            time_risk = self._calculate_time_risk(current_time)
            
            # Calculate overall safety score (0-100, higher is safer)
            base_safety = 100 - (crime_risk * 100)
            adjusted_safety = max(0, min(100, base_safety / time_risk))
            
            # Determine safety level
            safety_level = self._get_safety_level(adjusted_safety)
            
            # Get location name
            location_name = self._get_location_name(latitude, longitude)
            
            return {
                'latitude': latitude,
                'longitude': longitude,
                'location_name': location_name,
                'safety_score': round(adjusted_safety, 2),
                'safety_level': safety_level,
                'crime_risk': round(crime_risk, 2),
                'time_risk_factor': round(time_risk, 2),
                'nearby_incidents': self._get_nearby_incidents(location),
                'recommendations': self._get_safety_recommendations(adjusted_safety, time_risk)
            }
        except Exception as e:
            logger.error(f"Error calculating safety score: {e}")
            return {"error": str(e)}
    
    def find_safe_route(self, start_lat, start_lng, end_lat, end_lng):
        """
        Find safer route between two points
        
        Args:
            start_lat, start_lng: Starting coordinates
            end_lat, end_lng: Destination coordinates
            
        Returns:
            dict: Route information with safety scores
        """
        try:
            # Calculate direct route
            start = (start_lat, start_lng)
            end = (end_lat, end_lng)
            distance = geodesic(start, end).kilometers
            
            # Sample multiple waypoints along the route
            num_waypoints = max(3, int(distance * 2))
            waypoints = []
            
            for i in range(num_waypoints + 1):
                fraction = i / num_waypoints
                lat = start_lat + (end_lat - start_lat) * fraction
                lng = start_lng + (end_lng - start_lng) * fraction
                
                safety = self.get_location_safety_score(lat, lng)
                waypoints.append({
                    'latitude': lat,
                    'longitude': lng,
                    'safety_score': safety.get('safety_score', 50)
                })
            
            # Calculate route safety score
            avg_safety = np.mean([w['safety_score'] for w in waypoints])
            min_safety = min([w['safety_score'] for w in waypoints])
            
            return {
                'start': {'latitude': start_lat, 'longitude': start_lng},
                'end': {'latitude': end_lat, 'longitude': end_lng},
                'distance_km': round(distance, 2),
                'waypoints': waypoints,
                'average_safety_score': round(avg_safety, 2),
                'minimum_safety_score': round(min_safety, 2),
                'overall_route_safety': self._get_safety_level(avg_safety),
                'warnings': self._get_route_warnings(waypoints)
            }
        except Exception as e:
            logger.error(f"Error finding safe route: {e}")
            return {"error": str(e)}
    
    def generate_safety_map(self, center_lat, center_lng, radius_km=2, output_file='safety_map.html'):
        """
        Generate an interactive safety heatmap
        
        Args:
            center_lat, center_lng: Center coordinates
            radius_km: Radius to analyze (in kilometers)
            output_file: Output HTML file path
            
        Returns:
            str: Path to generated map file
        """
        try:
            # Create base map
            safety_map = folium.Map(
                location=[center_lat, center_lng],
                zoom_start=13,
                tiles='OpenStreetMap'
            )
            
            # Add center marker
            folium.Marker(
                [center_lat, center_lng],
                popup='Your Location',
                icon=folium.Icon(color='blue', icon='home')
            ).add_to(safety_map)
            
            # Add crime hotspots
            for hotspot in self.crime_hotspots:
                if geodesic((center_lat, center_lng), 
                           (hotspot['lat'], hotspot['lng'])).kilometers <= radius_km:
                    
                    color = 'red' if hotspot['severity'] == 'high' else 'orange'
                    folium.CircleMarker(
                        location=[hotspot['lat'], hotspot['lng']],
                        radius=hotspot['severity_score'] * 20,
                        popup=f"Risk: {hotspot['severity']} - {hotspot['type']}",
                        color=color,
                        fill=True,
                        fillColor=color,
                        fillOpacity=0.4
                    ).add_to(safety_map)
            
            # Save map
            map_path = f"../frontend/static/{output_file}"
            safety_map.save(map_path)
            
            return {
                'map_file': output_file,
                'center': {'latitude': center_lat, 'longitude': center_lng},
                'radius_km': radius_km
            }
        except Exception as e:
            logger.error(f"Error generating safety map: {e}")
            return {"error": str(e)}
    
    def _initialize_crime_data(self):
        """Initialize sample crime hotspot data"""
        # In production, load this from a real crime database
        return [
            {'lat': 28.6139, 'lng': 77.2090, 'severity': 'high', 'severity_score': 0.8, 'type': 'theft'},
            {'lat': 28.6129, 'lng': 77.2290, 'severity': 'medium', 'severity_score': 0.5, 'type': 'harassment'},
            {'lat': 28.6339, 'lng': 77.2190, 'severity': 'high', 'severity_score': 0.9, 'type': 'assault'},
            {'lat': 28.7041, 'lng': 77.1025, 'severity': 'low', 'severity_score': 0.3, 'type': 'vandalism'},
            # Add more as needed
        ]
    
    def _calculate_crime_risk(self, location):
        """Calculate crime risk based on proximity to hotspots"""
        if not self.crime_hotspots:
            return 0.3  # Default moderate risk
        
        risks = []
        for hotspot in self.crime_hotspots:
            hotspot_location = (hotspot['lat'], hotspot['lng'])
            distance = geodesic(location, hotspot_location).kilometers
            
            # Risk decreases with distance (exponential decay)
            if distance < 0.5:
                risk = hotspot['severity_score']
            elif distance < 2:
                risk = hotspot['severity_score'] * np.exp(-distance/2)
            else:
                risk = hotspot['severity_score'] * 0.1
            
            risks.append(risk)
        
        # Return maximum risk from nearby hotspots
        return min(max(risks) if risks else 0.3, 1.0)
    
    def _calculate_time_risk(self, current_time=None):
        """Calculate risk factor based on time of day"""
        if current_time is None:
            current_time = datetime.now()
        
        hour = current_time.hour
        
        if 21 <= hour or hour < 6:  # 9 PM - 6 AM
            return self.time_risk_factors['night']
        elif 18 <= hour < 21:  # 6 PM - 9 PM
            return self.time_risk_factors['evening']
        else:  # 6 AM - 6 PM
            return self.time_risk_factors['day']
    
    def _get_location_name(self, latitude, longitude):
        """Get human-readable location name"""
        try:
            location = self.geolocator.reverse(f"{latitude}, {longitude}")
            return location.address if location else "Unknown Location"
        except:
            return "Unknown Location"
    
    def _get_nearby_incidents(self, location):
        """Get nearby crime incidents"""
        incidents = []
        for hotspot in self.crime_hotspots:
            hotspot_location = (hotspot['lat'], hotspot['lng'])
            distance = geodesic(location, hotspot_location).kilometers
            
            if distance < 1:  # Within 1 km
                incidents.append({
                    'type': hotspot['type'],
                    'severity': hotspot['severity'],
                    'distance_km': round(distance, 2)
                })
        
        return sorted(incidents, key=lambda x: x['distance_km'])[:5]
    
    @staticmethod
    def _get_safety_level(score):
        """Determine safety level from score"""
        if score >= 80:
            return "SAFE"
        elif score >= 60:
            return "MODERATE"
        elif score >= 40:
            return "CAUTION"
        else:
            return "UNSAFE"
    
    @staticmethod
    def _get_safety_recommendations(safety_score, time_risk):
        """Get safety recommendations"""
        recommendations = []
        
        if safety_score < 50:
            recommendations.append("⚠️ High risk area - Avoid if possible")
            recommendations.append("📱 Share your location with trusted contacts")
            recommendations.append("👥 Travel in groups")
        
        if time_risk > 1.3:
            recommendations.append("🌙 High-risk time period - Extra caution advised")
            recommendations.append("🚖 Consider using trusted transportation")
        
        if safety_score >= 80:
            recommendations.append("✅ Generally safe area")
            recommendations.append("👀 Stay aware of surroundings")
        
        return recommendations
    
    @staticmethod
    def _get_route_warnings(waypoints):
        """Generate warnings for unsafe sections of route"""
        warnings = []
        
        for i, waypoint in enumerate(waypoints):
            if waypoint['safety_score'] < 50:
                warnings.append(f"⚠️ Low safety zone at waypoint {i+1} (score: {waypoint['safety_score']:.1f})")
        
        return warnings


# Initialize global safety scorer instance
safety_scorer = SafetyScorer()


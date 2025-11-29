"""
Module 1: Toxicity Detection
Uses Detoxify (MIT License) - https://github.com/unitaryai/detoxify
Detects: Toxicity, Threat, Insult, Sexual content, Profanity, Hate speech
"""
from detoxify import Detoxify
import logging

logger = logging.getLogger(__name__)


class ToxicityDetector:
    """Toxicity detection using Detoxify model"""
    
    def __init__(self):
        """Initialize the Detoxify model"""
        try:
            # Using 'original' model - you can also use 'unbiased' or 'multilingual'
            self.model = Detoxify('original')
            logger.info("✅ Toxicity detection model loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading toxicity model: {e}")
            self.model = None
    
    def analyze_text(self, text):
        """
        Analyze text for various types of toxicity
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Toxicity scores for different categories
        """
        if not self.model:
            return {"error": "Model not loaded"}
        
        try:
            results = self.model.predict(text)
            
            # Calculate overall risk level
            max_score = max(results.values())
            risk_level = self._get_risk_level(max_score)
            
            return {
                'scores': {
                    'toxicity': float(results['toxicity']),
                    'severe_toxicity': float(results['severe_toxicity']),
                    'obscene': float(results['obscene']),
                    'threat': float(results['threat']),
                    'insult': float(results['insult']),
                    'identity_attack': float(results['identity_attack'])
                },
                'max_score': float(max_score),
                'risk_level': risk_level,
                'is_toxic': max_score > 0.5,
                'text_analyzed': text[:100] + '...' if len(text) > 100 else text
            }
        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return {"error": str(e)}
    
    def analyze_conversation(self, messages):
        """
        Analyze multiple messages in a conversation
        
        Args:
            messages (list): List of message strings
            
        Returns:
            dict: Aggregated toxicity analysis
        """
        if not messages:
            return {"error": "No messages provided"}
        
        results = []
        toxic_count = 0
        
        for msg in messages:
            analysis = self.analyze_text(msg)
            if not analysis.get('error'):
                results.append(analysis)
                if analysis.get('is_toxic'):
                    toxic_count += 1
        
        if not results:
            return {"error": "No valid analyses"}
        
        # Calculate average scores
        avg_scores = {}
        for key in results[0]['scores'].keys():
            avg_scores[key] = sum(r['scores'][key] for r in results) / len(results)
        
        return {
            'message_count': len(messages),
            'toxic_message_count': toxic_count,
            'toxicity_percentage': (toxic_count / len(messages)) * 100,
            'average_scores': avg_scores,
            'individual_results': results,
            'overall_risk_level': self._get_risk_level(max(avg_scores.values()))
        }
    
    @staticmethod
    def _get_risk_level(score):
        """Determine risk level based on score"""
        if score < 0.3:
            return "LOW"
        elif score < 0.6:
            return "MEDIUM"
        elif score < 0.8:
            return "HIGH"
        else:
            return "CRITICAL"


# Initialize global detector instance
toxicity_detector = ToxicityDetector()


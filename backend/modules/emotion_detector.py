"""
Module 2: Emotion & Mental Health Detection
Uses Transformers with emotion classification models (MIT/Apache License)
Detects: Sadness, Fear, Anger, Joy, Surprise, Love
"""
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)


class EmotionDetector:
    """Emotion and mental health analysis using transformer models"""
    
    def __init__(self):
        """Initialize emotion detection pipeline"""
        try:
            # Using distilbert-based emotion classifier
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
            
            # Sentiment analysis for additional context
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english"
            )
            
            logger.info("✅ Emotion detection models loaded successfully")
        except Exception as e:
            logger.error(f"❌ Error loading emotion models: {e}")
            self.emotion_classifier = None
            self.sentiment_analyzer = None
    
    def analyze_emotion(self, text):
        """
        Analyze emotions in text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Emotion scores and mental health indicators
        """
        if not self.emotion_classifier or not self.sentiment_analyzer:
            return {"error": "Models not loaded"}
        
        try:
            # Get emotion scores
            emotion_results = self.emotion_classifier(text)[0]
            emotions = {item['label']: float(item['score']) for item in emotion_results}
            
            # Get sentiment
            sentiment = self.sentiment_analyzer(text)[0]
            
            # Find dominant emotion
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])
            
            # Assess mental health risk
            mental_health_risk = self._assess_mental_health_risk(emotions)
            
            return {
                'emotions': emotions,
                'dominant_emotion': {
                    'name': dominant_emotion[0],
                    'score': dominant_emotion[1]
                },
                'sentiment': {
                    'label': sentiment['label'],
                    'score': float(sentiment['score'])
                },
                'mental_health_risk': mental_health_risk,
                'needs_support': mental_health_risk['level'] in ['HIGH', 'CRITICAL'],
                'text_analyzed': text[:100] + '...' if len(text) > 100 else text
            }
        except Exception as e:
            logger.error(f"Error analyzing emotions: {e}")
            return {"error": str(e)}
    
    def analyze_conversation_emotions(self, messages):
        """
        Analyze emotions across multiple messages to detect patterns
        
        Args:
            messages (list): List of message strings
            
        Returns:
            dict: Emotional pattern analysis
        """
        if not messages:
            return {"error": "No messages provided"}
        
        results = []
        high_risk_count = 0
        
        for msg in messages:
            analysis = self.analyze_emotion(msg)
            if not analysis.get('error'):
                results.append(analysis)
                if analysis['mental_health_risk']['level'] in ['HIGH', 'CRITICAL']:
                    high_risk_count += 1
        
        if not results:
            return {"error": "No valid analyses"}
        
        # Aggregate emotions
        emotion_totals = {}
        for result in results:
            for emotion, score in result['emotions'].items():
                emotion_totals[emotion] = emotion_totals.get(emotion, 0) + score
        
        # Calculate averages
        emotion_averages = {k: v/len(results) for k, v in emotion_totals.items()}
        
        # Detect concerning patterns
        patterns = self._detect_emotional_patterns(results)
        
        return {
            'message_count': len(messages),
            'high_risk_message_count': high_risk_count,
            'average_emotions': emotion_averages,
            'emotional_patterns': patterns,
            'overall_mental_health_risk': self._aggregate_mental_health_risk(results),
            'recommendation': self._get_recommendation(patterns, high_risk_count, len(messages))
        }
    
    @staticmethod
    def _assess_mental_health_risk(emotions):
        """Assess mental health risk based on emotion scores"""
        # Calculate distress indicators
        distress_score = (
            emotions.get('sadness', 0) * 1.2 +
            emotions.get('fear', 0) * 1.3 +
            emotions.get('anger', 0) * 0.8
        )
        
        positive_score = (
            emotions.get('joy', 0) +
            emotions.get('love', 0) * 0.8
        )
        
        # Net emotional state
        net_score = distress_score - positive_score
        
        if net_score < 0.3:
            level = "LOW"
        elif net_score < 0.6:
            level = "MEDIUM"
        elif net_score < 0.9:
            level = "HIGH"
        else:
            level = "CRITICAL"
        
        return {
            'level': level,
            'distress_score': float(distress_score),
            'positive_score': float(positive_score),
            'net_score': float(net_score)
        }
    
    @staticmethod
    def _detect_emotional_patterns(results):
        """Detect concerning emotional patterns"""
        patterns = []
        
        # Check for persistent negative emotions
        negative_count = sum(1 for r in results 
                           if r['dominant_emotion']['name'] in ['sadness', 'fear', 'anger'])
        if negative_count > len(results) * 0.6:
            patterns.append("persistent_negative_emotions")
        
        # Check for emotional escalation
        if len(results) >= 3:
            recent_distress = [r['mental_health_risk']['distress_score'] for r in results[-3:]]
            if all(recent_distress[i] < recent_distress[i+1] for i in range(len(recent_distress)-1)):
                patterns.append("escalating_distress")
        
        # Check for extreme fear or sadness
        extreme_emotions = sum(1 for r in results 
                              if r['emotions'].get('fear', 0) > 0.8 or 
                              r['emotions'].get('sadness', 0) > 0.8)
        if extreme_emotions > 0:
            patterns.append("extreme_emotional_distress")
        
        return patterns
    
    @staticmethod
    def _aggregate_mental_health_risk(results):
        """Calculate overall mental health risk"""
        avg_net_score = sum(r['mental_health_risk']['net_score'] for r in results) / len(results)
        
        if avg_net_score < 0.3:
            return "LOW"
        elif avg_net_score < 0.6:
            return "MEDIUM"
        elif avg_net_score < 0.9:
            return "HIGH"
        else:
            return "CRITICAL"
    
    @staticmethod
    def _get_recommendation(patterns, high_risk_count, total_count):
        """Get recommendation based on analysis"""
        if "extreme_emotional_distress" in patterns or high_risk_count > total_count * 0.5:
            return "URGENT: Consider reaching out to a mental health professional or crisis helpline immediately."
        elif "escalating_distress" in patterns:
            return "WARNING: Emotional distress appears to be escalating. Consider seeking support."
        elif "persistent_negative_emotions" in patterns:
            return "NOTICE: Persistent negative emotions detected. Consider talking to someone you trust."
        else:
            return "MONITOR: Continue to monitor emotional wellbeing."


# Initialize global detector instance
emotion_detector = EmotionDetector()


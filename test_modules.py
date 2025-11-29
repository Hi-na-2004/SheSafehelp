"""
Test script for SheSafe application
Run this to verify all modules are working
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_toxicity_module():
    """Test toxicity detection module"""
    print("\n🧪 Testing Toxicity Detection Module...")
    try:
        from modules.toxicity_detector import toxicity_detector
        
        test_text = "This is a test message"
        result = toxicity_detector.analyze_text(test_text)
        
        if 'scores' in result:
            print("✅ Toxicity detection working!")
            print(f"   Sample score: {result['max_score']:.3f}")
            return True
        else:
            print("❌ Unexpected result format")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_emotion_module():
    """Test emotion detection module"""
    print("\n🧪 Testing Emotion Detection Module...")
    try:
        from modules.emotion_detector import emotion_detector
        
        test_text = "I am feeling happy today"
        result = emotion_detector.analyze_emotion(test_text)
        
        if 'emotions' in result:
            print("✅ Emotion detection working!")
            print(f"   Dominant emotion: {result['dominant_emotion']['name']}")
            return True
        else:
            print("❌ Unexpected result format")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_safety_module():
    """Test safety scoring module"""
    print("\n🧪 Testing Safety Scoring Module...")
    try:
        from modules.safety_scorer import safety_scorer
        
        # Test with sample coordinates (New Delhi, India)
        result = safety_scorer.get_location_safety_score(28.6139, 77.2090)
        
        if 'safety_score' in result:
            print("✅ Safety scoring working!")
            print(f"   Safety score: {result['safety_score']:.1f}/100")
            return True
        else:
            print("❌ Unexpected result format")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_sos_module():
    """Test SOS system module"""
    print("\n🧪 Testing SOS System Module...")
    try:
        from modules.sos_system import sos_system
        
        print("✅ SOS system initialized!")
        print(f"   Twilio configured: {sos_system.client is not None}")
        print(f"   Emergency contacts: {len(sos_system.emergency_contacts)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 60)
    print("🛡️  SheSafe - Module Testing")
    print("=" * 60)
    
    results = []
    
    # Test all modules
    results.append(("Toxicity Detection", test_toxicity_module()))
    results.append(("Emotion Detection", test_emotion_module()))
    results.append(("Safety Scoring", test_safety_module()))
    results.append(("SOS System", test_sos_module()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{name:25} {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} modules working")
    
    if passed == total:
        print("\n🎉 All modules are working correctly!")
    else:
        print("\n⚠️  Some modules need attention. Check errors above.")
    
    print("\n💡 Tip: First run may be slow as models are being downloaded")
    print("=" * 60)

if __name__ == "__main__":
    main()


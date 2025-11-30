"""
SafeCircle - Women Safety & Support Platform
Main Flask Application with 4 Core Modules
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Import routes
from routes.toxicity_routes import toxicity_bp
from routes.emotion_routes import emotion_bp
from routes.safety_routes import safety_bp
from routes.sos_routes import sos_bp

# Register blueprints
app.register_blueprint(toxicity_bp, url_prefix='/api/toxicity')
app.register_blueprint(emotion_bp, url_prefix='/api/emotion')
app.register_blueprint(safety_bp, url_prefix='/api/safety')
app.register_blueprint(sos_bp, url_prefix='/api/sos')


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'modules': {
            'toxicity_detection': 'active',
            'emotion_analysis': 'active',
            'safety_scoring': 'active',
            'sos_system': 'active'
        }
    })


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection for real-time alerts"""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print('Client disconnected')


if __name__ == '__main__':
    print("🚀 Starting SheSafe Application...")
    print("📍 Access the application at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)


from flask import Flask, jsonify, request
from decouple import config
from openai import OpenAI
import os
from routes.ai_routes import ai_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(ai_bp, url_prefix='/api/ai')

# Initialize OpenAI client
client = OpenAI()  # It will automatically use OPENAI_API_KEY from environment

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Service is running"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001) 
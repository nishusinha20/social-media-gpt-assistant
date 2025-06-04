from flask import Blueprint, jsonify, request
from openai import OpenAI
from decouple import config

ai_bp = Blueprint('ai', __name__)
client = OpenAI()  # It will automatically use OPENAI_API_KEY from environment

PERSONALITY_PROMPT = """You are an expert social media manager. Create {num_questions} engaging questions to understand a person's interests, 
content style, and personality for social media content creation. Focus on questions that will help in creating authentic social media posts. 
Return only the questions in a clear, direct manner."""

CONTENT_GENERATION_PROMPT = """Based on the user's responses to our questions, create an engaging social media post that matches their style and interests.
The post should feel authentic and personal. Keep the tone consistent with their personality.
Consider the platform-specific constraints and best practices for {platform}.
"""

@ai_bp.route('/generate-questions', methods=['GET'])
def generate_questions():
    try:
        num_questions = request.args.get('num_questions', default=5, type=int)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": PERSONALITY_PROMPT.format(num_questions=num_questions)},
                {"role": "user", "content": "Generate engaging questions to understand user's social media personality"}
            ]
        )
        
        # Process the response into structured questions
        questions_text = response.choices[0].message.content.strip().split('\n')
        questions = [
            {
                "id": i + 1,
                "question": q.strip().lstrip('0123456789.- '),
                "answer": None
            }
            for i, q in enumerate(questions_text)
            if q.strip()
        ]
        
        return jsonify({"questions": questions}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/submit-responses', methods=['POST'])
def submit_responses():
    try:
        data = request.get_json()
        if not data or 'responses' not in data:
            return jsonify({"error": "Responses are required"}), 400
            
        # Store responses in memory (in a real application, you'd want to use a database)
        return jsonify({
            "message": "Responses collected successfully",
            "responses": data['responses']
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@ai_bp.route('/generate-content', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        if not data or 'responses' not in data or 'platform' not in data:
            return jsonify({"error": "Responses and platform are required"}), 400

        # Prepare user profile based on responses
        user_profile = "\n".join([
            f"Question: {response['question']}\nAnswer: {response['answer']}"
            for response in data['responses']
        ])

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": CONTENT_GENERATION_PROMPT.format(platform=data['platform'])},
                {"role": "user", "content": f"Based on this user profile, create an engaging social media post:\n\n{user_profile}"}
            ]
        )

        return jsonify({
            "content": response.choices[0].message.content,
            "platform": data['platform']
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 
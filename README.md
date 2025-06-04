# Social Media Content Bot

A Flask-based API that uses OpenAI's GPT to generate personalized social media content based on user preferences and style.

## Features

- Generate personalized questions to understand user's content style
- Submit user responses about content preferences
- Generate platform-specific social media content
- Health check endpoint

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd social-media-bot-be
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your_openai_api_key_here
```

5. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5001`

## API Endpoints

### Health Check
```bash
GET /health
```

### Generate Questions
```bash
GET /api/ai/generate-questions?num_questions=5
```

### Submit Responses
```bash
POST /api/ai/submit-responses
```

### Generate Content
```bash
POST /api/ai/generate-content
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key

## License

MIT 
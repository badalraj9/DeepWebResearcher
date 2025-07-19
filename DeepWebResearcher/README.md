# DeepWebResearcher Backend

A FastAPI backend for AI-powered research and content generation using OpenRouter and Tavily.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
Create a `.env` file in the DeepWebResearcher directory with:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

3. Get API Keys:
- **OpenRouter**: Sign up at https://openrouter.ai/ and get your API key
- **Tavily**: Sign up at https://tavily.com/ and get your API key

4. Run the server:
```bash
python app.py
```

The server will start on http://localhost:5000

## Features

- AI-powered research using OpenRouter (Claude 3.5 Sonnet)
- Web search using Tavily
- Fact-checking and verification
- Content generation in multiple styles
- Draft management and library system

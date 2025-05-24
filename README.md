# Workday AI Application Assistant

This application automates the process of filling out Workday job applications using AI. It analyzes your resume and job descriptions to create tailored applications.

## Features

- Resume parsing and analysis
- Job description analysis
- Automated Workday form filling
- AI-powered experience tailoring
- Secure credential management
- Support for multiple AI providers:
  - OpenAI (GPT-4/GPT-3.5)
  - Anthropic (Claude 3)
  - Google AI (Gemini Pro)
  - Hugging Face (Mixtral-8x7B)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your credentials:
```
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key

# Google AI
GOOGLE_API_KEY=your_google_api_key

# Hugging Face
HUGGINGFACE_TOKEN=your_huggingface_token

# Workday
WORKDAY_USERNAME=your_workday_username
WORKDAY_PASSWORD=your_workday_password
```

3. Run the application:
```bash
python main.py
```

## Usage

1. Upload your resume (PDF or DOCX format)
2. Provide the Workday job application URL
3. Provide the job description
4. (Optional) Specify the AI provider to use (defaults to OpenAI)
   - openai
   - anthropic
   - google
   - huggingface

The AI will analyze your resume and the job description, and the application will automatically fill out the Workday form with tailored responses.

## AI Provider Comparison

- **OpenAI (GPT-4)**
  - Pros: High quality responses, good at following instructions
  - Cons: Higher cost, token limits
  - Best for: High-quality, detailed analysis

- **Anthropic (Claude 3)**
  - Pros: Large context window, good at analysis
  - Cons: Higher cost than some alternatives
  - Best for: Complex analysis and matching

- **Google AI (Gemini Pro)**
  - Pros: Good performance, competitive pricing
  - Cons: Newer model, may have limitations
  - Best for: General purpose use

- **Hugging Face (Mixtral-8x7B)**
  - Pros: Free to use, runs locally
  - Cons: Requires more computational resources
  - Best for: Privacy-focused applications

## Security Note

This application stores credentials securely and does not share your information with third parties. All processing is done locally except for AI analysis which uses the selected AI provider's API.

## Requirements

- Python 3.8+
- Chrome browser (for Selenium automation)
- Internet connection
- API key for your chosen AI provider
- For Hugging Face: Sufficient GPU memory for local model execution 

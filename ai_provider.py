import requests
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

class AIProvider:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            'Content-Type': 'application/json'
        }

    def generate_response(self, prompt: str, system_prompt: str = None) -> str:
        # Combine system prompt and user prompt if system prompt exists
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": full_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            }
        }

        print("Sending request to Gemini API...")
        response = requests.post(
            f"{self.api_url}?key={self.api_key}",
            headers=self.headers,
            json=payload
        )

        if response.status_code != 200:
            print(f"API Error Response: {response.text}")
            raise Exception(f"Google AI API error: {response.text}")

        try:
            result = response.json()
            print("Received response from Gemini API")
            
            # Debug print the response
            print("Response structure:", result.keys())
            
            if 'candidates' not in result:
                print("No candidates in response:", result)
                raise Exception("No candidates in response")
                
            if not result['candidates']:
                print("Empty candidates list:", result)
                raise Exception("Empty candidates list")
                
            if 'content' not in result['candidates'][0]:
                print("No content in candidate:", result['candidates'][0])
                raise Exception("No content in candidate")
                
            if 'parts' not in result['candidates'][0]['content']:
                print("No parts in content:", result['candidates'][0]['content'])
                raise Exception("No parts in content")
                
            if not result['candidates'][0]['content']['parts']:
                print("Empty parts list:", result['candidates'][0]['content'])
                raise Exception("Empty parts list")
                
            if 'text' not in result['candidates'][0]['content']['parts'][0]:
                print("No text in part:", result['candidates'][0]['content']['parts'][0])
                raise Exception("No text in part")
            
            response_text = result['candidates'][0]['content']['parts'][0]['text']
            
            # Clean up the response text
            # Remove markdown code block markers if present
            response_text = response_text.replace('```json', '').replace('```', '').strip()
            
            print("Cleaned response text:", response_text[:100] + "..." if len(response_text) > 100 else response_text)
            
            return response_text
            
        except (KeyError, IndexError) as e:
            print("Error parsing response:", str(e))
            print("Full response:", result)
            raise Exception(f"Failed to parse Google AI response: {str(e)}")

def get_ai_provider(provider_name: str = "google") -> AIProvider:
    """Factory function to get the AI provider."""
    return AIProvider() 
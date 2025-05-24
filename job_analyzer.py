from typing import Dict, Any
import os
from dotenv import load_dotenv
from ai_provider import get_ai_provider

load_dotenv()

class JobAnalyzer:
    def __init__(self, ai_provider_name: str = "openai"):
        self.ai_provider = get_ai_provider(ai_provider_name)

    def analyze_job_description(self, job_description: str, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze job description and match it with resume data to create tailored responses."""
        prompt = f"""
        Analyze the following job description and resume data to create tailored responses for a Workday application.
        Focus on matching skills, experiences, and qualifications.

        Job Description:
        {job_description}

        Resume Data:
        {resume_data}

        Provide responses in JSON format with the following structure:
        {{
            "experience_matches": [
                {{
                    "job_requirement": "requirement from job description",
                    "matching_experience": "relevant experience from resume",
                    "tailored_response": "tailored response highlighting the match"
                }}
            ],
            "skill_matches": [
                {{
                    "required_skill": "skill from job description",
                    "matching_skill": "skill from resume",
                    "evidence": "example of skill usage from experience"
                }}
            ],
            "education_matches": [
                {{
                    "requirement": "education requirement from job description",
                    "qualification": "matching education from resume",
                    "relevance": "explanation of relevance"
                }}
            ],
            "additional_qualifications": [
                "list of additional qualifications from resume that could be relevant"
            ]
        }}
        """

        system_prompt = "You are an expert job application analyzer that matches resumes to job descriptions. Return the response in valid JSON format."

        return self.ai_provider.generate_response(prompt, system_prompt)

    def generate_application_responses(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Generate specific responses for Workday application fields based on the analysis."""
        prompt = f"""
        Based on the following analysis, generate specific responses for a Workday application form.
        Focus on creating concise, professional responses that highlight the best matches.

        Analysis:
        {analysis}

        Generate responses for the following fields:
        1. Summary of Qualifications
        2. Work Experience
        3. Education
        4. Skills
        5. Additional Information

        Format the response as a JSON object with these fields as keys.
        """

        system_prompt = "You are an expert at crafting professional job application responses. Return the response in valid JSON format."

        return self.ai_provider.generate_response(prompt, system_prompt) 
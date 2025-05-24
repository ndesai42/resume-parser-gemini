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
        Analyze the following job description and resume data to create tailored responses for a Workday powered job application.
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

    def tailor_bullet_points(self, job_description: str, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tailor bullet points to match job description while preserving core content."""
        prompt = f"""
        Analyze the following job description and resume data to tailor the bullet points for each work experience.
        Focus on making minor adjustments to emphasize relevant skills and experiences while preserving the core content and achievements.

        Job Description:
        {job_description}

        Resume Data:
        {resume_data}

        For each work experience, provide tailored bullet points that:
        1. Maintain the original achievements and metrics
        2. Slightly rephrase to emphasize skills mentioned in the job description
        3. Keep the same level of detail and specificity
        4. Don't add or remove any major responsibilities
        5. Don't change any dates, company names, or job titles

        Return the response in JSON format with the following structure:
        {{
            "tailored_experience": [
                {{
                    "company": "Company Name",
                    "title": "Job Title",
                    "dates": "Start Date - End Date",
                    "original_bullets": ["Original bullet 1", "Original bullet 2"],
                    "tailored_bullets": ["Tailored bullet 1", "Tailored bullet 2"]
                }}
            ]
        }}
        """

        system_prompt = "You are an expert at tailoring resume bullet points to match job descriptions while preserving the core content and achievements. Return the response in valid JSON format."

        return self.ai_provider.generate_response(prompt, system_prompt) 
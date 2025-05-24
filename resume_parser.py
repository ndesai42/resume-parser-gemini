import pdfplumber
from docx import Document
from typing import Dict, Any
import os
from dotenv import load_dotenv
from ai_provider import get_ai_provider

load_dotenv()

class ResumeParser:
    def __init__(self, ai_provider_name: str = "google"):
        self.ai_provider = get_ai_provider()

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse resume from PDF or DOCX file and extract structured information."""
        if file_path.endswith('.pdf'):
            text = self._extract_from_pdf(file_path)
        elif file_path.endswith(('.doc', '.docx')):
            text = self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Please use PDF or DOC/DOCX.")

        return self._analyze_resume(text)

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    def _analyze_resume(self, text: str) -> Dict[str, Any]:
        """Analyze resume text using AI to extract structured information."""
        prompt = f"""
        Analyze the following resume and extract information in the following JSON format:
        {{
            "personal_information": {{
                "name": "Full Name",
                "email": "email@example.com",
                "phone": "phone number",
                "location": "city, state"
            }},
            "work_experience": [
                {{
                    "company": "Company Name",
                    "title": "Job Title",
                    "dates": "Start Date - End Date",
                    "responsibilities": ["Responsibility 1", "Responsibility 2"]
                }}
            ],
            "education": [
                {{
                    "institution": "School Name",
                    "degree": "Degree Name",
                    "dates": "Start Date - End Date"
                }}
            ],
            "skills": ["Skill 1", "Skill 2"],
            "projects": [
                {{
                    "name": "Project Name",
                    "description": "Project Description"
                }}
            ],
            "certifications": ["Certification 1", "Certification 2"]
        }}

        Resume text:
        {text}

        Return ONLY the JSON object, with no additional text or explanation.
        """

        system_prompt = "You are a resume parser that extracts structured information from resumes. Return ONLY a valid JSON object matching the exact format specified, with no additional text or explanation."

        return self.ai_provider.generate_response(prompt, system_prompt) 
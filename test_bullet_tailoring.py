from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
import json

def main():
    # Initialize the parser and analyzer with Gemini provider
    parser = ResumeParser(ai_provider_name="google")
    analyzer = JobAnalyzer(ai_provider_name="google")
    
    try:
        # Parse the resume
        resume_path = "resume.pdf"  # Update this to your resume path
        resume_data = parser.parse_resume(resume_path)
        
        # Example job description (replace with actual job description)
        job_description = """
        We are seeking a Software Engineer with experience in Python development and AI integration.
        The ideal candidate should have:
        - Strong Python programming skills
        - Experience with AI/ML integration
        - Knowledge of web development frameworks
        - Experience with API development
        - Strong problem-solving abilities
        """
        
        # Get tailored bullet points
        tailored_bullets = analyzer.tailor_bullet_points(job_description, resume_data)
        
        # Print the results
        print("\nOriginal Resume Data:")
        print("=" * 50)
        print(json.dumps(resume_data, indent=2))
        
        print("\nTailored Bullet Points:")
        print("=" * 50)
        print(json.dumps(json.loads(tailored_bullets), indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 
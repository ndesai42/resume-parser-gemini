from resume_parser import ResumeParser
import json

def main():
    # Initialize the parser with Gemini provider
    parser = ResumeParser(ai_provider_name="google")
    
    try:
        # Parse the resume (replace with your resume path)
        resume_path = "~/Downloads/Neel_Desai (1).pdf"  # or "your_resume.docx"
        result = parser.parse_resume(resume_path)
        
        # Pretty print the result
        print("Parsed Resume Data:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 
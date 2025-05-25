from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
import json

def main():
    # Initialize the parser and analyzer with Gemini provider
    parser = ResumeParser(ai_provider_name="google")
    analyzer = JobAnalyzer(ai_provider_name="google")
    
    try:
        # Parse the resume
        resume_path = "resume.pdf"
        print(f"Parsing resume: {resume_path}")
        resume_data = parser.parse_resume(resume_path)
        
        # Example job description for a Software Engineering role
        job_description = """
        Company Overview:

First Rounds on Me is a revolutionary dating app designed for modern singles who are tired of the frustrations of today's dating scene. The app focuses on helping users plan dates and build genuine connections by requiring them to match with others by planning a date with a date, time, and location. It allows users to chat with their date only 24 hours before the date, encouraging "getting to know each other" in real life (IRL). The founder, Joe Feminella, describes the app as a transformative movement redefining connection, aiming to cultivate a community where people embrace diversity and genuine connections over the 'like-minded' criteria.


First Round’s on Me is an equal opportunity employer. We celebrate diversity and are committed to creating an inclusive environment for all employees.


Locations: New York, NY, Los Angeles, CA, Austin, TX, Boston, MA, Remote



Position Overview: 

We are looking for a Software Engineering Intern (Python/Django) to join our technology team for a 3-month internship. You’ll help us build and scale real-world backend systems that power our dating platform. This is a hands-on role where you’ll gain experience working on production systems, writing scalable code, and contributing meaningfully to a fast-moving startup. High performers may be considered for co-op extensions or full-time roles.


Responsibilities:

Develop and maintain backend services and APIs using Python and Django.
Collaborate with frontend and mobile engineers to ensure seamless integrations.
Write clean, maintainable, and efficient code.
Participate in pair programming, code reviews, and agile standups.
Contribute to the scalability, reliability, and security of our backend architecture.
Engage in real-world problem solving and system design discussions.


Qualifications:

Pursuing or recently completed a Bachelor's or Master's in Computer Science, Engineering, or related field and work experience.
Proficient in Python and Django.
Understanding of web application architecture, REST APIs, and databases.
Strong communication skills and a passion for building user-focused tech.
Bonus points for familiarity with Docker, AWS, PostgreSQL, and CI/CD tools.
Extra love if you've built something live, contributed to open source, or dabbled in React Native.

        """
        
        print("\nAnalyzing job description and tailoring bullet points...")
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
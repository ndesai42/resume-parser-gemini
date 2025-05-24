import os
from resume_parser import ResumeParser
import json
from dotenv import load_dotenv
import urllib.parse

def parse_resume_file(file_path):
    # Load environment variables
    load_dotenv()
    
    # Initialize parser with Gemini
    parser = ResumeParser(ai_provider_name="google")
    
    try:
        # Clean up the file path and handle special characters
        file_path = file_path.strip().strip('"').strip("'")
        file_path = file_path.replace('\\', '')  # Remove any escape characters
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            print("Current working directory:", os.getcwd())
            print("\nFiles in Downloads directory:")
            downloads_dir = os.path.expanduser("~/Downloads")
            for file in os.listdir(downloads_dir):
                if file.lower().endswith(('.pdf', '.doc', '.docx')):
                    print(f"- {file}")
            return
        
        # Check file extension
        if not file_path.lower().endswith(('.pdf', '.doc', '.docx')):
            print("Error: Only PDF, DOC, and DOCX files are supported")
            return
        
        print(f"Parsing resume: {file_path}")
        print("This may take a few moments...")
        
        # Parse the resume
        result = parser.parse_resume(file_path)
        
        # Print the results in a formatted way
        print("\nParsed Resume Data:")
        print("=" * 50)
        
        # Parse the JSON string into a dictionary
        parsed_data = json.loads(result)
        
        # Print each section
        for section, data in parsed_data.items():
            print(f"\n{section.upper().replace('_', ' ')}:")
            print("-" * 30)
            if isinstance(data, list):
                for item in data:
                    print(json.dumps(item, indent=2))
            else:
                print(json.dumps(data, indent=2))
        
        # Save the parsed data to a JSON file
        output_file = f"parsed_resume_{os.path.splitext(os.path.basename(file_path))[0]}.json"
        with open(output_file, 'w') as f:
            json.dump(parsed_data, f, indent=2)
        print(f"\nParsed data saved to: {output_file}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        print("Full error traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    # Get the resume file path from user input
    print("Please enter the path to your resume file (PDF, DOC, or DOCX)")
    print("Example: ~/Downloads/My Resume.pdf")
    print("\nAvailable files in Downloads:")
    downloads_dir = os.path.expanduser("~/Downloads")
    for file in os.listdir(downloads_dir):
        if file.lower().endswith(('.pdf', '.doc', '.docx')):
            print(f"- {file}")
    
    print("\nEnter the filename from the list above:")
    file_name = input("Filename: ").strip()
    
    # Construct the full path
    file_path = os.path.join(downloads_dir, file_name)
    
    parse_resume_file(file_path) 
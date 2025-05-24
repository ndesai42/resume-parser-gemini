import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from workday_automator import WorkdayAutomator
import json
from typing import Optional
import uvicorn

app = FastAPI(title="Workday AI Application Assistant")

@app.post("/apply")
async def apply_for_job(
    resume: UploadFile = File(...),
    job_url: str = Form(...),
    job_description: str = Form(...),
    ai_provider: str = Form("openai")  # Default to OpenAI
):
    try:
        # Save uploaded resume
        resume_path = f"temp_{resume.filename}"
        with open(resume_path, "wb") as f:
            f.write(await resume.read())

        # Parse resume
        parser = ResumeParser(ai_provider_name=ai_provider)
        resume_data = parser.parse_resume(resume_path)

        # Analyze job and generate responses
        analyzer = JobAnalyzer(ai_provider_name=ai_provider)
        
        # First, get tailored bullet points
        tailored_bullets = analyzer.tailor_bullet_points(job_description, resume_data)
        
        # Update resume data with tailored bullets
        tailored_data = json.loads(tailored_bullets)
        for exp in tailored_data["tailored_experience"]:
            for resume_exp in resume_data["work_experience"]:
                if exp["company"] == resume_exp["company"] and exp["title"] == resume_exp["title"]:
                    resume_exp["responsibilities"] = exp["tailored_bullets"]
        
        # Now analyze the job with the tailored resume
        analysis = analyzer.analyze_job_description(job_description, resume_data)
        application_responses = analyzer.generate_application_responses(analysis)

        # Initialize Workday automation
        automator = WorkdayAutomator()
        automator.initialize_driver()

        try:
            # Login and fill application
            automator.login(job_url)
            automator.fill_application_form(json.loads(application_responses))
            automator.submit_application()

            return JSONResponse({
                "status": "success",
                "message": "Application submitted successfully",
                "tailored_bullets": tailored_data
            })

        finally:
            # Clean up
            automator.close()
            os.remove(resume_path)

    except Exception as e:
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
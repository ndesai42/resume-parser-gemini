import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from workday_automator import WorkdayAutomator
import json
from typing import Optional
import uvicorn
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Workday AI Application Assistant")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    logger.info("Serving index.html")
    return FileResponse("static/index.html")

@app.post("/parse-resume")
async def parse_resume(resume: UploadFile = File(...)):
    try:
        logger.info(f"Received resume file: {resume.filename}")
        
        # Save uploaded resume
        resume_path = f"temp_{resume.filename}"
        with open(resume_path, "wb") as f:
            f.write(await resume.read())
        logger.info(f"Saved resume to: {resume_path}")

        # Parse resume
        logger.info("Starting resume parsing")
        parser = ResumeParser(ai_provider_name="google")
        resume_data = parser.parse_resume(resume_path)
        logger.info("Resume parsing completed")

        # Clean up
        os.remove(resume_path)
        logger.info("Temporary file removed")

        return JSONResponse(resume_data)

    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        return JSONResponse({
            "status": "error",
            "message": str(e)
        }, status_code=500)

@app.post("/apply")
async def apply_for_job(
    resume: UploadFile = File(...),
    job_url: str = Form(""),
    job_description: str = Form(...),
    ai_provider: str = Form("openai")
):
    try:
        logger.info(f"Received resume file: {resume.filename}")
        logger.info(f"Job description: {job_description[:100]}...")
        logger.info(f"AI provider: {ai_provider}")
        # Save resume to temp file
        temp_filename = f"temp_{resume.filename}"
        with open(temp_filename, "wb") as f:
            f.write(await resume.read())
        logger.info(f"Saved resume to: {temp_filename}")
        # Parse resume
        parser = ResumeParser(ai_provider_name=ai_provider)
        parsed_resume = parser.parse_resume(temp_filename)
        logger.info(f"Type of parsed_resume: {type(parsed_resume)}")
        logger.info(f"Content of parsed_resume: {json.dumps(parsed_resume)[:500]}")
        # Analyze job
        analyzer = JobAnalyzer(ai_provider_name=ai_provider)
        tailored_bullets = analyzer.tailor_bullet_points(job_description, parsed_resume)
        logger.info(f"Type of tailored_bullets: {type(tailored_bullets)}")
        logger.info(f"Content of tailored_bullets: {json.dumps(tailored_bullets)[:500]}")
        logger.error(f"Raw tailored_bullets string: {tailored_bullets}")
        # Remove temp file
        os.remove(temp_filename)
        if isinstance(tailored_bullets, str):
            # Remove trailing commas before closing braces/brackets
            tailored_bullets = re.sub(r',([ \t\r\n]+[}\]])', r'\1', tailored_bullets)
            tailored_bullets = json.loads(tailored_bullets)
        return {"tailored_bullets": tailored_bullets}
    except Exception as e:
        logger.error(f"Error in /apply: {e}", exc_info=True)
        return {"error": f"Failed to analyze resume: {str(e)}"}

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    ) 
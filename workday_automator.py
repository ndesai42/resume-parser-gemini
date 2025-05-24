from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from dotenv import load_dotenv
import time
from typing import Dict, Any

load_dotenv()

class WorkdayAutomator:
    def __init__(self):
        self.driver = None
        self.wait = None

    def initialize_driver(self):
        """Initialize the Chrome WebDriver with appropriate options."""
        options = webdriver.ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, url: str):
        """Login to Workday using credentials from environment variables."""
        self.driver.get(url)
        
        # Wait for login form and input credentials
        username = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password = self.driver.find_element(By.ID, "password")
        
        username.send_keys(os.getenv("WORKDAY_USERNAME"))
        password.send_keys(os.getenv("WORKDAY_PASSWORD"))
        
        # Click login button
        login_button = self.driver.find_element(By.ID, "submit")
        login_button.click()

    def fill_application_form(self, application_data: Dict[str, Any]):
        """Fill out the Workday application form with the provided data."""
        try:
            # Wait for the application form to load
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "application-form")))

            # Fill personal information
            self._fill_personal_info(application_data.get("personal_info", {}))

            # Fill work experience
            self._fill_work_experience(application_data.get("work_experience", []))

            # Fill education
            self._fill_education(application_data.get("education", []))

            # Fill skills
            self._fill_skills(application_data.get("skills", []))

            # Fill additional information
            self._fill_additional_info(application_data.get("additional_info", {}))

        except TimeoutException:
            print("Timeout waiting for form elements")
            raise

    def _fill_personal_info(self, personal_info: Dict[str, str]):
        """Fill personal information section."""
        for field, value in personal_info.items():
            try:
                element = self.wait.until(EC.presence_of_element_located((By.NAME, field)))
                element.clear()
                element.send_keys(value)
            except TimeoutException:
                print(f"Could not find field: {field}")

    def _fill_work_experience(self, experiences: list):
        """Fill work experience section."""
        for exp in experiences:
            try:
                # Click add experience button
                add_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-experience")))
                add_button.click()

                # Fill experience fields
                for field, value in exp.items():
                    element = self.wait.until(EC.presence_of_element_located((By.NAME, field)))
                    element.clear()
                    element.send_keys(value)

                # Save experience
                save_button = self.driver.find_element(By.CLASS_NAME, "save-experience")
                save_button.click()
                time.sleep(1)  # Wait for save to complete

            except TimeoutException:
                print(f"Could not add experience: {exp.get('company', 'Unknown')}")

    def _fill_education(self, education: list):
        """Fill education section."""
        for edu in education:
            try:
                # Click add education button
                add_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-education")))
                add_button.click()

                # Fill education fields
                for field, value in edu.items():
                    element = self.wait.until(EC.presence_of_element_located((By.NAME, field)))
                    element.clear()
                    element.send_keys(value)

                # Save education
                save_button = self.driver.find_element(By.CLASS_NAME, "save-education")
                save_button.click()
                time.sleep(1)  # Wait for save to complete

            except TimeoutException:
                print(f"Could not add education: {edu.get('institution', 'Unknown')}")

    def _fill_skills(self, skills: list):
        """Fill skills section."""
        try:
            skills_field = self.wait.until(EC.presence_of_element_located((By.NAME, "skills")))
            skills_field.clear()
            skills_field.send_keys(", ".join(skills))
        except TimeoutException:
            print("Could not find skills field")

    def _fill_additional_info(self, additional_info: Dict[str, str]):
        """Fill additional information section."""
        for field, value in additional_info.items():
            try:
                element = self.wait.until(EC.presence_of_element_located((By.NAME, field)))
                element.clear()
                element.send_keys(value)
            except TimeoutException:
                print(f"Could not find field: {field}")

    def submit_application(self):
        """Submit the completed application."""
        try:
            submit_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-application")))
            submit_button.click()
            
            # Wait for confirmation
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "application-submitted")))
            print("Application submitted successfully!")
        except TimeoutException:
            print("Could not submit application")

    def close(self):
        """Close the browser and clean up."""
        if self.driver:
            self.driver.quit() 
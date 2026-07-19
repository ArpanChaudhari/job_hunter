import requests  # type: ignore
import json
from src.matcher import get_missing_skills
from src.process_resume import clean_text , extract_text_from_pdf , extract_keywords


def generate_cover_letter(prompt, model="llama3.2:3b"):
    # hitting the local ollama API so my resume data stays private!
    url = "http://localhost:11434/api/generate"

    # This is the data we are sending to ollama
    payload = {"model": model, "prompt": prompt, "stream": False}

    # We send the request and grab the response
    response = requests.post(url, json=payload)
    data = response.json()  # Convert the JSON text into Python dictionary

    return data["response"]


def create_prompt(resume_text, job_desc, missing_skills):
    system_prompt = f"""
    You are an expert cover letter writer and ATS specialist.

    Using the candidate's `{resume_text}`, the target `{job_desc}`, and identified `{missing_skills}`, 
    generate a professional, personalized, and job-specific cover letter.

    Match the candidate's experience, projects, and skills with the job requirements. 
    If skills are missing, emphasize transferable skills, adaptability, and willingness to learn instead of mentioning deficiencies.

    Do not invent experiences, achievements, or skills not present in the resume.

    Return only the final cover letter in a professional tone, tailored to the specific role and company.
    """
    return system_prompt


# Entry point of the program
if __name__ == "__main__":
    
    resume_path = "resume.pdf" # path to the resume pdf file
    job_desc_path = "job_description.txt" # path to the job description text file

    # extract and clean resume text
    resume_text = extract_text_from_pdf(resume_path)
    cleaned_resume_text = clean_text(resume_text)

    # read and clean job description text
    with open(job_desc_path, "r") as f:
        job_desc = f.read()
    cleaned_job_desc = clean_text(job_desc)

    # Identify skills present in JD but missing from resume
    missing_skill = get_missing_skills(cleaned_resume_text, cleaned_job_desc)

    # Prompt Creation
    final_prompt = create_prompt(cleaned_resume_text,cleaned_job_desc,missing_skill)
    
    # Generate cover letter using local Ollama model
    cover_letter = generate_cover_letter(final_prompt)

    # Display generated cover letter
    print(cover_letter)



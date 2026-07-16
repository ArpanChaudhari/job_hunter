from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore # convert text to numerical features using TF-IDF
from sklearn.metrics.pairwise import cosine_similarity  # type: ignore # compute cosine similarity between vectors

from process_resume import (
    extract_text_from_pdf,
    clean_text,
    extract_keywords,
)  # import functions from process_resume.py


def calculate_match_score(resume_text, job_desc):
    vectorizer = TfidfVectorizer(stop_words="english")  # initialize TF-IDF vectorizer

    tfidf_matrix = vectorizer.fit_transform(
        [resume_text, job_desc]
    )  # fit and transform both resume and job description into TF-IDF vectors

    match = cosine_similarity(
        tfidf_matrix[0:1], tfidf_matrix[1:2]
    )  # compute cosine similarity between resume and job description

    match_score = match[0][0] * 100  # convert similarity score to percentage

    return round(match_score, 2)  # round the score to 2 decimal places


def get_missing_skills(resume_text, job_desc):
    resume_keywords = set(extract_keywords(resume_text))  # extract keywords from resume
    job_desc_keywords = set(
        extract_keywords(job_desc)
    )  # extract keywords from job description

    missing_skills = (
        job_desc_keywords - resume_keywords
    )  # find skills in job description not in resume

    return list(missing_skills)  # return the missing skills as a list of strings


if __name__ == "__main__":
    resume_path = "resume.pdf"  # path to the resume pdf file
    job_desc_path = "job_description.txt"  # path to the job description text file

    # extract and clean resume text
    resume_text = extract_text_from_pdf(resume_path)
    cleaned_resume_text = clean_text(resume_text)

    # read and clean job description text
    with open(job_desc_path, "r") as f:
        job_desc = f.read()
    cleaned_job_desc = clean_text(job_desc)

    # calculate match score
    match_score = calculate_match_score(cleaned_resume_text, cleaned_job_desc)

    # get missing skills
    missing_skills = get_missing_skills(cleaned_resume_text, cleaned_job_desc)

    print(f"Match Score: {match_score}%")
    print(f"Missing Skills: {missing_skills}")

# JobHunter: AI-Powered Cover Letter Maker

**🚀 Live App:** [https://job-hunter-app.streamlit.app/](https://job-hunter-app.streamlit.app/)

![JobHunter Banner](images/logo.png)

JobHunter is a premium, beautifully designed Streamlit application that generates highly personalized cover letters by analyzing your resume against a specific job description. It uses Machine Learning to score your resume and leverages ultra-fast AI (via Groq API) to write the perfect cover letter.

## Features

- **ML-Powered Matching:** Calculates an exact Match Score between your resume and the job description using TF-IDF and Cosine Similarity.
- **Skill Gap Analysis:** Automatically extracts and identifies critical missing skills from the job description so the AI can address them gracefully.
- **Lightning Fast AI Generation:** Integrates with the Groq API (using Llama 3 models) to craft highly personalized cover letters in mere seconds.
- **Premium UI:** A highly polished, responsive, dark-mode interface built with custom CSS, avoiding the "standard" Streamlit look.
- **Native PDF Parsing:** Accurately extracts and cleans text directly from your uploaded PDF or Word resumes.

## Tech Stack

- **Frontend:** Streamlit, Custom CSS
- **Machine Learning:** Scikit-learn (`TfidfVectorizer`, `cosine_similarity`)
- **Natural Language Processing:** NLTK, pdfplumber
- **Generative AI:** Groq API (Llama 3.1 8B)

## Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/job-hunter.git
cd job-hunter
```

**2. Create a virtual environment**
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up your Groq API Key**
- Create a `.streamlit/secrets.toml` file in the root directory.
- Add your Groq API key to the file:
```toml
GROQ_API_KEY = "your_api_key_here"
```

**5. Run the Application**
```bash
streamlit run app.py
```

## Screenshots
![App Interface](images/screenshot.png)

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## License
This project is licensed under the MIT License.

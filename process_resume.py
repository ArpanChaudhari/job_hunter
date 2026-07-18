import pdfplumber  # type: ignore # read pdf files
import re  # regular expressions
from sklearn.feature_extraction.text import CountVectorizer  # type: ignore # convert text to numerical features


# function to extract text from pdf file
def extract_text_from_pdf(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
        return text


def clean_text(text):
    if not text:
        return ""
    # convert the text to lowercase
    text = text.lower()

    # remove special characters ( keeping alphanumeric, spaces, and common tech symbols like #, +, -)
    text = re.sub(r"[^a-z0-9\s#\+\-\.]", " ", text)

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_keywords(text):
    if not text.strip():
        return []  # Return empty if there is no text at all

    try:
        vectorizer = CountVectorizer(
            stop_words="english", ngram_range=(1, 2)
        )  # consider unigrams and bigrams

        vectorizer.fit_transform([text])  # fit and transform the text
        # fit_transform learn all unique words in the text and transform the text into numerical features (bag of words representation)

        return vectorizer.get_feature_names_out() # return the extracted keywords as a list of strings
    
    except ValueError:
        # If the vocabulary is completely empty after removing stop words, catch the error
        return []


# main function to test the code
# __name == "__main__" is common python idiom to check if the script is being run directly or imported as a module
if __name__ == "__main__":

    pdf_path = "resume.pdf"  # path to the pdf file

    # call the function to extract text from pdf
    extracted_text = extract_text_from_pdf(pdf_path)

    # call the function to clean the extracted text
    cleaned_text = clean_text(extracted_text)

    # call the function to extract keywords
    keywords = extract_keywords(cleaned_text)

    print("Cleaned Text:")
    print(cleaned_text)
    print("\nExtracted Keywords:")
    print(keywords)

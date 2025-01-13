from flask import Blueprint, jsonify, request
import os
from werkzeug.utils import secure_filename
import spacy
import PyPDF2
from groq import Groq 
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.utils import get_stop_words

cvAPI = Blueprint("api", __name__)
nlp = spacy.load("en_core_web_sm")

UPLOAD_FOLDER_FILES = "public/assets/cv"
if not os.path.exists(UPLOAD_FOLDER_FILES):
    os.makedirs(UPLOAD_FOLDER_FILES)

groq = Groq(api_key="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")

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    try:
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + " "
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

def summarize_text(text):
    """Summarize text to fit within the specified word count."""
    try:
        print("\n\n\nSummarizing text:", text)
        
        parser = PlaintextParser.from_string(text, PlaintextParser.from_string(text, get_stop_words("english")))
        summarizer = LsaSummarizer() 
        summary = summarizer(parser.document, sentences_count=5) 
        summarized = " ".join(str(sentence) for sentence in summary)
        
        return summarized
    
    except Exception as e:
        return text

def check_cv():
    try:
        data = request.form
        cv = request.files.get("cv")
        job_description = data.get("requirements")

        if not cv or not job_description:
            return jsonify({"error": "CV file and job description are required."}), 400

        cv_filename = secure_filename(cv.filename)
        upload_path = os.path.join(UPLOAD_FOLDER_FILES, cv_filename)
        cv.save(upload_path)

        cv_text = extract_text_from_pdf(upload_path)
        if len(cv_text.split()) > 1000:
            print("\n\nlen(cv_text.split()):", len(cv_text.split()))
            cv_text = summarize_text(cv_text)

        if len(job_description.split()) > 600:
            job_description = summarize_text(job_description)

        response = groq.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    Analyze the following CV content and job description. 
                    1. Provide a one-word rating (Not Good, Good, Best) based on how well the CV matches the job description.
                    2. Suggestions for improvements to make the CV better match the job description.
                    3. List what matches and what does not match in separate paragraphs.
                    4. Response must be with proper heaadings and with complete details.
                    5. Whenever you provide points or list make it must be with the number like 1, 2, 3, etc.
                    6. Do not provide any other response than the mentioned above.
                    7. You Only Cover these headings Rating, Suggestions for Improvements, What Matches and What Doesn't Match, Matches, Non-Matches, Overall Analysis

                    CV Content: "{cv_text}"
                    Job Description: "{job_description}"
                    """
                }
            ],
            model="llama3-8b-8192"
        )

        groq_result = response.choices[0].message.content

        # Add line breaks wherever there's a new line
        formatted_result = groq_result.replace("\n", "<br />")

        # Example of adding bold formatting where necessary
        # If you need to bold specific parts (e.g., headings, ratings, etc.)
        formatted_result = formatted_result.replace("**Rating:**", "<strong>Rating:</strong>")
        formatted_result = formatted_result.replace("**Suggestions for improvements:**", "<strong>Suggestions for improvements:</strong>")
        formatted_result = formatted_result.replace("**What matches and what does not:**", "<strong>What matches and what does not:</strong>")
        formatted_result = formatted_result.replace("**What matches:**", "<strong>What matches:</strong>")
        formatted_result = formatted_result.replace("**What does not match:**", "<strong>What does not match:</strong>")
        formatted_result = formatted_result.replace("**Additional comments:**", "<strong>Additional comments:</strong>")
        formatted_result = formatted_result.replace("**Suggestions for Improvements:**", "<strong>Suggestions for improvements:</strong>")
        formatted_result = formatted_result.replace("**suggestions for Improvement:**", "<strong>Suggestions for improvements:</strong>")
        formatted_result = formatted_result.replace("**suggestions for improvement:**", "<strong>Suggestions for improvements:</strong>")
        formatted_result = formatted_result.replace("**Matches and Non-Matches:**", "<strong>Matches and Non-Matches:</strong>")
        formatted_result = formatted_result.replace("**Matches:**", "<strong>Matches:</strong>")
        formatted_result = formatted_result.replace("**Non-Matches:**", "<strong>Non-Matches:</strong>")
        formatted_result = formatted_result.replace("**Overall Analysis:**", "<strong>Overall Analysis:</strong>")
        formatted_result = formatted_result.replace("**Conclusion:**", "<strong>Conclusion:</strong>")
        formatted_result = formatted_result.replace("**Does Not Match:**", "<strong>Does Not Match:</strong>")
        formatted_result = formatted_result.replace("**Projects Relevant to the Job Description:**", "<strong>Projects Relevant to the Job Description:</strong>")
        formatted_result = formatted_result.replace("**What Matches and What Does Not Match:**", "<strong>What Matches and What Does Not Match:</strong>")
        formatted_result = formatted_result.replace("**Overall Analysis:**", "<strong>Overall Analysis:</strong>")
        formatted_result = formatted_result.replace("**What Matches and What Doesn't Match:**", "<strong>What Matches and What Doesn't Match:</strong>")
        formatted_result = formatted_result.replace("**Doesn't Match:**", "<strong>Doesn't Match:</strong>")

        # Output formatted result for debugging
        print("\n\ngroq_result:", formatted_result)

        if not groq_result:
            raise ValueError("Invalid response from Groq API")

        return jsonify({'message': 'Cv Matched Successfully', 'status': 200, 'data': formatted_result})

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

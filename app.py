import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
import PyPDF2

# ==============================
# CONFIG
# ==============================
# Ensure the upload folder exists for temporary processing
import tempfile
UPLOAD_FOLDER = tempfile.gettempdir()

# Load environment variables from .env if present (robust fallback)
if os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() and not line.strip().startswith("#"):
                    parts = line.strip().split("=", 1)
                    if len(parts) == 2:
                        os.environ[parts[0].strip()] = parts[1].strip()
    except Exception as e:
        print(f"Error loading .env file: {e}")

# Retrieve Gemini API key from environment
apiKey = os.environ.get("GEMINI_API_KEY")
if not apiKey:
    print("Warning: GEMINI_API_KEY environment variable is not set!")

client = genai.Client(api_key=apiKey)

app = Flask(__name__)
# Enable CORS so the browser (frontend) can talk to this server without security blocks
CORS(app) 
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==============================
# PDF PARSING
# ==============================
def extract_text_from_pdf(pdf_path):
    """Parses PDF content into raw text."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"PDF Error: {e}")
    return text


# ==============================
# AI LOGIC
# ==============================
# ==============================
# AI LOGIC
# ==============================
def parse_resume(resume_text):
    """Extracts key info from the resume using AI."""
    prompt = f"Extract Skills, Experience, and Education from this resume in bullet points:\n{resume_text}"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

def parse_job_description(jd_text):
    """Extracts requirements from the JD using AI."""
    prompt = f"Extract Required Skills and Qualifications from this Job Description:\n{jd_text}"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text

def get_final_json_analysis(parsed_resume, parsed_jd):
    """Aggregates data into the specific JSON format the Scoreboard UI requires."""
    prompt = f"""
    Based on the parsed Resume and Job Description below, generate a final ATS evaluation.
    
    Resume Info: {parsed_resume}
    JD Info: {parsed_jd}

    Return ONLY a JSON object with this exact structure:
    {{
      "score": (integer 0-100),
      "feedbackSummary": "A one-paragraph overall summary of the candidate's performance and suitability for the role.",
      "matchedSkills": ["Skill 1", "Skill 2", "Skill 3"],
      "missingSkills": ["Skill 1", "Skill 2", "Skill 3"],
      "developmentPlan": ["Step 1", "Step 2", "Step 3"]
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    return response.text

# ==============================
# ROUTES (Connecting Frontend & Backend)
# ==============================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    The Bridge: Receives the FormData from the frontend 'fetch' call.
    Expects: 'resume' (PDF file) OR 'resume_text' (string)
    and 'job_description' (string).
    """
    resume_text = ""

    # 1. Get Resume Content (Plain Text or PDF File)
    if "resume_text" in request.form and request.form.get("resume_text").strip():
        resume_text = request.form.get("resume_text")
    elif "resume" in request.files:
        resume_file = request.files["resume"]
        if resume_file.filename != '':
            filename = f"temp_{resume_file.filename}"
            pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume_file.save(pdf_path)
            
            # Extract PDF or Text file
            if resume_file.filename.lower().endswith(".pdf"):
                resume_text = extract_text_from_pdf(pdf_path)
            else:
                try:
                    with open(pdf_path, "r", encoding="utf-8", errors="ignore") as f:
                        resume_text = f.read()
                except Exception as e:
                    print(f"Error reading uploaded file as text: {e}")

            # Cleanup
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

    if not resume_text or not resume_text.strip():
        return jsonify({"error": "Resume plain text or a PDF resume file is required"}), 400

    jd_text = request.form.get("job_description")
    if not jd_text or not jd_text.strip():
        return jsonify({"error": "Job description is required"}), 400

    try:
        # 2. Run AI Analysis
        parsed_resume = parse_resume(resume_text)
        parsed_jd = parse_job_description(jd_text)

        # 3. Format result for the Scoreboard UI
        final_analysis_raw = get_final_json_analysis(parsed_resume, parsed_jd)
        final_data = json.loads(final_analysis_raw)

        return jsonify(final_data)

    except Exception as e:
        print(f"Internal Error: {e}")
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    # Ensure port 8080 is used as per typical development environments
    app.run(debug=True, port=8080, host='0.0.0.0')
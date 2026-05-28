# ATS Resume Matcher

An AI-powered ATS Resume Matcher that analyzes resumes against job descriptions and provides an ATS compatibility score with improvement suggestions.

---

## Features

- ATS score calculation
- Resume and Job Description matching
- Keyword extraction
- Missing skills detection
- AI-powered suggestions
- PDF/DOCX support
- Simple and clean interface

---

## Tech Stack

- **Python**
- **Flask**
- **Gemini API**
- **PyPDF2**
- **Tailwind CSS & React** (Frontend)

---

## Project Structure

```
MatchMyResume/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
│
├── uploads/
│
└── templates/
    └── index.html
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/mythili7605/MatchMyResume.git
cd MatchMyResume
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**
```powershell
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file in the root directory.

```env
GEMINI_API_KEY=your_api_key_here
```

---

### Run the Application

```bash
python app.py
```
*The application will start on `http://localhost:8080`*

---

## Example Workflow

1. **Define Your Role:** Specify your target job role and highest qualification.
2. **Upload Resume:** Provide your resume in PDF/text format (or edit the preview).
3. **Analyze:** Click 'Analyze & Score Match'.
4. **Review Results:** View your ATS score, matched strengths, critical skill gaps, and a personalized career roadmap.

---

## Future Improvements

- Resume ranking system
- AI-generated interview questions
- Resume rewriting suggestions
- LinkedIn integration
- Job recommendations

---

## Screenshots



<img width="1877" height="906" alt="image" src="https://github.com/user-attachments/assets/f6c4efe5-daef-4ac8-ba92-1f568850c6f8" />
<img width="1902" height="817" alt="image" src="https://github.com/user-attachments/assets/c6149500-fedc-480d-b60a-b3bf485cc70e" />



## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## License

MIT License

---

## Author

**Mythili**  
Aspiring AI Engineer 🚀

# SkillWeaver - AI Resume Analyzer

A Django web application that analyzes resumes against job descriptions using Natural Language Processing (NLP) and Machine Learning techniques to help job seekers improve their chances of landing interviews.

---

## Features

- Upload and parse resume content (PDF/DOCX)
- Match resume against a job description using **TF-IDF** and **Cosine Similarity**
- Generate a **skill match score** showing how relevant the resume is
- Provide **improvement suggestions** based on missing keywords and skills
- Clean and intuitive web interface built with Django

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| NLP / ML | Scikit-learn (TF-IDF, Cosine Similarity) |
| Text Processing | NLTK / SpaCy |
| Frontend | HTML, CSS, Django Templates |
| Database | SQLite (default Django DB) |

---

## How It Works

1. User uploads their **resume** and pastes a **job description**
2. Text is extracted and preprocessed (tokenization, stopword removal, stemming)
3. Both texts are vectorized using **TF-IDF (Term Frequency-Inverse Document Frequency)**
4. **Cosine Similarity** is calculated between the two vectors to produce a match score
5. Missing keywords from the job description are identified and shown as suggestions

---

## Project Structure

```
ai_resume_analyzer/
│
├── manage.py
├── requirements.txt
│
├── ai_resume_analyzer/        # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── analyzer/                  # Main app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── ml/                    # ML logic
│   │   └── similarity.py
│   └── templates/
│       └── analyzer/
│           └── index.html
│
└── static/                    # CSS, JS files
```

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. Open your browser and go to `http://127.0.0.1:8000`

---

## Requirements

Create a `requirements.txt` with:

```
Django>=4.0
scikit-learn
nltk
numpy
python-docx
PyPDF2
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Usage

1. Go to the home page
2. Paste your resume text or upload a file
3. Paste the job description you are targeting
4. Click **Analyze**
5. View your match score and improvement suggestions

---

## ML Approach

### TF-IDF Vectorization
Converts resume and job description text into numerical vectors where each dimension represents the importance of a word relative to both documents.

### Cosine Similarity
Measures the angle between the two vectors. A score of **1.0** means a perfect match, while **0.0** means no similarity at all.

```
Score = (Resume Vector · JD Vector) / (||Resume Vector|| × ||JD Vector||)
```

---

## Future Improvements

- [ ] Support for PDF and DOCX file upload
- [ ] Section-wise analysis (Skills, Experience, Education)
- [ ] Export analysis report as PDF
- [ ] User authentication and history tracking
- [ ] Advanced NLP using BERT or transformer models

---

## Author

**Muchu**
- GitHub: [@yourusername](https://github.com/yourusername)

---

## License

This project is open source and available under the [MIT License](LICENSE).

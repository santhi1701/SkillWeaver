# SkillWeaver – AI Resume Analyzer for Role-Based Career Matching

SkillWeaver is a Django-based AI-powered web application that analyzes resumes and evaluates them against a selected job role instead of requiring a job description (JD). The system uses Natural Language Processing (NLP) and Machine Learning techniques to identify relevant skills, calculate a role-based match score, and provide personalized improvement suggestions for users.

---

## Features

* Upload and parse resumes (PDF/DOCX)
* Analyze resumes based on a selected job role
* Role-specific skill matching using NLP techniques
* Generate an AI-based resume match score
* Identify missing skills required for the selected role
* Provide improvement suggestions to strengthen the resume
* Clean and responsive web interface built with Django
* Supports multiple predefined technical roles

---

## Supported Roles

SkillWeaver can analyze resumes for roles such as:

* Data Scientist
* Data Analyst
* Python Developer
* Web Developer
* Machine Learning Engineer
* Frontend Developer
* Backend Developer
* Full Stack Developer

The system compares the uploaded resume with predefined skill sets for each role and calculates compatibility.

---

## Tech Stack

| Layer           | Technology                               |
| --------------- | ---------------------------------------- |
| Backend         | Python, Django                           |
| NLP / ML        | Scikit-learn (TF-IDF, Cosine Similarity) |
| Text Processing | NLTK / SpaCy                             |
| Frontend        | HTML, CSS, Django Templates              |
| Database        | SQLite (Default Django DB)               |
| File Processing | PyPDF2, python-docx                      |

---

## How It Works

1. User uploads their resume (PDF/DOCX)
2. User selects a target job role
3. Resume text is extracted and preprocessed

   * Tokenization
   * Stopword removal
   * Text normalization
4. The system compares resume content with predefined role-specific skill datasets
5. TF-IDF vectorization converts text into numerical vectors
6. Cosine Similarity calculates the similarity score
7. Missing skills and improvement suggestions are generated
8. Final role compatibility score is displayed to the user

---

## Project Structure

```bash
skillweaver/
│
├── manage.py
├── requirements.txt
│
├── skillweaver/               # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── analyzer/                  # Main application
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── ml/                    # ML and NLP logic
│   │   └── similarity.py
│   └── templates/
│       └── analyzer/
│           └── index.html
│
├── static/                    # CSS and JS files
└── media/                     # Uploaded resumes
```

---

## Getting Started

### Prerequisites

* Python 3.8+
* pip

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/santhi1701/skillweaver.git
cd skillweaver
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. Open in Browser

```bash
http://127.0.0.1:8000
```

---

## Requirements

Create a `requirements.txt` file with the following dependencies:

```txt
Django>=4.0
scikit-learn
nltk
numpy
python-docx
PyPDF2
spacy
```

Install using:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Open the application in your browser
2. Upload your resume file or paste resume text
3. Select your target job role
4. Click the **Analyze** button
5. View:

   * Resume match score
   * Missing skills
   * Suggested improvements
   * Role compatibility analysis

---

## ML Approach

### TF-IDF Vectorization

TF-IDF (Term Frequency–Inverse Document Frequency) converts resume text and role skill data into numerical vectors based on keyword importance.

### Cosine Similarity

Cosine Similarity measures how closely the resume matches the selected role.

```text
Score = (Resume Vector · Role Vector) / (||Resume Vector|| × ||Role Vector||)
```

A higher score indicates better compatibility with the selected role.

---

## Key Functionalities

### Resume Parsing

Extracts text content from uploaded PDF and DOCX files.

### Skill Matching

Compares resume skills with predefined skills required for selected roles.

### Missing Skill Detection

Identifies important missing technologies or keywords.

### Suggestion Generation

Provides personalized recommendations to improve resume quality.

---

## Future Improvements

* [ ] Add AI-based resume recommendations using BERT/Transformers
* [ ] Role-wise interview question suggestions
* [ ] Resume score visualization dashboard
* [ ] User authentication and resume history
* [ ] Export analysis report as PDF
* [ ] ATS compatibility checking
* [ ] Real-time job recommendation integration

---

## Author

**Muchu Santhi Kumari**

* GitHub: [@santhi1701](https://github.com/santhi1701)

---

## License

This project is open-source and available under the MIT License.

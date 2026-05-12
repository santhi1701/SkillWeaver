
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import Resume, User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from difflib import SequenceMatcher
import fitz
import docx2txt
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# Home view
def home(request):
    return render(request, 'analyzer/home.html')

# Register view
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'analyzer/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'analyzer/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('home')


@login_required
def upload_resume(request, role_name=None):
    if role_name is None:
        return redirect('role_match')  # redirect if no role provided

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        if resume_file:
            request.session['uploaded_resume'] = resume_file.name
            return redirect('analyze_resume', role_name=role_name)

    return render(request, 'analyzer/upload_resume.html', {'selected_role': role_name})

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.username = username
        user.email = email
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')
    resumes = user.resumes.all() if hasattr(user, 'resumes') else None
    return render(request, 'analyzer/profile.html', {'resumes': resumes})
@login_required
def role_match(request):
    roles = [
        {'name': 'Software Engineer', 'slug': 'software-engineer', 'icon': 'fas fa-code'},
        {'name': 'Data Analyst', 'slug': 'data-analyst', 'icon': 'fas fa-chart-line'},
        {'name': 'Machine Learning Engineer', 'slug': 'ml-engineer', 'icon': 'fas fa-robot'},
        {'name': 'Full Stack Developer', 'slug': 'full-stack-developer', 'icon': 'fas fa-laptop-code'},
    ]
    return render(request, 'analyzer/role_match.html', {'roles': roles})



@login_required
def role_detail(request, role_name):
    role_display_name = role_name.replace('-', ' ').title()

    if request.method == 'POST' and request.FILES.get('resume'):
        resume_file = request.FILES['resume']
        # Redirect to the analyze page with role name
        request.session['uploaded_resume'] = resume_file.name
        request.session['selected_role'] = role_name
        return redirect('analyze_resume', role_name=role_name)

    return render(request, 'analyzer/upload_resume.html', {'role': role_display_name})


def extract_text_from_resume(file):
    try:
        if file.name.endswith('.pdf'):
            text = ""
            with fitz.open(stream=file.read(), filetype="pdf") as doc:
                for page in doc:
                    text += page.get_text()
        elif file.name.endswith('.docx'):
            text = docx2txt.process(file)
        else:
            text = file.read().decode('utf-8', errors='ignore')
        return text
    except Exception as e:
        print(" Error extracting text:", e)
        return ""


# ----------------------------
# Main analyzer view
# ----------------------------
@login_required
def analyze_resume(request, role_name):
    if request.method == 'POST':
        resume_file = request.FILES.get('resume')
        if not resume_file:
            return render(request, 'analyzer/upload_resume.html', {
                'error': "Please upload a valid resume file."
            })

        #  Step 1: Extract text safely
        resume_text = extract_text_from_resume(resume_file).lower()

        #  Step 2: Role-based skill definitions
        role_skills = {
            "software-engineer": [
                "python", "java", "c++", "spring boot", "django", "react",
                "html", "css", "javascript", "sql", "rest api", "git", "problem solving"
            ],
            "data-analyst": [
                "excel", "python", "sql", "power bi", "tableau",
                "data visualization", "statistics", "machine learning"
            ],
            "full-stack-developer": [
                "html", "css", "javascript", "react", "node.js",
                "bootstrap", "api integration", "responsive design"
            ],
            "ml-engineer": [
                "python", "machine learning", "deep learning", "tensorflow",
                "scikit-learn", "pandas", "numpy", "matplotlib", "data preprocessing"
            ],
        }

        expected = role_skills.get(role_name, [])
        matched, missing = [], []

        #  Step 3: Define aliases for flexible matching
        skill_aliases = {
            "html": ["html", "html5"],
            "css": ["css", "css3", "cascading style sheets"],
            "javascript": ["javascript", "js", "ecmascript"],
            "python": ["python", "py"],
            "java": ["java", "jdk", "jre"],
            "react": ["react", "reactjs", "react.js"],
            "node.js": ["node", "nodejs", "node.js"],
            "spring boot": ["spring", "springboot", "spring boot"],
            "django": ["django", "django framework"],
            "sql": ["sql", "mysql", "postgresql"],
            "git": ["git", "github", "gitlab"],
            "bootstrap": ["bootstrap", "bootstrap5"],
            "rest api": ["rest api", "api", "api development"],
            "data visualization": ["data visualization", "visualization", "charts"],
        }

        #  Step 4: Fuzzy match helper
        def is_similar(a, b):
            return SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.8

        #  Step 5: Smart matching logic
        for skill in expected:
            aliases = skill_aliases.get(skill.lower(), [skill])
            found = False

            for alias in aliases:
                # Check for direct or fuzzy match
                if re.search(r'\b' + re.escape(alias.lower()) + r'\b', resume_text):
                    found = True
                    break
                elif any(is_similar(alias, word) for word in re.findall(r'\w+', resume_text)):
                    found = True
                    break

            if found:
                matched.append(skill)
            else:
                missing.append(skill)

        #  Step 6: Compute friendly score
        raw_score = (len(matched) / len(expected) * 100) if expected else 0
        score = max(50, round(raw_score))  # keep it positive, never demotivating

        # Step 7: AI-generated motivational feedback
        if score >= 85:
            suggestion = " Excellent! Your resume is a great fit for this role — you're interview-ready!"
        elif score >= 70:
            suggestion = " Great match! You’re close — consider adding a few more relevant projects or skills."
        elif score >= 55:
            suggestion = " Good start! You have the base skills. Add more tools or frameworks to boost alignment."
        else:
            suggestion = " Keep improving! Add more technical keywords, certifications, or project details."

        # Step 8: Send context to template
        context = {
            'role': role_name.replace('-', ' ').title(),
            'resume_name': resume_file.name,
            'matched': matched,
            'missing': missing,
            'score': score,
            'suggestion': suggestion,
        }

        return render(request, 'analyzer/analyze_result.html', context)

    return redirect('role_match')
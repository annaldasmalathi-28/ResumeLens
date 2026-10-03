import streamlit as st
import PyPDF2
import re


# ============================================================
# RESUMELENS
# Intelligent Resume Analyzer
# ============================================================


# ------------------------------------------------------------
# 1. JOB ROLE DATABASE
# ------------------------------------------------------------

ROLES = {

    "Python Developer": [
        "python",
        "sql",
        "git",
        "oop",
        "flask",
        "rest api",
        "docker",
        "django"
    ],

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "pandas",
        "numpy",
        "power bi",
        "tableau",
        "statistics"
    ],

    "Frontend Developer": [
        "html",
        "css",
        "javascript",
        "git",
        "react",
        "typescript",
        "responsive design"
    ],

    "Java Developer": [
        "java",
        "oops",
        "sql",
        "git",
        "spring",
        "spring boot",
        "hibernate",
        "rest api"
    ],

    "AI/ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "numpy",
        "pandas",
        "scikit-learn",
        "tensorflow",
        "pytorch"
    ],

    "Backend Developer": [
        "python",
        "java",
        "sql",
        "rest api",
        "git",
        "docker",
        "database",
        "authentication"
    ]
}


# ------------------------------------------------------------
# 2. SKILL ALIASES
# ------------------------------------------------------------

SKILL_ALIASES = {

    "python": [
        "python",
        "python programming"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "database sql"
    ],

    "git": [
        "git",
        "github",
        "gitlab"
    ],

    "oop": [
        "oop",
        "object oriented programming",
        "object-oriented programming"
    ],

    "rest api": [
        "rest api",
        "restful api",
        "rest services"
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "neural networks"
    ],

    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "responsive design": [
        "responsive design",
        "responsive web design"
    ]
}


# ------------------------------------------------------------
# 3. PDF TEXT EXTRACTION
# ------------------------------------------------------------

def extract_text_from_pdf(uploaded_file):

    text = ""

    try:

        reader = PyPDF2.PdfReader(uploaded_file)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    except Exception as error:

        st.error(
            f"Error reading PDF: {error}"
        )

    return text


# ------------------------------------------------------------
# 4. TEXT CLEANING
# ------------------------------------------------------------

def clean_text(text):

    text = text.lower()

    # Remove unnecessary characters
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ------------------------------------------------------------
# 5. SKILL DETECTION
# ------------------------------------------------------------

def detect_skills(resume_text):

    resume_text = clean_text(
        resume_text
    )

    detected_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            if alias.lower() in resume_text:

                detected_skills.append(
                    skill
                )

                break

    return detected_skills


# ------------------------------------------------------------
# 6. ROLE ANALYSIS
# ------------------------------------------------------------

def analyze_resume(
    resume_text,
    target_role
):

    resume_text = clean_text(
        resume_text
    )

    required_skills = ROLES[
        target_role
    ]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        found = False

        # Check aliases
        if skill in SKILL_ALIASES:

            for alias in SKILL_ALIASES[skill]:

                if alias.lower() in resume_text:

                    found = True
                    break

        else:

            if skill.lower() in resume_text:

                found = True

        if found:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    total = len(
        required_skills
    )

    if total > 0:

        score = (
            len(matched_skills)
            / total
        ) * 100

    else:

        score = 0

    return (
        round(score, 2),
        matched_skills,
        missing_skills
    )


# ------------------------------------------------------------
# 7. RECOMMENDATIONS
# ------------------------------------------------------------

def generate_recommendations(
    missing_skills
):

    recommendations = []

    recommendation_map = {

        "python":
            "Strengthen Python fundamentals and build a practical project.",

        "sql":
            "Practice SQL queries, joins, subqueries and database design.",

        "git":
            "Learn Git and GitHub and maintain your projects using version control.",

        "oop":
            "Learn OOP concepts such as classes, inheritance, polymorphism and encapsulation.",

        "flask":
            "Learn Flask and build a Python-based web application.",

        "django":
            "Learn Django and build a backend web application.",

        "rest api":
            "Learn REST APIs and build a CRUD API project.",

        "docker":
            "Learn Docker and containerize one of your projects.",

        "pandas":
            "Learn Pandas for data cleaning and data analysis.",

        "numpy":
            "Learn NumPy for numerical computing.",

        "power bi":
            "Learn Power BI and create an interactive dashboard.",

        "tableau":
            "Learn Tableau and build a data visualization project.",

        "statistics":
            "Study statistics concepts used in data analysis.",

        "machine learning":
            "Learn supervised and unsupervised machine learning and build a prediction project.",

        "deep learning":
            "Learn neural networks and deep learning fundamentals.",

        "scikit-learn":
            "Practice machine learning using Scikit-learn.",

        "tensorflow":
            "Learn TensorFlow and build a simple neural network.",

        "pytorch":
            "Learn PyTorch and implement a basic deep learning model.",

        "html":
            "Improve HTML skills and build a responsive web project.",

        "css":
            "Learn Flexbox, Grid and responsive CSS.",

        "javascript":
            "Practice JavaScript, DOM manipulation and asynchronous programming.",

        "react":
            "Learn React fundamentals and build a frontend application.",

        "typescript":
            "Learn TypeScript fundamentals and use it in a frontend project.",

        "database":
            "Learn database design, normalization and SQL.",

        "authentication":
            "Learn authentication, authorization and secure login systems."
    }

    for skill in missing_skills:

        if skill in recommendation_map:

            recommendations.append(
                recommendation_map[skill]
            )

        else:

            recommendations.append(
                f"Learn {skill.title()} and build a project using it."
            )

    return recommendations


# ------------------------------------------------------------
# 8. RESUME SECTION DETECTION
# ------------------------------------------------------------

def detect_sections(resume_text):

    text = clean_text(
        resume_text
    )

    sections = {

        "Education": [
            "education",
            "academic",
            "qualification"
        ],

        "Experience": [
            "experience",
            "work experience",
            "employment"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certifications",
            "certificates",
            "certification"
        ],

        "Skills": [
            "skills",
            "technical skills"
        ]
    }

    found_sections = []

    for section, keywords in sections.items():

        for keyword in keywords:

            if keyword in text:

                found_sections.append(
                    section
                )

                break

    return found_sections


# ------------------------------------------------------------
# 9. RESUME QUALITY CHECK
# ------------------------------------------------------------

def calculate_resume_quality(
    resume_text
):

    score = 0

    text = clean_text(
        resume_text
    )

    # Length check
    if len(text) > 500:
        score += 20

    # Email
    if re.search(
        r"[\w\.-]+@[\w\.-]+\.\w+",
        text
    ):
        score += 20

    # Phone
    if re.search(
        r"\b\d{10}\b",
        text
    ):
        score += 20

    # LinkedIn
    if "linkedin" in text:
        score += 20

    # GitHub
    if "github" in text:
        score += 20

    return score


# ------------------------------------------------------------
# 10. STREAMLIT PAGE
# ------------------------------------------------------------

st.set_page_config(

    page_title="ResumeLens",

    page_icon="📄",

    layout="wide"
)


# ------------------------------------------------------------
# HEADER
# ------------------------------------------------------------

st.title(
    "📄 ResumeLens"
)

st.subheader(
    "Intelligent Resume Analyzer"
)

st.write(
    """
    Analyze your resume against your target career role,
    discover skill gaps and receive personalized recommendations.
    """
)

st.divider()


# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.title(
    "🎯 ResumeLens"
)

st.sidebar.write(
    """
    Upload your resume and select
    your target job role.
    """
)

st.sidebar.info(
    """
    ResumeLens analyzes:

    ✓ Skills
    ✓ Skill gaps
    ✓ Resume quality
    ✓ Role match
    ✓ Career recommendations
    """
)


# ------------------------------------------------------------
# ROLE SELECTION
# ------------------------------------------------------------

target_role = st.selectbox(

    "🎯 Select your target role",

    list(
        ROLES.keys()
    )
)


# ------------------------------------------------------------
# FILE UPLOAD
# ------------------------------------------------------------

uploaded_file = st.file_uploader(

    "📤 Upload your resume",

    type=["pdf"]
)


# ------------------------------------------------------------
# ANALYZE BUTTON
# ------------------------------------------------------------

if uploaded_file:

    st.success(
        f"Resume uploaded: {uploaded_file.name}"
    )

    if st.button(
        "🔍 Analyze Resume",
        type="primary"
    ):

        with st.spinner(
            "Analyzing your resume..."
        ):

            # Extract text
            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            if not resume_text.strip():

                st.error(
                    """
                    Could not extract text from this PDF.

                    Please upload a text-based PDF instead
                    of a scanned image PDF.
                    """
                )

                st.stop()


            # Detect skills
            detected_skills = detect_skills(
                resume_text
            )


            # Analyze target role
            score, matched, missing = analyze_resume(

                resume_text,

                target_role
            )


            # Recommendations
            recommendations = generate_recommendations(
                missing
            )


            # Sections
            sections = detect_sections(
                resume_text
            )


            # Quality
            quality_score = calculate_resume_quality(
                resume_text
            )


        # ------------------------------------------------
        # RESULTS
        # ------------------------------------------------

        st.divider()

        st.header(
            "📊 Resume Analysis Report"
        )


        # ------------------------------------------------
        # METRICS
        # ------------------------------------------------

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Role Match",
                f"{score}%"
            )


        with col2:

            st.metric(
                "Skills Found",
                len(detected_skills)
            )


        with col3:

            st.metric(
                "Missing Skills",
                len(missing)
            )


        with col4:

            st.metric(
                "Resume Quality",
                f"{quality_score}%"
            )


        # ------------------------------------------------
        # MATCH PROGRESS
        # ------------------------------------------------

        st.subheader(
            f"📈 {target_role} Match"
        )

        st.progress(
            int(score)
        )


        # ------------------------------------------------
        # MATCHED SKILLS
        # ------------------------------------------------

        st.subheader(
            "✅ Matched Skills"
        )

        if matched:

            columns = st.columns(3)

            for index, skill in enumerate(
                matched
            ):

                with columns[
                    index % 3
                ]:

                    st.success(
                        f"✓ {skill.title()}"
                    )

        else:

            st.warning(
                "No matching skills detected."
            )


        # ------------------------------------------------
        # MISSING SKILLS
        # ------------------------------------------------

        st.subheader(
            "⚠️ Skill Gaps"
        )

        if missing:

            columns = st.columns(3)

            for index, skill in enumerate(
                missing
            ):

                with columns[
                    index % 3
                ]:

                    st.warning(
                        f"• {skill.title()}"
                    )

        else:

            st.success(
                "No major skill gaps detected!"
            )


        # ------------------------------------------------
        # ALL DETECTED SKILLS
        # ------------------------------------------------

        st.subheader(
            "🧠 Skills Detected in Resume"
        )

        if detected_skills:

            skills_text = " • ".join(

                skill.title()

                for skill in detected_skills

            )

            st.info(
                skills_text
            )

        else:

            st.warning(
                "No predefined skills were detected."
            )


        # ------------------------------------------------
        # RESUME SECTIONS
        # ------------------------------------------------

        st.subheader(
            "📑 Resume Sections"
        )

        if sections:

            for section in sections:

                st.write(
                    f"✓ {section}"
                )

        else:

            st.warning(
                "Important resume sections were not detected."
            )


        # ------------------------------------------------
        # RECOMMENDATIONS
        # ------------------------------------------------

        st.subheader(
            "💡 Personalized Recommendations"
        )

        if recommendations:

            for index, recommendation in enumerate(

                recommendations,

                start=1

            ):

                st.info(
                    f"{index}. {recommendation}"
                )

        else:

            st.success(
                "Your resume matches the selected role well."
            )


        # ------------------------------------------------
        # EXPECTED SKILLS
        # ------------------------------------------------

        st.subheader(
            f"🎯 Skills Expected for {target_role}"
        )

        expected = ROLES[
            target_role
        ]

        st.write(

            " • ".join(

                skill.title()

                for skill in expected

            )

        )


        # ------------------------------------------------
        # EXTRACTED TEXT
        # ------------------------------------------------

        with st.expander(
            "📄 View Extracted Resume Text"
        ):

            st.text(
                resume_text
            )


        # ------------------------------------------------
        # FINAL MESSAGE
        # ------------------------------------------------

        st.divider()

        if score >= 80:

            st.success(
                "Your resume has strong alignment with the selected role."
            )

        elif score >= 50:

            st.warning(
                "Your resume has moderate alignment. "
                "Consider improving the identified skill gaps."
            )

        else:

            st.error(
                "Your resume has low alignment with the selected role. "
                "Focus on the recommended skills and projects."
            )

else:

    st.info(
        "👆 Upload a PDF resume to begin the analysis."
    )


# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------

st.divider()

st.caption(
    "ResumeLens | Python + Streamlit | Resume Analysis Project"
)

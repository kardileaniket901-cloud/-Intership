import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Experience Analysis | EduPro",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #4F46E5;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #6B7280;
        margin-bottom: 25px;
    }

    .info-card {
        padding: 25px;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #EEF2FF,
            #F5F3FF
        );
        text-align: center;
        border: 1px solid #E0E7FF;
    }

    .insight-card {
        padding: 25px;
        border-radius: 20px;
        background-color: #F0FDF4;
        border-left: 6px solid #22C55E;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

file = "EduPro Online Platform (2).xlsx"


teachers = pd.read_excel(
    file,
    sheet_name="Teachers"
)


courses = pd.read_excel(
    file,
    sheet_name="Courses"
)


transactions = pd.read_excel(
    file,
    sheet_name="Transactions"
)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

teachers.columns = teachers.columns.str.strip()

courses.columns = courses.columns.str.strip()

transactions.columns = transactions.columns.str.strip()


# ============================================================
# DATA INTEGRATION
# ============================================================

teacher_course = transactions.merge(
    teachers,
    on="TeacherID",
    how="left"
)

teacher_course = teacher_course.merge(
    courses,
    on="CourseID",
    how="left"
)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        📈 Experience Analysis
    </div>

    <div class="subtitle">
        Understanding the relationship between teaching experience,
        instructor performance and course quality
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Analysis Filters")


# Experience range

min_exp = int(
    teachers["YearsOfExperience"].min()
)

max_exp = int(
    teachers["YearsOfExperience"].max()
)


experience_range = st.sidebar.slider(
    "📈 Experience Range",
    min_value=min_exp,
    max_value=max_exp,
    value=(min_exp, max_exp)
)


# Rating range

min_rating = float(
    teachers["TeacherRating"].min()
)

max_rating = float(
    teachers["TeacherRating"].max()
)


rating_range = st.sidebar.slider(
    "⭐ Teacher Rating",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    step=0.1
)


# ============================================================
# FILTER TEACHERS
# ============================================================

filtered_teachers = teachers[
    teachers["YearsOfExperience"].between(
        experience_range[0],
        experience_range[1]
    )
]


filtered_teachers = filtered_teachers[
    filtered_teachers["TeacherRating"].between(
        rating_range[0],
        rating_range[1]
    )
]


# ============================================================
# FILTER INTEGRATED DATA
# ============================================================

filtered_data = teacher_course[
    teacher_course["TeacherID"].isin(
        filtered_teachers["TeacherID"]
    )
]


st.info(
    f"🔎 Analysis currently includes "
    f"**{len(filtered_teachers)} instructors**."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

if len(filtered_teachers) > 0:

    avg_experience = filtered_teachers[
        "YearsOfExperience"
    ].mean()

    avg_teacher_rating = filtered_teachers[
        "TeacherRating"
    ].mean()

else:

    avg_experience = 0

    avg_teacher_rating = 0


if len(filtered_data) > 0:

    avg_course_rating = filtered_data[
        "CourseRating"
    ].mean()

else:

    avg_course_rating = 0


# ============================================================
# CORRELATION
# ============================================================

if len(filtered_teachers) >= 2:

    teacher_correlation = filtered_teachers[
        [
            "YearsOfExperience",
            "TeacherRating"
        ]
    ].corr().iloc[0, 1]

else:

    teacher_correlation = 0


if len(filtered_data) >= 2:

    course_correlation = filtered_data[
        [
            "YearsOfExperience",
            "CourseRating"
        ]
    ].corr().iloc[0, 1]

else:

    course_correlation = 0


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Experience Performance Indicators")


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "📈 Avg Experience",
    f"{avg_experience:.1f} yrs"
)


col2.metric(
    "⭐ Avg Teacher Rating",
    f"{avg_teacher_rating:.2f}"
)


col3.metric(
    "🎯 Avg Course Rating",
    f"{avg_course_rating:.2f}"
)


col4.metric(
    "📐 Experience → Teacher",
    f"{teacher_correlation:.2f}"
)


col5.metric(
    "📐 Experience → Course",
    f"{course_correlation:.2f}"
)


st.divider()


# ============================================================
# EXPERIENCE VS TEACHER RATING
# ============================================================

st.subheader(
    "📈 Years of Experience vs Teacher Rating"
)


if len(filtered_teachers) > 0:

    fig_teacher = px.scatter(
        filtered_teachers,
        x="YearsOfExperience",
        y="TeacherRating",
        hover_data=[
            "TeacherName",
            "Expertise"
        ],
        title="Experience vs Teacher Rating"
    )


    fig_teacher.update_traces(
        marker=dict(
            size=10
        )
    )


    fig_teacher.update_layout(
        xaxis_title="Years of Experience",
        yaxis_title="Teacher Rating"
    )


    st.plotly_chart(
        fig_teacher,
        use_container_width=True
    )

else:

    st.warning(
        "No data available for the selected filters."
    )


st.divider()


# ============================================================
# EXPERIENCE VS COURSE RATING
# ============================================================

st.subheader(
    "🎯 Years of Experience vs Course Rating"
)


if len(filtered_data) > 0:

    fig_course = px.scatter(
        filtered_data,
        x="YearsOfExperience",
        y="CourseRating",
        hover_data=[
            "TeacherName",
            "CourseName",
            "CourseCategory"
        ],
        title="Experience vs Course Rating"
    )


    fig_course.update_traces(
        marker=dict(
            size=9
        )
    )


    fig_course.update_layout(
        xaxis_title="Years of Experience",
        yaxis_title="Course Rating"
    )


    st.plotly_chart(
        fig_course,
        use_container_width=True
    )

else:

    st.warning(
        "No course data available."
    )


st.divider()


# ============================================================
# CREATE EXPERIENCE GROUPS
# ============================================================

st.subheader(
    "👨‍🏫 Instructor Performance by Experience Group"
)


def experience_group(years):

    if years <= 2:

        return "0–2 Years"

    elif years <= 5:

        return "3–5 Years"

    elif years <= 10:

        return "6–10 Years"

    else:

        return "10+ Years"


experience_data = filtered_teachers.copy()


experience_data[
    "ExperienceGroup"
] = experience_data[
    "YearsOfExperience"
].apply(
    experience_group
)


# ============================================================
# GROUP ANALYSIS
# ============================================================

group_analysis = experience_data.groupby(
    "ExperienceGroup"
).agg(

    AverageTeacherRating=(
        "TeacherRating",
        "mean"
    ),

    AverageExperience=(
        "YearsOfExperience",
        "mean"
    ),

    InstructorCount=(
        "TeacherID",
        "nunique"
    )

).reset_index()


group_analysis[
    "AverageTeacherRating"
] = group_analysis[
    "AverageTeacherRating"
].round(2)


group_analysis[
    "AverageExperience"
] = group_analysis[
    "AverageExperience"
].round(1)


# ============================================================
# EXPERIENCE GROUP CHART
# ============================================================

fig_group = px.bar(
    group_analysis,
    x="ExperienceGroup",
    y="AverageTeacherRating",
    text="AverageTeacherRating",
    title="Average Teacher Rating by Experience Group"
)


fig_group.update_layout(
    xaxis_title="Experience Group",
    yaxis_title="Average Teacher Rating"
)


st.plotly_chart(
    fig_group,
    use_container_width=True
)


# ============================================================
# GROUP TABLE
# ============================================================

st.subheader(
    "📋 Experience Group Summary"
)


st.dataframe(
    group_analysis,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# BEST EXPERIENCE GROUP
# ============================================================

if len(group_analysis) > 0:

    best_group = group_analysis.loc[
        group_analysis[
            "AverageTeacherRating"
        ].idxmax()
    ]


    st.markdown(
        f"""
        <div class="info-card">

        <h2>🏆 Highest Performing Experience Group</h2>

        <h1>
        {best_group["ExperienceGroup"]}
        </h1>

        <h3>
        ⭐ Average Teacher Rating:
        {best_group["AverageTeacherRating"]:.2f}
        </h3>

        <p>
        👨‍🏫 Instructors:
        {int(best_group["InstructorCount"])}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.subheader("💡 Key Insights")


if len(filtered_teachers) >= 2:

    if teacher_correlation > 0.5:

        teacher_message = (
            "There is a strong positive relationship "
            "between experience and teacher rating."
        )

    elif teacher_correlation > 0.2:

        teacher_message = (
            "There is a moderate positive relationship "
            "between experience and teacher rating."
        )

    elif teacher_correlation >= -0.2:

        teacher_message = (
            "There is little linear relationship "
            "between experience and teacher rating."
        )

    else:

        teacher_message = (
            "There is a negative relationship "
            "between experience and teacher rating."
        )


    if course_correlation > 0.5:

        course_message = (
            "Experience also shows a strong positive "
            "relationship with course rating."
        )

    elif course_correlation > 0.2:

        course_message = (
            "Experience shows a moderate positive "
            "relationship with course rating."
        )

    elif course_correlation >= -0.2:

        course_message = (
            "Experience has little linear relationship "
            "with course rating."
        )

    else:

        course_message = (
            "Experience shows a negative relationship "
            "with course rating."
        )


    st.markdown(
        f"""
        <div class="insight-card">

        <h3>📌 Finding 1</h3>

        <p>
        {teacher_message}
        </p>

        <h3>📌 Finding 2</h3>

        <p>
        {course_message}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


else:

    st.warning(
        "Not enough data to generate statistical insights."
    )
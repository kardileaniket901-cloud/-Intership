import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Instructor Performance | EduPro",
    page_icon="🏆",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main title */

    .main-title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #4F46E5;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #6B7280;
        font-size: 18px;
        margin-bottom: 25px;
    }


    /* Section title */

    .section-title {
        font-size: 26px;
        font-weight: bold;
        color: #111827;
        margin-top: 20px;
    }


    /* Instructor card */

    .instructor-card {
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


    /* Warning card */

    .warning-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #FFF7ED;
        border-left: 6px solid #F97316;
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
# CALCULATE ENROLLMENTS PER INSTRUCTOR
# ============================================================

enrollment = transactions.groupby(
    "TeacherID"
).size().reset_index(
    name="EnrollmentCount"
)


# ============================================================
# MERGE TEACHER + ENROLLMENT
# ============================================================

teacher_data = teachers.merge(
    enrollment,
    on="TeacherID",
    how="left"
)


# If instructor has no transactions,
# replace missing enrollment with 0

teacher_data["EnrollmentCount"] = (
    teacher_data["EnrollmentCount"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# CALCULATE COURSE INFORMATION PER INSTRUCTOR
# ============================================================

teacher_courses = transactions.merge(
    courses,
    on="CourseID",
    how="left"
)


course_count = teacher_courses.groupby(
    "TeacherID"
)["CourseID"].nunique().reset_index(
    name="CourseCount"
)


teacher_data = teacher_data.merge(
    course_count,
    on="TeacherID",
    how="left"
)


teacher_data["CourseCount"] = (
    teacher_data["CourseCount"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🏆 Instructor Performance
    </div>

    <div class="subtitle">
        Evaluate instructor quality, experience, courses and enrollments
    </div>
    """,
    unsafe_allow_html=True
)


st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Filters")


# ------------------------------
# Expertise Filter
# ------------------------------

expertise_options = sorted(
    teacher_data["Expertise"]
    .dropna()
    .unique()
    .tolist()
)


selected_expertise = st.sidebar.multiselect(
    "🔬 Expertise",
    expertise_options
)


# ------------------------------
# Gender Filter
# ------------------------------

gender_options = sorted(
    teacher_data["Gender"]
    .dropna()
    .unique()
    .tolist()
)


selected_gender = st.sidebar.multiselect(
    "👤 Gender",
    gender_options
)


# ------------------------------
# Experience Filter
# ------------------------------

min_exp = int(
    teacher_data["YearsOfExperience"].min()
)

max_exp = int(
    teacher_data["YearsOfExperience"].max()
)


experience_range = st.sidebar.slider(
    "📈 Years of Experience",
    min_value=min_exp,
    max_value=max_exp,
    value=(min_exp, max_exp)
)


# ------------------------------
# Rating Filter
# ------------------------------

min_rating = float(
    teacher_data["TeacherRating"].min()
)

max_rating = float(
    teacher_data["TeacherRating"].max()
)


rating_range = st.sidebar.slider(
    "⭐ Teacher Rating",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    step=0.1
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = teacher_data.copy()


if selected_expertise:

    filtered = filtered[
        filtered["Expertise"].isin(
            selected_expertise
        )
    ]


if selected_gender:

    filtered = filtered[
        filtered["Gender"].isin(
            selected_gender
        )
    ]


filtered = filtered[
    filtered["YearsOfExperience"].between(
        experience_range[0],
        experience_range[1]
    )
]


filtered = filtered[
    filtered["TeacherRating"].between(
        rating_range[0],
        rating_range[1]
    )
]


# ============================================================
# FILTER RESULT
# ============================================================

st.info(
    f"🔎 Showing **{len(filtered)}** instructors "
    f"based on your selected filters."
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Performance Overview</div>',
    unsafe_allow_html=True
)


if len(filtered) > 0:

    total_instructors = filtered[
        "TeacherID"
    ].nunique()

    average_rating = filtered[
        "TeacherRating"
    ].mean()

    average_experience = filtered[
        "YearsOfExperience"
    ].mean()

    total_enrollments = filtered[
        "EnrollmentCount"
    ].sum()

    average_courses = filtered[
        "CourseCount"
    ].mean()


else:

    total_instructors = 0

    average_rating = 0

    average_experience = 0

    total_enrollments = 0

    average_courses = 0


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "👨‍🏫 Instructors",
        total_instructors
    )


with col2:

    st.metric(
        "⭐ Avg Rating",
        round(average_rating, 2)
    )


with col3:

    st.metric(
        "📈 Avg Experience",
        f"{average_experience:.1f} yrs"
    )


with col4:

    st.metric(
        "👥 Enrollments",
        f"{total_enrollments:,}"
    )


with col5:

    st.metric(
        "📚 Avg Courses",
        round(average_courses, 1)
    )


st.divider()


# ============================================================
# TOP INSTRUCTOR
# ============================================================

if len(filtered) > 0:

    top_instructor = filtered.loc[
        filtered["TeacherRating"].idxmax()
    ]


    st.markdown(
        """
        <div class="instructor-card">

        <h2>🥇 Top-Rated Instructor</h2>

        <h1>
        👨‍🏫
        """
        + str(top_instructor["TeacherName"])
        + """
        </h1>

        <h3>
        ⭐ Rating:
        """
        + f'{top_instructor["TeacherRating"]:.2f}'
        + """
        </h3>

        <p>
        🔬 Expertise:
        """
        + str(top_instructor["Expertise"])
        + """
        &nbsp;&nbsp; | &nbsp;&nbsp;

        📈 Experience:
        """
        + str(top_instructor["YearsOfExperience"])
        + """
        years

        &nbsp;&nbsp; | &nbsp;&nbsp;

        👥 Enrollments:
        """
        + f'{top_instructor["EnrollmentCount"]:,}'
        + """
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# TOP 10 LEADERBOARD
# ============================================================

st.subheader("🏆 Instructor Leaderboard")


leaderboard = filtered.sort_values(
    "TeacherRating",
    ascending=False
).head(10).copy()


leaderboard.insert(
    0,
    "Rank",
    range(1, len(leaderboard) + 1)
)


if len(leaderboard) > 0:

    st.dataframe(
        leaderboard[
            [
                "Rank",
                "TeacherName",
                "Expertise",
                "YearsOfExperience",
                "TeacherRating",
                "CourseCount",
                "EnrollmentCount"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No instructors match your filters."
    )


st.divider()


# ============================================================
# CHART 1 — RATING DISTRIBUTION
# ============================================================

if len(filtered) > 0:

    col1, col2 = st.columns(2)


    with col1:

        st.subheader("⭐ Teacher Rating Distribution")


        fig_rating = px.histogram(
            filtered,
            x="TeacherRating",
            nbins=10,
            title="Distribution of Teacher Ratings"
        )


        fig_rating.update_layout(
            xaxis_title="Teacher Rating",
            yaxis_title="Number of Instructors"
        )


        st.plotly_chart(
            fig_rating,
            use_container_width=True
        )


    # ========================================================
    # CHART 2 — EXPERIENCE VS RATING
    # ========================================================

    with col2:

        st.subheader(
            "📈 Experience vs Teacher Rating"
        )


        fig_experience = px.scatter(
            filtered,
            x="YearsOfExperience",
            y="TeacherRating",
            hover_data=[
                "TeacherName",
                "Expertise"
            ],
            title="Experience vs Teacher Rating"
        )


        fig_experience.update_layout(
            xaxis_title="Years of Experience",
            yaxis_title="Teacher Rating"
        )


        st.plotly_chart(
            fig_experience,
            use_container_width=True
        )


st.divider()


# ============================================================
# EXPERTISE PERFORMANCE
# ============================================================

st.subheader("🔬 Expertise-wise Performance")


if len(filtered) > 0:

    expertise_analysis = filtered.groupby(
        "Expertise"
    ).agg(
        AverageRating=(
            "TeacherRating",
            "mean"
        ),
        AverageExperience=(
            "YearsOfExperience",
            "mean"
        ),
        Instructors=(
            "TeacherID",
            "nunique"
        ),
        Enrollments=(
            "EnrollmentCount",
            "sum"
        )
    ).reset_index()


    expertise_analysis[
        "AverageRating"
    ] = expertise_analysis[
        "AverageRating"
    ].round(2)


    fig_expertise = px.bar(
        expertise_analysis.sort_values(
            "AverageRating",
            ascending=False
        ),
        x="Expertise",
        y="AverageRating",
        hover_data=[
            "Instructors",
            "AverageExperience",
            "Enrollments"
        ],
        title="Average Teacher Rating by Expertise"
    )


    fig_expertise.update_layout(
        xaxis_title="Expertise",
        yaxis_title="Average Teacher Rating"
    )


    st.plotly_chart(
        fig_expertise,
        use_container_width=True
    )


st.divider()


# ============================================================
# INSTRUCTOR DETAILS
# ============================================================

st.subheader("👨‍🏫 Instructor Details")


if len(filtered) > 0:

    instructor_names = sorted(
        filtered["TeacherName"]
        .dropna()
        .unique()
        .tolist()
    )


    selected_teacher = st.selectbox(
        "Select an instructor",
        instructor_names
    )


    teacher = filtered[
        filtered["TeacherName"]
        == selected_teacher
    ].iloc[0]


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "⭐ Teacher Rating",
        round(
            teacher["TeacherRating"],
            2
        )
    )


    col2.metric(
        "📈 Experience",
        f'{teacher["YearsOfExperience"]} years'
    )


    col3.metric(
        "📚 Courses",
        teacher["CourseCount"]
    )


    col4.metric(
        "👥 Enrollments",
        f'{teacher["EnrollmentCount"]:,}'
    )


    st.write(
        f"**Expertise:** {teacher['Expertise']}"
    )

    st.write(
        f"**Gender:** {teacher['Gender']}"
    )

    st.write(
        f"**Age:** {teacher['Age']}"
    )


st.divider()


# ============================================================
# LOW PERFORMING INSTRUCTORS
# ============================================================

st.subheader("⚠️ Instructors Requiring Attention")


if len(filtered) > 0:

    low_performers = filtered[
        filtered["TeacherRating"] < 3.5
    ].sort_values(
        "TeacherRating"
    )


    if len(low_performers) > 0:

        st.warning(
            f"{len(low_performers)} instructors "
            "have a rating below 3.5."
        )


        st.dataframe(
            low_performers[
                [
                    "TeacherName",
                    "Expertise",
                    "YearsOfExperience",
                    "TeacherRating",
                    "EnrollmentCount"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success(
            "🎉 No instructors below a 3.5 rating "
            "within the selected filters."
        )
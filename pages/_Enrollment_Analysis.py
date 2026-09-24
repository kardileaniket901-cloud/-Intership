import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Enrollment Analysis | EduPro",
    page_icon="👥",
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

    .highlight-card {
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

    .success-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #F0FDF4;
        border-left: 6px solid #22C55E;
    }

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
# DATA INTEGRATION
# ============================================================

data = transactions.merge(
    teachers,
    on="TeacherID",
    how="left"
)


data = data.merge(
    courses,
    on="CourseID",
    how="left"
)


# ============================================================
# INSTRUCTOR ENROLLMENT ANALYSIS
# ============================================================

instructor_enrollment = data.groupby(
    [
        "TeacherID",
        "TeacherName",
        "Expertise",
        "Gender",
        "Age",
        "YearsOfExperience",
        "TeacherRating"
    ]
).agg(

    EnrollmentCount=(
        "TransactionID",
        "nunique"
    ),

    CourseCount=(
        "CourseID",
        "nunique"
    ),

    AverageCourseRating=(
        "CourseRating",
        "mean"
    )

).reset_index()


instructor_enrollment[
    "AverageCourseRating"
] = instructor_enrollment[
    "AverageCourseRating"
].round(2)


# ============================================================
# RATING TIER
# ============================================================

def rating_tier(rating):

    if rating >= 4.5:

        return "High"

    elif rating >= 3.5:

        return "Medium"

    else:

        return "Low"


instructor_enrollment[
    "RatingTier"
] = instructor_enrollment[
    "TeacherRating"
].apply(
    rating_tier
)


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        👥 Enrollment Analysis
    </div>

    <div class="subtitle">
        Understanding the relationship between instructor quality
        and student enrollment
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Enrollment Filters")


# Expertise

expertise_options = sorted(
    instructor_enrollment[
        "Expertise"
    ].dropna().unique().tolist()
)


selected_expertise = st.sidebar.multiselect(
    "🔬 Expertise",
    expertise_options
)


# Rating tier

rating_tier_options = [
    "High",
    "Medium",
    "Low"
]


selected_tier = st.sidebar.multiselect(
    "⭐ Rating Tier",
    rating_tier_options
)


# Experience

min_exp = int(
    instructor_enrollment[
        "YearsOfExperience"
    ].min()
)


max_exp = int(
    instructor_enrollment[
        "YearsOfExperience"
    ].max()
)


experience_range = st.sidebar.slider(
    "📈 Experience",
    min_value=min_exp,
    max_value=max_exp,
    value=(min_exp, max_exp)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = instructor_enrollment.copy()


if selected_expertise:

    filtered = filtered[
        filtered["Expertise"].isin(
            selected_expertise
        )
    ]


if selected_tier:

    filtered = filtered[
        filtered["RatingTier"].isin(
            selected_tier
        )
    ]


filtered = filtered[
    filtered["YearsOfExperience"].between(
        experience_range[0],
        experience_range[1]
    )
]


st.info(
    f"🔎 Showing **{len(filtered)} instructors** "
    "based on your filters."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

if len(filtered) > 0:

    total_enrollments = filtered[
        "EnrollmentCount"
    ].sum()

    average_enrollment = filtered[
        "EnrollmentCount"
    ].mean()

    average_teacher_rating = filtered[
        "TeacherRating"
    ].mean()

    average_course_rating = filtered[
        "AverageCourseRating"
    ].mean()

    maximum_enrollment = filtered[
        "EnrollmentCount"
    ].max()

else:

    total_enrollments = 0

    average_enrollment = 0

    average_teacher_rating = 0

    average_course_rating = 0

    maximum_enrollment = 0


# ============================================================
# KPI SECTION
# ============================================================

st.subheader(
    "📊 Enrollment Performance Indicators"
)


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "👥 Total Enrollments",
    f"{total_enrollments:,}"
)


col2.metric(
    "👤 Avg Enrollment",
    f"{average_enrollment:.1f}"
)


col3.metric(
    "⭐ Avg Teacher Rating",
    f"{average_teacher_rating:.2f}"
)


col4.metric(
    "🎯 Avg Course Rating",
    f"{average_course_rating:.2f}"
)


col5.metric(
    "🏆 Highest Enrollment",
    f"{maximum_enrollment:,}"
)


st.divider()


# ============================================================
# TOP INSTRUCTOR BY ENROLLMENT
# ============================================================

if len(filtered) > 0:

    top_enrollment_teacher = filtered.loc[
        filtered[
            "EnrollmentCount"
        ].idxmax()
    ]


    st.markdown(
        f"""
        <div class="highlight-card">

        <h2>🏆 Most Enrolled Instructor</h2>

        <h1>
        👨‍🏫 {top_enrollment_teacher["TeacherName"]}
        </h1>

        <h3>
        👥 Enrollments:
        {int(top_enrollment_teacher["EnrollmentCount"]):,}
        </h3>

        <p>
        ⭐ Teacher Rating:
        {top_enrollment_teacher["TeacherRating"]:.2f}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        🔬 Expertise:
        {top_enrollment_teacher["Expertise"]}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        📈 Experience:
        {int(top_enrollment_teacher["YearsOfExperience"])}
        years

        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# TEACHER RATING VS ENROLLMENT
# ============================================================

st.subheader(
    "📈 Teacher Rating vs Student Enrollment"
)


if len(filtered) > 0:

    fig_rating_enrollment = px.scatter(
        filtered,
        x="TeacherRating",
        y="EnrollmentCount",
        size="EnrollmentCount",
        color="RatingTier",
        hover_data=[
            "TeacherName",
            "Expertise",
            "YearsOfExperience",
            "AverageCourseRating"
        ],
        title="Teacher Rating vs Enrollment"
    )


    fig_rating_enrollment.update_layout(
        xaxis_title="Teacher Rating",
        yaxis_title="Number of Enrollments"
    )


    st.plotly_chart(
        fig_rating_enrollment,
        use_container_width=True
    )


st.divider()


# ============================================================
# RATING TIER COMPARISON
# ============================================================

st.subheader(
    "⭐ Enrollment by Instructor Rating Tier"
)


if len(filtered) > 0:

    tier_analysis = filtered.groupby(
        "RatingTier"
    ).agg(

        AverageEnrollment=(
            "EnrollmentCount",
            "mean"
        ),

        TotalEnrollment=(
            "EnrollmentCount",
            "sum"
        ),

        AverageTeacherRating=(
            "TeacherRating",
            "mean"
        ),

        InstructorCount=(
            "TeacherID",
            "nunique"
        )

    ).reset_index()


    tier_analysis[
        "AverageEnrollment"
    ] = tier_analysis[
        "AverageEnrollment"
    ].round(1)


    tier_analysis[
        "AverageTeacherRating"
    ] = tier_analysis[
        "AverageTeacherRating"
    ].round(2)


    fig_tier = px.bar(
        tier_analysis,
        x="RatingTier",
        y="AverageEnrollment",
        text="AverageEnrollment",
        title="Average Enrollment by Instructor Rating Tier"
    )


    fig_tier.update_layout(
        xaxis_title="Instructor Rating Tier",
        yaxis_title="Average Enrollment"
    )


    st.plotly_chart(
        fig_tier,
        use_container_width=True
    )


st.divider()


# ============================================================
# TOP 10 INSTRUCTORS BY ENROLLMENT
# ============================================================

st.subheader(
    "🏆 Top 10 Instructors by Enrollment"
)


top10 = filtered.sort_values(
    "EnrollmentCount",
    ascending=False
).head(10)


if len(top10) > 0:

    fig_top10 = px.bar(
        top10.sort_values(
            "EnrollmentCount"
        ),
        x="EnrollmentCount",
        y="TeacherName",
        orientation="h",
        text="EnrollmentCount",
        color="TeacherRating",
        title="Top 10 Instructors by Student Enrollment"
    )


    fig_top10.update_layout(
        xaxis_title="Enrollments",
        yaxis_title="Instructor"
    )


    st.plotly_chart(
        fig_top10,
        use_container_width=True
    )


st.divider()


# ============================================================
# EXPERTISE VS ENROLLMENT
# ============================================================

st.subheader(
    "🔬 Enrollment by Expertise"
)


if len(filtered) > 0:

    expertise_enrollment = filtered.groupby(
        "Expertise"
    ).agg(

        TotalEnrollment=(
            "EnrollmentCount",
            "sum"
        ),

        AverageEnrollment=(
            "EnrollmentCount",
            "mean"
        ),

        AverageTeacherRating=(
            "TeacherRating",
            "mean"
        )

    ).reset_index()


    expertise_enrollment[
        "AverageEnrollment"
    ] = expertise_enrollment[
        "AverageEnrollment"
    ].round(1)


    fig_expertise = px.bar(
        expertise_enrollment.sort_values(
            "TotalEnrollment",
            ascending=False
        ),
        x="Expertise",
        y="TotalEnrollment",
        text="TotalEnrollment",
        title="Total Enrollment by Instructor Expertise",
        hover_data=[
            "AverageEnrollment",
            "AverageTeacherRating"
        ]
    )


    st.plotly_chart(
        fig_expertise,
        use_container_width=True
    )


st.divider()


# ============================================================
# COURSE CATEGORY ENROLLMENT
# ============================================================

st.subheader(
    "📚 Enrollment by Course Category"
)


category_data = data[
    data["TeacherID"].isin(
        filtered["TeacherID"]
    )
]


if len(category_data) > 0:

    category_enrollment = category_data.groupby(
        "CourseCategory"
    ).size().reset_index(
        name="EnrollmentCount"
    )


    category_enrollment = category_enrollment.sort_values(
        "EnrollmentCount",
        ascending=False
    )


    fig_category = px.bar(
        category_enrollment,
        x="CourseCategory",
        y="EnrollmentCount",
        text="EnrollmentCount",
        title="Student Enrollment by Course Category"
    )


    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


st.divider()


# ============================================================
# LOW RATING + HIGH ENROLLMENT
# ============================================================

st.subheader(
    "⚠️ Low-Rated Instructors with High Enrollment"
)


if len(filtered) > 0:

    enrollment_median = filtered[
        "EnrollmentCount"
    ].median()


    attention = filtered[
        (filtered["TeacherRating"] < 3.5)
        &
        (filtered["EnrollmentCount"] > enrollment_median)
    ].sort_values(
        "EnrollmentCount",
        ascending=False
    )


    if len(attention) > 0:

        st.warning(
            f"{len(attention)} instructors have "
            "below-3.5 ratings but above-median enrollment."
        )


        st.dataframe(
            attention[
                [
                    "TeacherName",
                    "Expertise",
                    "TeacherRating",
                    "AverageCourseRating",
                    "EnrollmentCount",
                    "YearsOfExperience"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


    else:

        st.success(
            "🎉 No low-rated, high-enrollment instructors "
            "were found."
        )


st.divider()


# ============================================================
# DETAILED TABLE
# ============================================================

st.subheader(
    "📋 Detailed Instructor Enrollment Analysis"
)


if len(filtered) > 0:

    st.dataframe(
        filtered.sort_values(
            "EnrollmentCount",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.subheader(
    "💡 Enrollment Insights"
)


if len(filtered) >= 2:

    correlation = filtered[
        [
            "TeacherRating",
            "EnrollmentCount"
        ]
    ].corr().iloc[0, 1]


    if correlation > 0.5:

        message = (
            "There is a strong positive relationship "
            "between teacher rating and enrollment."
        )

    elif correlation > 0.2:

        message = (
            "There is a moderate positive relationship "
            "between teacher rating and enrollment."
        )

    elif correlation >= -0.2:

        message = (
            "There is little linear relationship "
            "between teacher rating and enrollment."
        )

    else:

        message = (
            "There is a negative relationship "
            "between teacher rating and enrollment."
        )


    st.markdown(
        f"""
        <div class="success-card">

        <h3>📌 Rating → Enrollment Relationship</h3>

        <p>
        {message}
        </p>

        <p>
        <b>Correlation:</b> {correlation:.2f}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

else:

    st.warning(
        "Not enough data to calculate correlation."
    )
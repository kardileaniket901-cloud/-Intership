import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Expertise Analysis | EduPro",
    page_icon="🔬",
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

    .expertise-card {
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
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🔬 Expertise Analysis
    </div>

    <div class="subtitle">
        Evaluate teaching quality, course quality and demand
        across instructor expertise areas
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔎 Expertise Filters")


# Expertise

expertise_options = sorted(
    data["Expertise"]
    .dropna()
    .unique()
    .tolist()
)


selected_expertise = st.sidebar.multiselect(
    "🔬 Select Expertise",
    expertise_options
)


# Course category

category_options = sorted(
    data["CourseCategory"]
    .dropna()
    .unique()
    .tolist()
)


selected_category = st.sidebar.multiselect(
    "📚 Course Category",
    category_options
)


# Course level

level_options = sorted(
    data["CourseLevel"]
    .dropna()
    .unique()
    .tolist()
)


selected_level = st.sidebar.multiselect(
    "🎯 Course Level",
    level_options
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = data.copy()


if selected_expertise:

    filtered = filtered[
        filtered["Expertise"].isin(
            selected_expertise
        )
    ]


if selected_category:

    filtered = filtered[
        filtered["CourseCategory"].isin(
            selected_category
        )
    ]


if selected_level:

    filtered = filtered[
        filtered["CourseLevel"].isin(
            selected_level
        )
    ]


# ============================================================
# FILTER INFORMATION
# ============================================================

st.info(
    f"🔎 Analysis includes **{len(filtered)} enrollment records**."
)


# ============================================================
# EXPERTISE SUMMARY
# ============================================================

expertise_summary = filtered.groupby(
    "Expertise"
).agg(

    InstructorCount=(
        "TeacherID",
        "nunique"
    ),

    AverageTeacherRating=(
        "TeacherRating",
        "mean"
    ),

    AverageCourseRating=(
        "CourseRating",
        "mean"
    ),

    EnrollmentCount=(
        "TransactionID",
        "nunique"
    ),

    AverageExperience=(
        "YearsOfExperience",
        "mean"
    )

).reset_index()


expertise_summary[
    "AverageTeacherRating"
] = expertise_summary[
    "AverageTeacherRating"
].round(2)


expertise_summary[
    "AverageCourseRating"
] = expertise_summary[
    "AverageCourseRating"
].round(2)


expertise_summary[
    "AverageExperience"
] = expertise_summary[
    "AverageExperience"
].round(1)


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Expertise Performance Overview")


if len(expertise_summary) > 0:

    best_expertise = expertise_summary.loc[
        expertise_summary[
            "AverageTeacherRating"
        ].idxmax()
    ]


    highest_course_quality = expertise_summary.loc[
        expertise_summary[
            "AverageCourseRating"
        ].idxmax()
    ]


    total_enrollments = expertise_summary[
        "EnrollmentCount"
    ].sum()


    average_teacher_rating = filtered[
        "TeacherRating"
    ].mean()


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "🔬 Expertise Areas",
        len(expertise_summary)
    )


    col2.metric(
        "⭐ Avg Teacher Rating",
        round(
            average_teacher_rating,
            2
        )
    )


    col3.metric(
        "🎯 Best Teacher Expertise",
        best_expertise["Expertise"]
    )


    col4.metric(
        "👥 Total Enrollments",
        f"{total_enrollments:,}"
    )


else:

    st.warning(
        "No data available for the selected filters."
    )


st.divider()


# ============================================================
# TEACHER RATING BY EXPERTISE
# ============================================================

st.subheader(
    "⭐ Average Teacher Rating by Expertise"
)


if len(expertise_summary) > 0:

    teacher_rating_chart = px.bar(
        expertise_summary.sort_values(
            "AverageTeacherRating",
            ascending=False
        ),
        x="Expertise",
        y="AverageTeacherRating",
        text="AverageTeacherRating",
        title="Teaching Quality by Expertise",
        hover_data=[
            "InstructorCount",
            "AverageExperience",
            "EnrollmentCount"
        ]
    )


    teacher_rating_chart.update_layout(
        xaxis_title="Expertise",
        yaxis_title="Average Teacher Rating"
    )


    st.plotly_chart(
        teacher_rating_chart,
        use_container_width=True
    )


st.divider()


# ============================================================
# COURSE RATING BY EXPERTISE
# ============================================================

st.subheader(
    "🎯 Average Course Rating by Expertise"
)


if len(expertise_summary) > 0:

    course_rating_chart = px.bar(
        expertise_summary.sort_values(
            "AverageCourseRating",
            ascending=False
        ),
        x="Expertise",
        y="AverageCourseRating",
        text="AverageCourseRating",
        title="Course Quality by Instructor Expertise",
        hover_data=[
            "InstructorCount",
            "AverageExperience",
            "EnrollmentCount"
        ]
    )


    course_rating_chart.update_layout(
        xaxis_title="Expertise",
        yaxis_title="Average Course Rating"
    )


    st.plotly_chart(
        course_rating_chart,
        use_container_width=True
    )


st.divider()


# ============================================================
# TEACHER RATING VS COURSE RATING
# ============================================================

st.subheader(
    "📈 Teacher Quality vs Course Quality"
)


if len(expertise_summary) > 0:

    fig_comparison = px.scatter(
        expertise_summary,
        x="AverageTeacherRating",
        y="AverageCourseRating",
        size="EnrollmentCount",
        color="Expertise",
        hover_data=[
            "InstructorCount",
            "AverageExperience"
        ],
        title="Instructor Rating vs Course Rating by Expertise"
    )


    fig_comparison.update_layout(
        xaxis_title="Average Teacher Rating",
        yaxis_title="Average Course Rating"
    )


    st.plotly_chart(
        fig_comparison,
        use_container_width=True
    )


st.divider()


# ============================================================
# ENROLLMENT BY EXPERTISE
# ============================================================

st.subheader(
    "👥 Enrollment by Expertise"
)


if len(expertise_summary) > 0:

    enrollment_chart = px.bar(
        expertise_summary.sort_values(
            "EnrollmentCount",
            ascending=False
        ),
        x="Expertise",
        y="EnrollmentCount",
        text="EnrollmentCount",
        title="Student Enrollment by Instructor Expertise"
    )


    enrollment_chart.update_layout(
        xaxis_title="Expertise",
        yaxis_title="Number of Enrollments"
    )


    st.plotly_chart(
        enrollment_chart,
        use_container_width=True
    )


st.divider()


# ============================================================
# EXPERIENCE BY EXPERTISE
# ============================================================

st.subheader(
    "📈 Experience by Expertise"
)


if len(expertise_summary) > 0:

    experience_chart = px.bar(
        expertise_summary.sort_values(
            "AverageExperience",
            ascending=False
        ),
        x="Expertise",
        y="AverageExperience",
        text="AverageExperience",
        title="Average Teaching Experience by Expertise"
    )


    experience_chart.update_layout(
        xaxis_title="Expertise",
        yaxis_title="Average Years of Experience"
    )


    st.plotly_chart(
        experience_chart,
        use_container_width=True
    )


st.divider()


# ============================================================
# EXPERTISE PERFORMANCE TABLE
# ============================================================

st.subheader(
    "📋 Detailed Expertise Performance"
)


if len(expertise_summary) > 0:

    st.dataframe(
        expertise_summary.sort_values(
            "AverageTeacherRating",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# BEST EXPERTISE
# ============================================================

if len(expertise_summary) > 0:

    best_expertise = expertise_summary.loc[
        expertise_summary[
            "AverageTeacherRating"
        ].idxmax()
    ]


    st.markdown(
        f"""
        <div class="success-card">

        <h2>🏆 Strongest Expertise Area</h2>

        <h1>
        🔬 {best_expertise["Expertise"]}
        </h1>

        <p>
        ⭐ Teacher Rating:
        <b>{best_expertise["AverageTeacherRating"]:.2f}</b>
        </p>

        <p>
        🎯 Course Rating:
        <b>{best_expertise["AverageCourseRating"]:.2f}</b>
        </p>

        <p>
        👥 Enrollments:
        <b>{int(best_expertise["EnrollmentCount"]):,}</b>
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# TRAINING / IMPROVEMENT AREAS
# ============================================================

st.subheader(
    "⚠️ Potential Expertise Improvement Areas"
)


if len(expertise_summary) > 0:

    improvement = expertise_summary[
        expertise_summary[
            "AverageTeacherRating"
        ] < 3.5
    ].sort_values(
        "AverageTeacherRating"
    )


    if len(improvement) > 0:

        st.warning(
            f"{len(improvement)} expertise areas "
            "have an average teacher rating below 3.5."
        )


        st.dataframe(
            improvement[
                [
                    "Expertise",
                    "InstructorCount",
                    "AverageTeacherRating",
                    "AverageCourseRating",
                    "EnrollmentCount"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


    else:

        st.success(
            "🎉 No expertise area has an average "
            "teacher rating below 3.5."
        )


st.divider()


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.subheader("💡 Key Expertise Insights")


if len(expertise_summary) > 0:

    highest_enrollment = expertise_summary.loc[
        expertise_summary[
            "EnrollmentCount"
        ].idxmax()
    ]


    highest_course_rating = expertise_summary.loc[
        expertise_summary[
            "AverageCourseRating"
        ].idxmax()
    ]


    col1, col2 = st.columns(2)


    with col1:

        st.success(
            f"👥 **Highest enrollment expertise:** "
            f"{highest_enrollment['Expertise']} "
            f"with "
            f"{int(highest_enrollment['EnrollmentCount']):,} "
            f"enrollments."
        )


    with col2:

        st.success(
            f"🎯 **Highest course quality expertise:** "
            f"{highest_course_rating['Expertise']} "
            f"with an average course rating of "
            f"{highest_course_rating['AverageCourseRating']:.2f}."
        )

else:

    st.warning(
        "Select different filters to generate insights."
    )
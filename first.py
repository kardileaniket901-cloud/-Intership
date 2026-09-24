import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduPro Overview",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# LOAD DATA
# ============================================================

file = "EduPro Online Platform (2).xlsx"

users = pd.read_excel(
    file,
    sheet_name="Users"
)

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

users.columns = users.columns.str.strip()
teachers.columns = teachers.columns.str.strip()
courses.columns = courses.columns.str.strip()
transactions.columns = transactions.columns.str.strip()


# ============================================================
# PAGE TITLE
# ============================================================

st.markdown(
    """
    <h1 style="
        text-align:center;
        color:#4F46E5;
        font-size:45px;
    ">
        📊 EduPro Overview
    </h1>

    <p style="
        text-align:center;
        font-size:18px;
        color:#666666;
    ">
        Instructor Performance & Course Quality Evaluation
    </p>
    """,
    unsafe_allow_html=True
)


st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.subheader("Instructor Filters")


# Expertise filter

expertise_options = sorted(
    teachers["Expertise"].dropna().unique().tolist()
)

selected_expertise = st.sidebar.multiselect(
    "Select Expertise",
    expertise_options
)


# Teacher rating filter

min_teacher_rating = float(
    teachers["TeacherRating"].min()
)

max_teacher_rating = float(
    teachers["TeacherRating"].max()
)

selected_rating = st.sidebar.slider(
    "Teacher Rating",
    min_value=min_teacher_rating,
    max_value=max_teacher_rating,
    value=(min_teacher_rating, max_teacher_rating),
    step=0.1
)


# ============================================================
# FILTER TEACHERS
# ============================================================

filtered_teachers = teachers[
    teachers["TeacherRating"].between(
        selected_rating[0],
        selected_rating[1]
    )
]


if selected_expertise:

    filtered_teachers = filtered_teachers[
        filtered_teachers["Expertise"].isin(
            selected_expertise
        )
    ]


# ============================================================
# FILTER INFORMATION
# ============================================================

st.info(
    f"Showing {len(filtered_teachers)} instructors "
    f"based on your selected filters."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_instructors = filtered_teachers[
    "TeacherID"
].nunique()

total_courses = courses[
    "CourseID"
].nunique()

total_transactions = transactions[
    "TransactionID"
].nunique()


if len(filtered_teachers) > 0:

    average_teacher_rating = filtered_teachers[
        "TeacherRating"
    ].mean()

else:

    average_teacher_rating = 0


average_course_rating = courses[
    "CourseRating"
].mean()


# ============================================================
# KPI CARDS
# ============================================================

st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "👨‍🏫 Instructors",
        total_instructors
    )


with col2:

    st.metric(
        "📚 Courses",
        total_courses
    )


with col3:

    st.metric(
        "📝 Transactions",
        total_transactions
    )


with col4:

    st.metric(
        "⭐ Teacher Rating",
        round(average_teacher_rating, 2)
    )


with col5:

    st.metric(
        "🎯 Course Rating",
        round(average_course_rating, 2)
    )


st.divider()


# ============================================================
# TOP 5 INSTRUCTORS
# ============================================================

st.subheader("🏆 Top 5 Instructors")


top5 = filtered_teachers.sort_values(
    "TeacherRating",
    ascending=False
).head(5)


if len(top5) > 0:

    st.dataframe(
        top5[
            [
                "TeacherID",
                "TeacherName",
                "Expertise",
                "YearsOfExperience",
                "TeacherRating"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning(
        "No instructors match the selected filters."
    )


st.divider()


# ============================================================
# CHART 1 — GENDER DISTRIBUTION
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("👨‍🏫 Instructor Gender Distribution")

    gender_data = filtered_teachers[
        "Gender"
    ].value_counts().reset_index()

    gender_data.columns = [
        "Gender",
        "Count"
    ]

    if len(gender_data) > 0:

        fig_gender = px.pie(
            gender_data,
            names="Gender",
            values="Count",
            title="Instructor Gender Distribution"
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True
        )


# ============================================================
# CHART 2 — EXPERTISE DISTRIBUTION
# ============================================================

with col2:

    st.subheader("🔬 Instructor Expertise")

    expertise_data = filtered_teachers[
        "Expertise"
    ].value_counts().reset_index()

    expertise_data.columns = [
        "Expertise",
        "Count"
    ]

    if len(expertise_data) > 0:

        fig_expertise = px.bar(
            expertise_data,
            x="Expertise",
            y="Count",
            title="Instructor Distribution by Expertise"
        )

        st.plotly_chart(
            fig_expertise,
            use_container_width=True
        )


st.divider()


# ============================================================
# CHART 3 — EXPERIENCE VS TEACHER RATING
# ============================================================

st.subheader("📈 Experience vs Teacher Rating")


if len(filtered_teachers) > 0:

    fig_experience = px.scatter(
        filtered_teachers,
        x="YearsOfExperience",
        y="TeacherRating",
        hover_data=[
            "TeacherName",
            "Expertise"
        ],
        title="Years of Experience vs Teacher Rating",
        trendline="ols"
    )

    st.plotly_chart(
        fig_experience,
        use_container_width=True
    )


st.divider()


# ============================================================
# COURSE CATEGORY PERFORMANCE
# ============================================================

st.subheader("📚 Course Category Performance")


category_rating = courses.groupby(
    "CourseCategory"
)["CourseRating"].mean().reset_index()


category_rating = category_rating.sort_values(
    "CourseRating",
    ascending=False
)


fig_category = px.bar(
    category_rating,
    x="CourseCategory",
    y="CourseRating",
    title="Average Course Rating by Category"
)


st.plotly_chart(
    fig_category,
    use_container_width=True
)


st.divider()


# ============================================================
# QUICK INSIGHTS
# ============================================================

st.subheader("💡 Quick Insights")


if len(filtered_teachers) > 0:

    best_teacher = filtered_teachers.loc[
        filtered_teachers["TeacherRating"].idxmax()
    ]

    highest_category = category_rating.iloc[0]

    col1, col2 = st.columns(2)


    with col1:

        st.success(
            f"🏆 Highest-rated instructor: "
            f"**{best_teacher['TeacherName']}** "
            f"with a rating of "
            f"**{best_teacher['TeacherRating']:.2f}**."
        )


    with col2:

        st.success(
            f"📚 Highest-rated course category: "
            f"**{highest_category['CourseCategory']}** "
            f"with an average rating of "
            f"**{highest_category['CourseRating']:.2f}**."
        )

else:

    st.warning(
        "Select different filters to see insights."
    )
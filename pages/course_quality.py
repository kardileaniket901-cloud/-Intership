import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Course Quality | EduPro",
    page_icon="📚",
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

    .quality-card {
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

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

file = "EduPro Online Platform (2).xlsx"

courses = pd.read_excel(
    file,
    sheet_name="Courses"
)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

courses.columns = courses.columns.str.strip()


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        📚 Course Quality Analysis
    </div>

    <div class="subtitle">
        Evaluate course ratings, categories, levels and duration
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🔎 Course Filters")


# ------------------------------------------------------------
# Category Filter
# ------------------------------------------------------------

category_options = sorted(
    courses["CourseCategory"]
    .dropna()
    .unique()
    .tolist()
)

selected_category = st.sidebar.multiselect(
    "📚 Course Category",
    category_options
)


# ------------------------------------------------------------
# Level Filter
# ------------------------------------------------------------

level_options = sorted(
    courses["CourseLevel"]
    .dropna()
    .unique()
    .tolist()
)

selected_level = st.sidebar.multiselect(
    "🎯 Course Level",
    level_options
)


# ------------------------------------------------------------
# Rating Filter
# ------------------------------------------------------------

min_rating = float(
    courses["CourseRating"].min()
)

max_rating = float(
    courses["CourseRating"].max()
)

rating_range = st.sidebar.slider(
    "⭐ Course Rating",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    step=0.1
)


# ------------------------------------------------------------
# Duration Filter
# ------------------------------------------------------------

min_duration = int(
    courses["CourseDuration"].min()
)

max_duration = int(
    courses["CourseDuration"].max()
)

duration_range = st.sidebar.slider(
    "⏱️ Course Duration",
    min_value=min_duration,
    max_value=max_duration,
    value=(min_duration, max_duration)
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered = courses.copy()


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


filtered = filtered[
    filtered["CourseRating"].between(
        rating_range[0],
        rating_range[1]
    )
]


filtered = filtered[
    filtered["CourseDuration"].between(
        duration_range[0],
        duration_range[1]
    )
]


# ============================================================
# FILTER INFORMATION
# ============================================================

st.info(
    f"🔎 Showing **{len(filtered)} courses** "
    "based on your selected filters."
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

if len(filtered) > 0:

    total_courses = filtered[
        "CourseID"
    ].nunique()

    average_rating = filtered[
        "CourseRating"
    ].mean()

    average_duration = filtered[
        "CourseDuration"
    ].mean()

    highest_rating = filtered[
        "CourseRating"
    ].max()

    lowest_rating = filtered[
        "CourseRating"
    ].min()

else:

    total_courses = 0

    average_rating = 0

    average_duration = 0

    highest_rating = 0

    lowest_rating = 0


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📊 Course Quality Indicators")


col1, col2, col3, col4, col5 = st.columns(5)


col1.metric(
    "📚 Courses",
    total_courses
)


col2.metric(
    "⭐ Avg Rating",
    round(average_rating, 2)
)


col3.metric(
    "⏱️ Avg Duration",
    round(average_duration, 1)
)


col4.metric(
    "🏆 Highest Rating",
    round(highest_rating, 2)
)


col5.metric(
    "⚠️ Lowest Rating",
    round(lowest_rating, 2)
)


st.divider()


# ============================================================
# TOP-RATED COURSE
# ============================================================

if len(filtered) > 0:

    top_course = filtered.loc[
        filtered["CourseRating"].idxmax()
    ]


    st.markdown(
        f"""
        <div class="quality-card">

        <h2>🏆 Highest Rated Course</h2>

        <h1>
        📚 {top_course["CourseName"]}
        </h1>

        <h3>
        ⭐ Rating:
        {top_course["CourseRating"]:.2f}
        </h3>

        <p>
        📂 Category:
        {top_course["CourseCategory"]}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        🎯 Level:
        {top_course["CourseLevel"]}

        &nbsp;&nbsp; | &nbsp;&nbsp;

        ⏱️ Duration:
        {top_course["CourseDuration"]}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# COURSE RATING DISTRIBUTION
# ============================================================

st.subheader("⭐ Course Rating Distribution")


if len(filtered) > 0:

    fig_rating = px.histogram(
        filtered,
        x="CourseRating",
        nbins=10,
        title="Distribution of Course Ratings"
    )


    fig_rating.update_layout(
        xaxis_title="Course Rating",
        yaxis_title="Number of Courses"
    )


    st.plotly_chart(
        fig_rating,
        use_container_width=True
    )


st.divider()


# ============================================================
# CATEGORY VS RATING
# ============================================================

st.subheader(
    "📚 Average Course Rating by Category"
)


if len(filtered) > 0:

    category_rating = filtered.groupby(
        "CourseCategory"
    )["CourseRating"].mean().reset_index()


    category_rating[
        "CourseRating"
    ] = category_rating[
        "CourseRating"
    ].round(2)


    category_rating = category_rating.sort_values(
        "CourseRating",
        ascending=False
    )


    fig_category = px.bar(
        category_rating,
        x="CourseCategory",
        y="CourseRating",
        text="CourseRating",
        title="Course Quality by Category"
    )


    fig_category.update_layout(
        xaxis_title="Course Category",
        yaxis_title="Average Course Rating"
    )


    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


st.divider()


# ============================================================
# COURSE LEVEL ANALYSIS
# ============================================================

st.subheader(
    "🎯 Average Course Rating by Level"
)


if len(filtered) > 0:

    level_rating = filtered.groupby(
        "CourseLevel"
    )["CourseRating"].mean().reset_index()


    level_rating[
        "CourseRating"
    ] = level_rating[
        "CourseRating"
    ].round(2)


    fig_level = px.bar(
        level_rating,
        x="CourseLevel",
        y="CourseRating",
        text="CourseRating",
        title="Course Quality by Level"
    )


    fig_level.update_layout(
        xaxis_title="Course Level",
        yaxis_title="Average Course Rating"
    )


    st.plotly_chart(
        fig_level,
        use_container_width=True
    )


st.divider()


# ============================================================
# CATEGORY × LEVEL HEATMAP
# ============================================================

st.subheader(
    "🔥 Course Category × Level Heatmap"
)


if len(filtered) > 0:

    heatmap_data = filtered.pivot_table(
        values="CourseRating",
        index="CourseCategory",
        columns="CourseLevel",
        aggfunc="mean"
    )


    fig, ax = plt.subplots(
        figsize=(10, 6)
    )


    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        cmap="YlGnBu",
        linewidths=0.5,
        ax=ax
    )


    ax.set_title(
        "Average Course Rating by Category and Level"
    )


    ax.set_xlabel("Course Level")

    ax.set_ylabel("Course Category")


    st.pyplot(fig)


st.divider()


# ============================================================
# COURSE DURATION ANALYSIS
# ============================================================

st.subheader(
    "⏱️ Course Duration vs Course Rating"
)


if len(filtered) > 0:

    fig_duration = px.scatter(
        filtered,
        x="CourseDuration",
        y="CourseRating",
        hover_data=[
            "CourseName",
            "CourseCategory",
            "CourseLevel"
        ],
        title="Course Duration vs Course Rating"
    )


    fig_duration.update_layout(
        xaxis_title="Course Duration",
        yaxis_title="Course Rating"
    )


    st.plotly_chart(
        fig_duration,
        use_container_width=True
    )


st.divider()


# ============================================================
# LONG COURSES ANALYSIS
# ============================================================

st.subheader(
    "⏱️ Courses Longer Than 40"
)


long_courses = filtered[
    filtered["CourseDuration"] > 40
]


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Courses > 40 Duration",
        len(long_courses)
    )


with col2:

    if len(long_courses) > 0:

        st.metric(
            "Average Rating",
            round(
                long_courses["CourseRating"].mean(),
                2
            )
        )

    else:

        st.metric(
            "Average Rating",
            0
        )


if len(long_courses) > 0:

    st.dataframe(
        long_courses[
            [
                "CourseID",
                "CourseName",
                "CourseCategory",
                "CourseLevel",
                "CourseDuration",
                "CourseRating"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# TOP 10 COURSES
# ============================================================

st.subheader("🏆 Top 10 Courses")


top_courses = filtered.sort_values(
    "CourseRating",
    ascending=False
).head(10)


if len(top_courses) > 0:

    st.dataframe(
        top_courses[
            [
                "CourseName",
                "CourseCategory",
                "CourseLevel",
                "CourseDuration",
                "CourseRating"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# LOW-RATED COURSES
# ============================================================

st.subheader(
    "⚠️ Courses Requiring Attention"
)


low_courses = filtered[
    filtered["CourseRating"] < 3.5
].sort_values(
    "CourseRating"
)


if len(low_courses) > 0:

    st.warning(
        f"{len(low_courses)} courses "
        "have a rating below 3.5."
    )


    st.dataframe(
        low_courses[
            [
                "CourseName",
                "CourseCategory",
                "CourseLevel",
                "CourseRating",
                "CourseDuration"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success(
        "🎉 No courses below 3.5 rating "
        "within the selected filters."
    )


st.divider()


# ============================================================
# AUTOMATIC INSIGHTS
# ============================================================

st.subheader("💡 Key Course Insights")


if len(filtered) > 0:

    best_category = category_rating.iloc[0]

    best_level = level_rating.loc[
        level_rating["CourseRating"].idxmax()
    ]


    col1, col2 = st.columns(2)


    with col1:

        st.success(
            f"📚 Highest-rated category: "
            f"**{best_category['CourseCategory']}** "
            f"with an average rating of "
            f"**{best_category['CourseRating']:.2f}**."
        )


    with col2:

        st.success(
            f"🎯 Highest-rated level: "
            f"**{best_level['CourseLevel']}** "
            f"with an average rating of "
            f"**{best_level['CourseRating']:.2f}**."
        )

else:

    st.warning(
        "No data available for the selected filters."
    )
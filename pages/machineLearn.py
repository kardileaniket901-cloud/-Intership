import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ML Prediction | EduPro",
    page_icon="🤖",
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

    .prediction-card {
        padding: 30px;
        border-radius: 25px;
        background: linear-gradient(
            135deg,
            #EEF2FF,
            #F5F3FF
        );
        text-align: center;
        border: 1px solid #C7D2FE;
    }

    .prediction-number {
        font-size: 55px;
        font-weight: bold;
        color: #4F46E5;
    }

    .model-card {
        padding: 20px;
        border-radius: 15px;
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


# ============================================================
# CLEAN DATA
# ============================================================

teachers.columns = teachers.columns.str.strip()


# Keep only required columns

ml_data = teachers[
    [
        "YearsOfExperience",
        "TeacherRating"
    ]
].dropna()


# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
    <div class="main-title">
        🤖 Teacher Rating Prediction
    </div>

    <div class="subtitle">
        Predict instructor rating using teaching experience
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# PROJECT OBJECTIVE
# ============================================================

st.subheader("🎯 Machine Learning Objective")

st.info(
    """
    This machine learning model investigates whether
    **Years of Experience** can be used to predict
    **Teacher Rating**.

    Input:
    📈 Years of Experience

    Output:
    ⭐ Predicted Teacher Rating
    """
)


# ============================================================
# DATA PREPARATION
# ============================================================

X = ml_data[
    ["YearsOfExperience"]
]

y = ml_data[
    "TeacherRating"
]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

if len(ml_data) >= 5:

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )


    # ========================================================
    # CREATE MODEL
    # ========================================================

    model = LinearRegression()


    # ========================================================
    # TRAIN MODEL
    # ========================================================

    model.fit(
        X_train,
        y_train
    )


    # ========================================================
    # PREDICTION
    # ========================================================

    y_pred = model.predict(
        X_test
    )


    # ========================================================
    # MODEL METRICS
    # ========================================================

    mae = mean_absolute_error(
        y_test,
        y_pred
    )


    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            y_pred
        )
    )


    r2 = r2_score(
        y_test,
        y_pred
    )


    # ========================================================
    # MODEL KPI
    # ========================================================

    st.subheader(
        "📊 Model Performance"
    )


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "📚 Training Records",
        len(X_train)
    )


    col2.metric(
        "🧪 Testing Records",
        len(X_test)
    )


    col3.metric(
        "📐 MAE",
        round(mae, 3)
    )


    col4.metric(
        "🎯 R² Score",
        round(r2, 3)
    )


    st.divider()


    # ========================================================
    # MODEL PERFORMANCE EXPLANATION
    # ========================================================

    st.subheader(
        "🧠 Understanding the Model"
    )


    st.write(
        f"""
        **Mean Absolute Error (MAE):** {mae:.3f}

        On average, the model's prediction differs from
        the actual teacher rating by approximately
        **{mae:.3f} rating points**.

        **Root Mean Squared Error (RMSE):** {rmse:.3f}

        **R² Score:** {r2:.3f}

        R² indicates how much of the variation in teacher
        rating is explained by Years of Experience.
        """
    )


    # ========================================================
    # INTERACTIVE PREDICTION
    # ========================================================

    st.divider()

    st.subheader(
        "🎚️ Predict Teacher Rating"
    )


    min_experience = int(
        teachers["YearsOfExperience"].min()
    )


    max_experience = int(
        teachers["YearsOfExperience"].max()
    )


    selected_experience = st.slider(
        "📈 Select Years of Teaching Experience",
        min_value=min_experience,
        max_value=max_experience,
        value=min_experience
    )


    # Make prediction

    prediction = model.predict(
        pd.DataFrame(
            {
                "YearsOfExperience": [
                    selected_experience
                ]
            }
        )
    )[0]


    # Keep prediction within rating scale

    prediction = max(
        0,
        min(
            5,
            prediction
        )
    )


    # ========================================================
    # DISPLAY PREDICTION
    # ========================================================

    st.markdown(
        f"""
        <div class="prediction-card">

        <h2>
        🤖 Predicted Teacher Rating
        </h2>

        <div class="prediction-number">
        ⭐ {prediction:.2f}
        </div>

        <p>
        Based on {selected_experience} years
        of teaching experience
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()


    # ========================================================
    # ACTUAL VS PREDICTED
    # ========================================================

    st.subheader(
        "🎯 Actual vs Predicted Ratings"
    )


    prediction_data = pd.DataFrame(
        {
            "Actual Rating": y_test.values,
            "Predicted Rating": y_pred
        }
    )


    fig_actual = px.scatter(
        prediction_data,
        x="Actual Rating",
        y="Predicted Rating",
        title="Actual vs Predicted Teacher Ratings"
    )


    fig_actual.add_shape(
        type="line",
        x0=0,
        y0=0,
        x1=5,
        y1=5
    )


    fig_actual.update_layout(
        xaxis_title="Actual Teacher Rating",
        yaxis_title="Predicted Teacher Rating"
    )


    st.plotly_chart(
        fig_actual,
        use_container_width=True
    )


    st.divider()


    # ========================================================
    # EXPERIENCE VS RATING
    # ========================================================

    st.subheader(
        "📈 Experience vs Teacher Rating"
    )


    fig_experience = px.scatter(
        ml_data,
        x="YearsOfExperience",
        y="TeacherRating",
        title="Teaching Experience vs Teacher Rating",
        trendline=None
    )


    # Regression line manually

    x_values = np.linspace(
        ml_data[
            "YearsOfExperience"
        ].min(),

        ml_data[
            "YearsOfExperience"
        ].max(),

        100
    )


    y_values = model.predict(
        pd.DataFrame(
            {
                "YearsOfExperience": x_values
            }
        )
    )


    fig_experience.add_scatter(
        x=x_values,
        y=y_values,
        mode="lines",
        name="Regression Line"
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


    # ========================================================
    # MODEL EQUATION
    # ========================================================

    st.subheader(
        "📐 Linear Regression Equation"
    )


    coefficient = model.coef_[0]

    intercept = model.intercept_


    st.latex(
        rf"""
        TeacherRating =
        {coefficient:.4f}
        \times YearsOfExperience
        +
        {intercept:.4f}
        """
    )


    st.write(
        f"""
        **Coefficient:** {coefficient:.4f}

        **Intercept:** {intercept:.4f}
        """
    )


    if coefficient > 0:

        st.success(
            "📈 The model estimates a positive relationship "
            "between experience and teacher rating."
        )

    elif coefficient < 0:

        st.warning(
            "📉 The model estimates a negative relationship "
            "between experience and teacher rating."
        )

    else:

        st.info(
            "➡️ The model estimates almost no linear "
            "effect of experience on teacher rating."
        )


    st.divider()


    # ========================================================
    # PREDICTION TABLE
    # ========================================================

    st.subheader(
        "📋 Actual vs Predicted Data"
    )


    result = X_test.copy()


    result["ActualRating"] = y_test.values

    result["PredictedRating"] = y_pred

    result["PredictionError"] = (
        result["ActualRating"]
        -
        result["PredictedRating"]
    )


    result = result.sort_values(
        "YearsOfExperience"
    )


    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )


    st.divider()


    # ========================================================
    # FINAL INTERPRETATION
    # ========================================================

    st.subheader(
        "💡 ML Interpretation"
    )


    if r2 >= 0.7:

        interpretation = (
            "The model explains a large proportion of "
            "the variation in teacher ratings."
        )

    elif r2 >= 0.4:

        interpretation = (
            "The model explains a moderate proportion "
            "of the variation in teacher ratings."
        )

    elif r2 >= 0:

        interpretation = (
            "The model explains only a limited amount "
            "of the variation in teacher ratings."
        )

    else:

        interpretation = (
            "The model performs poorly for this dataset. "
            "Experience alone may not be sufficient "
            "to predict teacher rating."
        )


    st.markdown(
        f"""
        <div class="model-card">

        <h3>🤖 Model Finding</h3>

        <p>
        {interpretation}
        </p>

        <p>
        The R² score is <b>{r2:.3f}</b>,
        while the MAE is <b>{mae:.3f}</b>.
        </p>

        <p>
        Therefore, teacher rating should not necessarily
        be predicted using experience alone. Other factors
        such as expertise, course quality and teaching
        characteristics may also be important.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


else:

    st.error(
        "Not enough data available to train the model."
    )
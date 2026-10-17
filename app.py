
"""Streamlit interface for the AtliQ Credit Intelligence prototype."""

import pandas as pd
import streamlit as st

from src.baseline_experiment import FEATURES
from src.model_inference import (
    predict_positive_probability,
    train_inference_model,
)
from src.scorecard import probability_to_score, score_to_category

st.set_page_config(
    page_title="AtliQ Credit Intelligence",
    page_icon="📊",
    layout="centered",
)

st.title("AtliQ Credit Intelligence")
st.caption("Educational credit-classification prototype")

st.warning(
    "Experimental only. This model is not validated for real-world lending "
    "decisions, and its output is not a calibrated estimate of future default risk."
)

st.write(
    "Enter the five baseline features below to explore the model's output. "
    "Use realistic, non-identifying example values."
)

with st.form("applicant_form"):
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30,
        step=1,
    )
    income = st.number_input(
        "Income",
        min_value=0.0,
        value=40000.0,
        step=1000.0,
    )
    dependants = st.number_input(
        "Number of dependants",
        min_value=0,
        max_value=30,
        value=1,
        step=1,
    )
    years_at_address = st.number_input(
        "Years at current address",
        min_value=0.0,
        value=4.0,
        step=1.0,
    )
    bank_balance = st.number_input(
        "Bank balance at application",
        min_value=0.0,
        value=9000.0,
        step=500.0,
    )

    submitted = st.form_submit_button("Run experimental prediction")

@st.cache_resource
def get_inference_model():
    return train_inference_model()


if submitted:
    try:
        with st.spinner("Preparing the baseline model..."):
            model = get_inference_model()

        applicant = pd.DataFrame(
            [
                {
                    "age": age,
                    "income": income,
                    "number_of_dependants": dependants,
                    "years_at_current_address": years_at_address,
                    "bank_balance_at_application": bank_balance,
                }
            ],
            columns=FEATURES,
        )

        probability = predict_positive_probability(model, applicant)[0]


        score = probability_to_score(probability)
        category = score_to_category(score)

        st.subheader("Experimental scorecard output")

        score_col, probability_col = st.columns(2)

        with score_col:
            st.metric("Illustrative score", f"{score} / 900")
            st.caption(f"Category: {category}")

        with probability_col:
            st.metric("Positive-class probability", f"{probability:.1%}")

        with st.expander("How is this score calculated?"):
            st.latex(r"S = \operatorname{round}(900 - 600p)")
            st.write(
                "Here, p is the model's predicted probability for the "
                "positive class in the existing dataset labels."
            )
            st.markdown(
                "- **750–900:** Excellent\n"
                "- **650–749:** Good\n"
                "- **500–649:** Average\n"
                "- **300–499:** Poor"
            )

        st.info(
            "Educational prototype only. This score is a custom mathematical "
            "transformation of an experimental model output, not a validated "
            "or calibrated credit score. The probability is not a validated "
            "estimate of future default risk. Do not use this output to make "
            "real lending decisions."
        )


    except (ValueError, TypeError, KeyError) as exc:
        st.error(f"Could not generate the experimental output: {exc}")

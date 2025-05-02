import streamlit as st
import pandas as pd
import datetime
import os
st.set_page_config(page_title="UTAUT Survey", layout="centered")

st.title("📊 UTAUT-Based Technology Adoption Survey on Discourse App")

st.write("Please answer the following questions based on your experience.")

# Basic user info
name = st.text_input("Your Name")
email = st.text_input("Your Email")

# Likert scale options
scale = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]

def likert(question):
    return st.radio(question, scale, key=question)

st.header("1. Performance Expectancy (PE)")
pe1 = likert("The app helps me understand discussions more effectively.")
pe2 = likert("The mined discourse data is useful for research or decision-making in discourse analysis.")
pe3 = likert("The app provides insightful summaries or visualizations.")
pe4 = likert("I can easily extract meaningful information from short discussions.")
pe5 = likert("The app improves my ability to analyze online conversations.")

st.header("2. Effort Expectancy (EE)")
ee1 = likert("Learning to operate the system is easy for me.")
ee2 = likert("It is easy to navigate and use the features of the app.")
ee3 = likert("The user interface is intuitive and user-friendly.")
ee4 = likert("I do not need technical help to use this app.")

st.header("3. Feature Satisfaction")
si1 = likert("The discourse mining results are accurate and reliable.")
si2 = likert("The app provides relevant information on temporal order of event in the text.")
si3 = likert("The search and filtering functions work as expected.")

st.header("4. Engagement and Adoption")
fc1 = likert("I would recommend this app to colleagues or classmates who working on discourse analysis.")
fc2 = likert("I am satisfied with the overall performance of the app.")
fc3 = likert("I believe this app has potential for educational or research purposes.")

if os.path.exists("utaut_responses.csv"):
    df = pd.read_csv("utaut_responses.csv")
    st.subheader("All Responses")
    st.dataframe(df)

    # --- Download CSV ---
    st.download_button(
        label="Download Responses as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='responses.csv',
        mime='text/csv',
    )
# Submit
if st.button("Submit Survey"):
    if name.strip() == "" or email.strip() == "":
        st.warning("Please enter your name and email.")
    else:
        response = {
            "Timestamp": datetime.datetime.now(),
            "Name": name,
            "Email": email,
            "PE1": pe1, "PE2": pe2, "PE3": pe3, "PE4": pe4, "PE5": pe5,
            "EE1": ee1, "EE2": ee2, "EE3": ee3, "EE4": ee4,
            "SI1": si1, "SI2": si2, "SI3": si3,
            "FC1": fc1, "FC2": fc2, "FC3": fc3
        }

        df = pd.DataFrame([response])
        df.to_csv("utaut_responses.csv", mode="a", header=not pd.io.common.file_exists("utaut_responses.csv"), index=False)

        st.success("✅ Thank you! Your response has been recorded.")
import matplotlib.pyplot as plt

# Mapping Likert responses to numeric scale (optional)
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Helper function to plot a bar chart for a set of questions
def plot_likert_distribution(title, questions):
    counts = {}
    for q in questions:
        if q in df.columns:
            values = df[q].dropna()
            counts[q] = values.value_counts().reindex(scale, fill_value=0)

    fig, ax = plt.subplots()
    df_counts = pd.DataFrame(counts)
    df_counts.plot(kind='bar', ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Number of Responses")
    ax.set_xlabel("Response Scale")
    ax.legend(title="Questions")
    st.pyplot(fig)

# ---- Graph 1: Performance Expectancy ----

    # Show bar chart
st.subheader("📈 Performance Expectancy (PE)")
plot_likert_distribution("Performance Expectancy", ["PE1", "PE2", "PE3", "PE4", "PE5"])

# ---- Graph 2: Effort Expectancy ----
st.subheader("📉 Effort Expectancy (EE)")
plot_likert_distribution("Effort Expectancy", ["EE1", "EE2", "EE3", "EE4"])


# ---- Graph 3: Feature Satisfaction ----
st.subheader("📊 Feature Satisfaction")
plot_likert_distribution("Feature Satisfaction", ["SI1", "SI2", "SI3"])

# ---- Graph 4: Engagement and Adoption ----
st.subheader("📌 Engagement and Adoption")
plot_likert_distribution("Engagement and Adoption", ["FC1", "FC2", "FC3"])

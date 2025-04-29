import streamlit as st
import pandas as pd
import datetime

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
pe2 = likert("The app provides insightful summaries or visualizations.")
pe2 = likert("I can easily extract meaningful information from short discussions.")
pe2 = likert("The app improves my ability to analyze online conversations.")

st.header("2. Effort Expectancy (EE)")
ee1 = likert("Learning to operate the system is easy for me.")
ee2 = likert("It is easy to navigate and use the features of the app.")
ee2 = likert("The user interface is intuitive and user-friendly.")
ee2 = likert("I do not need technical help to use this app.")

st.header("3. Feature Satisfaction")
si1 = likert("The discourse mining results are accurate and reliable.")
si2 = likert("The app provides relevant information on temporal order of event in the text.")
si2 = likert("The search and filtering functions work as expected.")

st.header("4. Engagement and Adoption")
fc1 = likert("I would recommend this app to colleagues or classmates who working on discourse analysis.")
fc2 = likert("I am satisfied with the overall performance of the app.")
fc2 = likert("I believe this app has potential for educational or research purposes.")


# Submit
if st.button("Submit Survey"):
    if name.strip() == "" or email.strip() == "":
        st.warning("Please enter your name and email.")
    else:
        response = {
            "Timestamp": datetime.datetime.now(),
            "Name": name,
            "Email": email,
            "PE1": pe1, "PE2": pe2,
            "EE1": ee1, "EE2": ee2,
            "SI1": si1, "SI2": si2,
            "FC1": fc1, "FC2": fc2,
            
        }

        df = pd.DataFrame([response])
        df.to_csv("utaut_responses.csv", mode="a", header=not pd.io.common.file_exists("utaut_responses.csv"), index=False)

        st.success("✅ Thank you! Your response has been recorded.")

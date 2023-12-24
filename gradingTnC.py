import streamlit as st

# Grading System Criteria
grading_criteria = {
    'Clarity': {
        'description': 'How clearly are the terms presented?',
        'scale': ['Poor', 'Fair', 'Good', 'Excellent']
    },
    'Fairness': {
        'description': 'Are the terms fair to both parties (user and service provider)?',
        'scale': ['Unfair', 'Neutral', 'Fair', 'Very Fair']
    },
    'Transparency': {
        'description': 'How transparent are the terms about data usage and privacy?',
        'scale': ['Not Transparent', 'Somewhat Transparent', 'Transparent', 'Very Transparent']
    },
    'User-Friendliness': {
        'description': 'How user-friendly are the terms for the average user?',
        'scale': ['Not User-Friendly', 'Slightly User-Friendly', 'User-Friendly', 'Very User-Friendly']
    }
}

# Function to calculate the overall grade
def calculate_overall_grade(scores):
    total_score = 0
    for score in scores:
        total_score += score
    average_score = total_score / len(scores)

    if average_score < 2:
        return 'Poor'
    elif 2 <= average_score < 3:
        return 'Fair'
    elif 3 <= average_score < 3.5:
        return 'Good'
    else:
        return 'Excellent'

# Streamlit app
st.title("Website Terms and Conditions Grading Tool")

# User input
st.subheader("Rate the Website's Terms and Conditions:")
scores = {}
for criterion, details in grading_criteria.items():
    st.write(f"**{criterion}** - {details['description']}")
    score = st.radio(f"Rate {criterion}:", options=details['scale'])
    scores[criterion] = details['scale'].index(score) + 1

# Calculate and display the overall grade
overall_grade = calculate_overall_grade(list(scores.values()))
st.subheader("Overall Grade:")
st.write(f"The website's terms and conditions are rated as: **{overall_grade}**")

# You can further customize this app to save and analyze grading data.

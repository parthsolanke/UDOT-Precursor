import pandas as pd
import streamlit as st
import plotly.express as px
from classification import process_text
from app_config import StreamlitConfig
from label_config import label_descriptions, binary_labels

StreamlitConfig()

# Streamlit app
st.title("Terms and Conditions Analysis Tool")

terms_text = st.text_area("Enter the Terms and Conditions:", height=200)
submit_button = st.button("Submit")

if submit_button and terms_text:
    classified_sentences = process_text(terms_text)
    
    st.divider()
    st.subheader("Analysis:")
    labels = list(label_descriptions.keys())
    for label in labels:
        st.markdown(f"<span style='color: #f54242'><b>{label}:</b></span>",
                    unsafe_allow_html=True)
        st.markdown("\n".join([sentence['sentence'] for sentence in classified_sentences
                               if sentence['label'] == label]))
     
    st.divider()
    st.subheader("Data Insights:")  
    cols = st.columns(2)         
    # dataframe
    df = pd.DataFrame({'Label': labels})
    df['Count'] = df['Label'].apply(lambda label: len([sentence['sentence'] 
                                                       for sentence in classified_sentences
                                                       if sentence['label'] == label]))

    # bar chart
    bar_fig = px.bar(df, x='Label', y='Count', text='Count',
                     color_discrete_sequence=px.colors.sequential.RdBu)
    bar_fig.update_layout(width=500, height=400)
    bar_fig.update_traces(textfont_size=12, textangle=0,
                          textposition="outside", cliponaxis=False)
    cols[0].plotly_chart(bar_fig)
    
    # pie chart
    pie_fig = px.pie(df, names='Label', values='Count',
                     color_discrete_sequence=px.colors.sequential.RdBu)
    pie_fig.update_layout(width=500, height=400)
    cols[1].plotly_chart(pie_fig)
                


st.divider()  
st.markdown("**Label Descriptions:**")
for label, description in label_descriptions.items():
    st.markdown(f"- <span style='color: #f54242'><b>{label}:</b></span> {description}",
                unsafe_allow_html=True)

   

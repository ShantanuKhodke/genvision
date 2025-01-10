import streamlit as st
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

# Streamlit App
st.title("Social Media Engagement Analysis")

# User input
st.write("Choose your action:")
action = st.radio(
    "Would you like to analyze a specific post type or ask another question?",
    ("Analyze Specific Post Type", "Ask Another Question")
)

# Functions to create different visualizations
def plot_bar_chart(data):
    fig, ax = plt.subplots()
    sns.barplot(x='Post Type', y='Engagement', data=data, ax=ax)
    ax.set_title('Engagement by Post Type')
    st.pyplot(fig)

def plot_line_chart(data):
    fig = px.line(data, x='Date', y='Engagement', title='Engagement Over Time')
    st.plotly_chart(fig)

def plot_pie_chart(data):
    fig = px.pie(data, names='Post Type', values='Engagement', title='Engagement Distribution by Post Type')
    st.plotly_chart(fig)

def plot_visualization_based_on_question(question, data):
    # Check for specific keywords in the question and decide the type of chart
    if "engagement over time" in question.lower():
        plot_line_chart(data)
    elif "engagement distribution" in question.lower():
        plot_pie_chart(data)
    elif "engagement by post type" in question.lower():
        plot_bar_chart(data)
    else:
        st.warning("Sorry, I couldn't understand your question for visualization.")

if action == "Analyze Specific Post Type":
    post_type = st.text_input("Enter the post type (e.g., Reels, Carousel, Static Images):")
    if st.button("Analyze"):
        if post_type:
            # Make API request
            url = "https://api.langflow.astra.datastax.com/lf/6b263e67-6d5a-4f3a-8593-e25a03fc94be/api/v1/run/74af8e39-9541-42f3-b1d6-8986ad4431f1?stream=false"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer AstraCS:kJCdcGzHLysKAiCZAKwiNRZl:51eaaab0a6aba52c59c94dba29b69b1ad024ab9ba44213836a4ad87783c6de87"
            }
            payload = {
                "input_value": post_type,
                "output_type": "chat",
                "input_type": "chat"
            }
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                result = response.json()

                if "outputs" in result and isinstance(result["outputs"], list):
                    outputs = result["outputs"][0]
                    if "outputs" in outputs and isinstance(outputs["outputs"], list):
                        inner_output = outputs["outputs"][0]
                        answer = inner_output["results"]["message"]["text"]
                        st.success("Analysis Results:")
                        st.write(answer)

                        # Example Data for visualization (replace this with actual data from API)
                        data = pd.DataFrame({
                            'Post Type': ['Reels', 'Carousel', 'Static Images'],
                            'Engagement': [120, 85, 75],
                            'Date': pd.date_range(start='2025-01-01', periods=3, freq='D')
                        })

                        # Visualizations
                        plot_bar_chart(data)
                        plot_line_chart(data)
                        plot_pie_chart(data)
                    else:
                        st.warning("No valid results found in the response.")
                else:
                    st.warning("Invalid response structure.")
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        else:
            st.warning("Please enter a post type.")
else:
    question = st.text_area("Ask your question about social media engagement analysis:", key="custom_question")

    if action == 'Ask Another Question':
        if st.button("Analyze"):
            if question:
                # Make API request
                url = "https://api.langflow.astra.datastax.com/lf/6b263e67-6d5a-4f3a-8593-e25a03fc94be/api/v1/run/74af8e39-9541-42f3-b1d6-8986ad4431f1?stream=false"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer AstraCS:kJCdcGzHLysKAiCZAKwiNRZl:51eaaab0a6aba52c59c94dba29b69b1ad024ab9ba44213836a4ad87783c6de87"
                }
                payload = {
                    "input_value": question,
                    "output_type": "chat",
                    "input_type": "chat"
                }
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 200:
                    result = response.json()

                    if "outputs" in result and isinstance(result["outputs"], list):
                        outputs = result["outputs"][0]
                        if "outputs" in outputs and isinstance(outputs["outputs"], list):
                            inner_output = outputs["outputs"][0]
                            answer = inner_output["results"]["message"]["text"]
                            st.success("Analysis Results:")
                            st.write(answer)

                            # Example Data for visualization (replace this with actual data from API)
                            data = pd.DataFrame({
                                'Post Type': ['Reels', 'Carousel', 'Static Images'],
                                'Engagement': [120, 85, 75],
                                'Date': pd.date_range(start='2025-01-01', periods=3, freq='D')
                            })

                            # Visualize based on the question input
                            plot_visualization_based_on_question(question, data)

                        else:
                            st.warning("No valid results found in the response.")
                    else:
                        st.warning("Invalid response structure.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            else:
                st.warning("Please enter a question")
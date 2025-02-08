"""
main.py

This is the entry point for the Podcast Summary App. It uses Streamlit to create a simple
web interface that accepts a YouTube podcast URL and a Slack channel name. When the user
submits the form, the app instantiates the PodSumCrew (defined in Podcast_Summarizer_AI_Agent.py)
and kicks off the process to transcribe, summarize, and send the summary via Slack.

Usage:
    streamlit run main.py
"""

# Import the PodSumCrew class from the main agent module.
from Podcast_Summarizer_AI_Agent import PodSumCrew
import streamlit as st

# Configure the Streamlit page settings.
st.set_page_config(page_title="Podcast Summary App", layout="centered")

def run():
    """
    Runs the Podcast Summary App.

    This function renders the UI elements using Streamlit, collects user inputs, and
    invokes the PodSumCrew to process the podcast URL and Slack channel.
    """
    # Display the title on the app.
    st.title("Podcast Summary App")

    # Create text input fields for the YouTube URL and Slack channel.
    podcast_url = st.text_input("Enter the URL of the Podcast you want to summarize")
    slack_channel = st.text_input("Enter the Slack channel name")

    # When the button is clicked, validate the inputs and trigger the summarization process.
    if st.button("Summarize Podcast"):
        if podcast_url and slack_channel:
            # Prepare inputs for the PodSumCrew.
            inputs = {'youtube_url': podcast_url, "slack_channel": slack_channel}
            # Kick off the process and capture the result.
            result = PodSumCrew().crew().kickoff(inputs=inputs)
            # Display the result on the page.
            st.write(result)
        else:
            st.write("Podcast URL or Slack channel is empty")

# Run the app if this file is executed directly.
if __name__ == "__main__":
    run()

import streamlit as st
from streamlit_chat import message
import openai
import speech_recognition as sr
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
import threading
import json
from langchain_community.llms import OpenAI

# Set up OpenAI API key
openai.api_key = "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"

# Function for speech-to-text processing
def recognize_speech(recognizer, microphone):
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Unable to recognize speech."
    except sr.RequestError as e:
        return f"Speech recognition service error: {e}"

# Define the Streamlit app
def main():
    st.title("Real-Time Speech Analysis and Sales Optimization")
    st.sidebar.title("TASKS")
    st.sidebar.write("1. Real-Time Sentiment Analysis\n2. Product Recommendation & Objection Handling\n3. Dashboard")

    # Real-Time Sentiment Analysis
    st.header("Real-Time Sentiment Analysis")
    st.write("Detect sentiment shifts in live sales calls using LLMs.")

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    real_time_transcript = st.empty()
    sentiment_display = st.empty()
    insights_display = st.empty()
    recommendation_display = st.empty()
    summary_display = st.empty()

    def process_audio_stream():
        crm_data = {"customer_profile": "Tech Enthusiast", "purchase_history": ["Laptop", "Smartphone"]}
        while True:
            transcript = recognize_speech(recognizer, microphone)
            if transcript:
                real_time_transcript.markdown(f"### Transcript: {transcript}")

                # Simulated sentiment analysis (replace with your model)
                if "good" in transcript or "great" in transcript:
                    sentiment = "Positive"
                elif "bad" in transcript or "problem" in transcript:
                    sentiment = "Negative"
                else:
                    sentiment = "Neutral"

                sentiment_display.markdown(f"### Detected Sentiment: {sentiment}")

                # Display actionable insights
                insights_display.markdown("### Actionable Insights:")
                if sentiment == "Positive":
                    insights_display.write("- Maintain a positive tone and highlight relevant product features.")
                elif sentiment == "Negative":
                    insights_display.write("- Address customer concerns empathetically and offer solutions.")
                    insights_display.write("- Avoid pushing sales; focus on rebuilding trust.")
                elif sentiment == "Neutral":
                    insights_display.write("- Engage the customer with questions to understand their needs.")
                    insights_display.write("- Provide information to guide the conversation positively.")

                # Product Recommendation & Dynamic Question Handling
                recommendations = ["Wireless Earbuds", "Smartwatch"]
                dynamic_questions = ["Would you like to explore accessories for your smartphone?", "Do you need extended warranty options?"]

                recommendation_display.markdown("### Real-Time Product Recommendations and Questions:")
                recommendation_display.write("#### Recommendations:")
                for rec in recommendations:
                    recommendation_display.write(f"- {rec}")
                recommendation_display.write("#### Dynamic Questions:")
                for q in dynamic_questions:
                    recommendation_display.write(f"- {q}")

                #Real-Time Post-Call Summary
                summary = {
                    "Transcript": transcript,
                    "Sentiment": sentiment,
                    "Recommendations": recommendations,
                    "Dynamic Questions": dynamic_questions
                }
                summary_display.markdown("### Real-Time Post-Call Summary:")
                summary_display.write(json.dumps(summary, indent=4))

    if st.button("Start Real-Time Analysis"):
        st.info("Listening for live speech. Speak into your microphone.")
        threading.Thread(target=process_audio_stream).start()

    st.sidebar.title("About")
    st.sidebar.info("This app demonstrates real-time speech analysis, sentiment detection (Positive, Negative, Neutral), product recommendations, and sales optimization using LLMs.")

if __name__ == "__main__":
    main()

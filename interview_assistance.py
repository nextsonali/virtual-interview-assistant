import streamlit as st
import random
import os
import datetime
from audio_recorder_streamlit import audio_recorder

# Directory to save recordings
SAVE_DIR = "interview_answers"
os.makedirs(SAVE_DIR, exist_ok=True)

# Question List
ALL_QUESTIONS = [
    "1. Tell me about yourself",
    "2. How your org structure looks like?",
    "3. What are your Responsibilities",
    "4. What are your strengths?",    
    "5. What are your Weaknesses",
    "6. What are the top three leadership skills you learned in your mgmt journey?",
    "7. How do you keep yourself up to date",
    "8. Tell me a time you failed?",
    "9. Share some of the critical feedback you received recently",
    "10. Why are you looking out?",
    "11. How do you motivate your team?",
    "12. How to build a trusted relationship with the employees", 
    "13. How do you identify a leader in your team to grow?", 
    "14. How do you grow your employees?",
    "15. How do you make your one-on-one effective?",
    "16. How to build a high performing team?", 
    "17. How do you make a low performing team achieve high goals?", 
    "18. What are things you do to have a effective global team?",
]

# Initialize session state
if "remaining_questions" not in st.session_state:
    st.session_state.remaining_questions = ALL_QUESTIONS.copy()

def get_random_question():
    if not st.session_state.remaining_questions:
        return None
    question = random.choice(st.session_state.remaining_questions)
    st.session_state.remaining_questions.remove(question)
    return question

st.title("🎤 Virtual Interview Assistant")
st.subheader("Your question:")

if "current_question" not in st.session_state:
    st.session_state.current_question = get_random_question()

if st.session_state.current_question:
    st.write(f"**{st.session_state.current_question}**")
    
    # Record audio answer
    audio_data = audio_recorder(
        sample_rate=44100,  # Higher sample rate for better quality
        pause_threshold=10.0,  # Stops recording after 10 seconds of silence
        text="Click to record your answer",  # Button text
        recording_color="#FF0000",  # Highlight when recording
        neutral_color="#AAAAAA",  # Default color
        icon_name="microphone"
    )
    if audio_data:
        st.audio(audio_data, format="audio/wav")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(SAVE_DIR, f"{timestamp}.wav")
        with open(filename, "wb") as f:
            f.write(audio_data)
        st.success(f"✅ Answer saved: {filename}")

    if st.button("Next Question"):
        st.session_state.current_question = get_random_question()
        st.rerun()
else:
    st.write("✅ No more questions available!")

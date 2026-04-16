import streamlit as st
import pandas as pd
import datetime
import os

# --- Configuration & File Path ---
st.set_page_config(page_title="Student Feedback Portal", page_icon="🎓")
FILE_PATH = "data/raw/teaching_quality_dataset.csv"

# --- Data Mapping ---
courses = ["DSA", "OS", "How Humans languagues work", "Tools and Technique"]
mentor_map = {
    "DSA": "Ojas",
    "OS": "Shivam",
    "How Humans languagues work": "Sai",
    "Tools and Technique": "Sai"
}

# --- App Header ---
st.title("🎓 Real-Time Student Feedback Portal")
st.markdown("Welcome! Please fill out the survey below. The data goes directly into our analytics pipeline to improve course quality.")

# Course Selection Outside the Form
course = st.selectbox("Select Course", courses)
mentor = mentor_map[course]
st.write(f"**Assigned Mentor:** {mentor}")

# --- Feedback Form ---
with st.form("feedback_form", clear_on_submit=True):
    st.subheader("Submit Your Feedback")
    
    student_id = st.text_input("Student ID (e.g., S999)")
    
    score = st.slider("Feedback Score (1 = Poor, 5 = Excellent)", 1.0, 5.0, 3.0, step=0.1)
    review = st.text_area("Any textual review or comments?")
    attendance = st.slider("Your approximate Attendance Rate (%)", 0, 100, 75)
    
    submitted = st.form_submit_button("Submit Survey")
    
    if submitted:
        if student_id == "":
            st.error("Please enter a valid Student ID.")
        else:
            # Prepare new row dictionary matching exactly the CSV header
            new_data = {
                "student_id": student_id,
                "course_id": course,
                "instructor_id": mentor,
                "feedback_score": score,
                "textual_review": review,
                "attendance_rate": attendance,
                # Setting defaults/mocks for backend metrics not asked in the form
                "assignment_submission_rate": 80,
                "quiz_avg_score": 75,
                "exam_avg_score": 75,
                "lms_logins_past_month": 15,
                "avg_session_duration_minutes": 20,
                "forum_participation_count": 5,
                "video_completion_rate": 80,
                "instructor_response_time": 24,
                "risk_level": "Low" if score > 3.0 else "High"
            }
            
            # Load, Append, and Save Data
            if os.path.exists(FILE_PATH):
                df = pd.read_csv(FILE_PATH)
                df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                df.to_csv(FILE_PATH, index=False)
                
                st.success(f"Thank you, {student_id}! Your feedback for {course} with {mentor} has been recorded.")
                st.balloons()
            else:
                st.error("Error: Dataset file not found in 'data/raw/'.")

# --- Dashboard Display ---
st.markdown("---")
st.subheader("Live Form Submissions Preview")
if os.path.exists(FILE_PATH):
    df_preview = pd.read_csv(FILE_PATH)
    # Show only relevant columns and the last 5 entries (most recent first)
    st.dataframe(df_preview[['student_id', 'course_id', 'instructor_id', 'feedback_score', 'attendance_rate']].tail(5))
else:
    st.write("No data found.")

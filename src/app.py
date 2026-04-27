import streamlit as st
import pandas as pd
import datetime
import os
import sys

# Ensure src directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import RAW_DATA_PATH, COURSES, COURSE_MENTOR_MAP

# --- Configuration & File Path ---
st.set_page_config(page_title="Academic Feedback Portal", layout="wide", initial_sidebar_state="expanded")
FILE_PATH = RAW_DATA_PATH

# --- Styling ---
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .card-header { font-weight: bold; color: #7f8c8d; text-transform: uppercase; font-size: 0.85rem; }
    </style>
""", unsafe_allow_html=True)

# --- Data Mapping ---
courses = COURSES
mentor_map = COURSE_MENTOR_MAP

# --- Application Header ---
st.title("Academic Quality & Feedback Portal")
st.markdown("Submit live evaluation data to update the institutional performance dashboards in real-time.")
st.markdown("---")

# --- Layout Definition ---
col_form, col_dashboard = st.columns([1, 2], gap="large")

with col_form:
    st.subheader("Data Entry: Evaluation Form")
    st.markdown("Please complete all fields to submit an official course review.")
    
    # Selection logic outside form for real-time mentor mapping
    selected_course = st.selectbox("Academic Subject", courses, help="Select the subject you are currently evaluating.")
    assigned_mentor = mentor_map[selected_course]
    
    st.info(f"**Instructor of Record:** {assigned_mentor}")
    
    with st.form("professional_feedback_form", clear_on_submit=True):
        
        student_id = st.text_input("Matriculation ID (e.g., S1050)")
        
        st.markdown("##### Assessment Metrics")
        score = st.slider("Teaching Quality Score", min_value=1.0, max_value=5.0, value=3.0, step=0.1, help="1.0 constitutes poor quality, 5.0 constitutes academic excellence.")
        attendance = st.slider("Approximate Attendance Rate (%)", min_value=0, max_value=100, value=75, step=5)
        
        st.markdown("##### Qualitative Feedback")
        review = st.text_area("Provide a detailed textual review regarding the course structure and delivery.")
        
        # Submit block
        submitted = st.form_submit_button("Submit Evaluation", use_container_width=True)
        
        if submitted:
            if not student_id.strip().upper().startswith("S"):
                st.error("Validation Error: Please enter a valid Matriculation ID starting with 'S' (e.g., S1050).")
            else:
                new_data = {
                    "student_id": student_id.strip().upper(),
                    "course_id": selected_course,
                    "instructor_id": assigned_mentor,
                    "feedback_score": float(score),
                    "textual_review": review.strip(),
                    "attendance_rate": int(attendance),
                    "assignment_submission_rate": 80,
                    "quiz_avg_score": 75,
                    "exam_avg_score": 75,
                    "lms_logins_past_month": 15,
                    "avg_session_duration_minutes": 20,
                    "forum_participation_count": 5,
                    "video_completion_rate": 80,
                    "instructor_response_time": 24,
                    "risk_level": "Low" if score >= 3.0 else "High"
                }
                
                if os.path.exists(FILE_PATH):
                    df_append = pd.read_csv(FILE_PATH)
                    df_append = pd.concat([df_append, pd.DataFrame([new_data])], ignore_index=True)
                    df_append.to_csv(FILE_PATH, index=False)
                    st.success("Transaction Complete: Evaluation recorded successfully.")
                else:
                    st.error("System Error: Backend dataset file unreachable.")

with col_dashboard:
    st.subheader("Live Operational Dashboard")
    st.markdown("Aggregated metrics based on the current raw dataset processing.")
    
    if os.path.exists(FILE_PATH):
        df_live = pd.read_csv(FILE_PATH)
        
        # Calculate dynamic metrics
        total_evaluations = len(df_live)
        avg_score = df_live['feedback_score'].mean()
        avg_attendance = df_live['attendance_rate'].mean()
        risk_entries = len(df_live[df_live['risk_level'] == 'High'])
        
        # Render Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Evaluations", f"{total_evaluations:,}")
        m2.metric("Mean Quality Score", f"{avg_score:.2f} / 5.0")
        m3.metric("Mean Attendance", f"{avg_attendance:.1f}%")
        m4.metric("High Risk Flags", f"{risk_entries}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- Interactive Data Visualizations ---
        st.markdown("<span class='card-header'>📊 Visual Analytics: Course Comparison</span>", unsafe_allow_html=True)
        
        course_agg = df_live.groupby(['course_id', 'instructor_id']).agg(
            evaluations=('student_id', 'count'),
            avg_score=('feedback_score', 'mean'),
            avg_attendance=('attendance_rate', 'mean')
        ).reset_index()
        
        # Native Streamlit Chart (Interactive)
        chart_data = course_agg.set_index('course_id')[['avg_score']]
        st.bar_chart(chart_data, color="#3498db")
        
        # --- Formatted Data Tables ---
        st.markdown("<span class='card-header'>📈 Course Performance Breakdown</span>", unsafe_allow_html=True)
        
        # Use pandas Styler to add color gradients to the dataframe for creativity
        formatted_df = course_agg.style.background_gradient(subset=['avg_score'], cmap='Blues').format({
            'avg_score': "{:.2f}",
            'avg_attendance': "{:.1f}%"
        })
        st.dataframe(formatted_df, use_container_width=True, hide_index=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hide raw logs inside a sleek expander (dropdown)
        with st.expander("🔍 Reveal Recent Raw Transactions (T-5)", expanded=False):
            display_columns = ['student_id', 'course_id', 'instructor_id', 'feedback_score', 'attendance_rate', 'risk_level']
            st.dataframe(
                df_live[display_columns].tail(5).sort_index(ascending=False), 
                use_container_width=True,
                hide_index=True
            )
        
    else:
        st.warning("Awaiting database connection to generate analytics.")

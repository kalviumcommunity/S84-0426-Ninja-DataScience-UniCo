import streamlit as st
import pandas as pd
import datetime
import os
import sys
import plotly.express as px
import plotly.graph_objects as go

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
        
        # Calculate deltas (mocked against a previous baseline for visual effect)
        avg_score_delta = round(avg_score - 3.5, 2)
        avg_attendance_delta = round(avg_attendance - 70, 1)
        
        m1.metric("Total Evaluations", f"{total_evaluations:,}", delta=f"+{len(df_live.tail(10))} recent")
        m2.metric("Mean Quality Score", f"{avg_score:.2f} / 5.0", delta=avg_score_delta)
        m3.metric("Mean Attendance", f"{avg_attendance:.1f}%", delta=f"{avg_attendance_delta}%")
        m4.metric("High Risk Flags", f"{risk_entries}", delta="Action Required" if risk_entries > 0 else "All Good", delta_color="inverse")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- Interactive Data Visualizations ---
        st.markdown("<span class='card-header'>📊 Visual Analytics: Course Comparison</span>", unsafe_allow_html=True)
        
        # Tabs for different graph views
        tab1, tab2, tab3 = st.tabs(["Quality Scores", "Attendance Trends", "Instructor Risk Analysis"])
        
        with tab1:
            course_agg = df_live.groupby(['course_id', 'instructor_id']).agg(
                evaluations=('student_id', 'count'),
                avg_score=('feedback_score', 'mean'),
                avg_attendance=('attendance_rate', 'mean')
            ).reset_index()
            
            fig1 = px.bar(course_agg, x='course_id', y='avg_score', color='instructor_id',
                         title="Average Quality Score by Course",
                         labels={'course_id': 'Course', 'avg_score': 'Average Score (out of 5)'},
                         text_auto='.2f', color_discrete_sequence=px.colors.qualitative.Pastel)
            fig1.update_layout(yaxis_range=[0, 5])
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            fig2 = px.box(df_live, x='course_id', y='attendance_rate', color='course_id',
                          title="Attendance Rate Distribution by Course",
                          labels={'course_id': 'Course', 'attendance_rate': 'Attendance Rate (%)'})
            st.plotly_chart(fig2, use_container_width=True)
            
        with tab3:
            risk_counts = df_live['risk_level'].value_counts().reset_index()
            risk_counts.columns = ['Risk Level', 'Count']
            fig3 = px.pie(risk_counts, names='Risk Level', values='Count', 
                          title="Overall Risk Distribution",
                          color='Risk Level', color_discrete_map={'Low': '#2ecc71', 'High': '#e74c3c'},
                          hole=0.4)
            st.plotly_chart(fig3, use_container_width=True)
            
        # Optional: Radar chart for multi-dimensional metrics
        st.markdown("<span class='card-header'>🕸 Multi-metric Course Radar</span>", unsafe_allow_html=True)
        radar_df = pd.DataFrame(dict(
            r=[avg_score/5*100, avg_attendance,  df_live['assignment_submission_rate'].mean(), df_live['quiz_avg_score'].mean(), df_live['video_completion_rate'].mean()],
            theta=['Teaching Quality %', 'Attendance %', 'Assignments %', 'Quiz Avg %', 'Video Completion %']
        ))
        fig4 = go.Figure(data=go.Scatterpolar(
            r=radar_df['r'],
            theta=radar_df['theta'],
            fill='toself',
            name='Institutional Average',
            line_color='#9b59b6'
        ))
        fig4.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig4, use_container_width=True)

        # --- Formatted Data Tables ---
        st.markdown("<span class='card-header'>📈 Course Performance Breakdown</span>", unsafe_allow_html=True)
        
        # Add formatting without requiring matplotlib
        formatted_df = course_agg.style.format({
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

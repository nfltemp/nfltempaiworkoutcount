import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
from exercise_utils import (
    EXERCISES,
    analyze_pushup,
    analyze_squat,
    analyze_curl,
    analyze_plank,
    analyze_pullup,
    analyze_lunge,
    analyze_press,
    analyze_row
)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

def main():
    st.set_page_config(page_title="AI Fitness Trainer", layout="wide")
    
    # Initialize session state variables
    if 'rep_count' not in st.session_state:
        st.session_state.rep_count = 0
    if 'set_count' not in st.session_state:
        st.session_state.set_count = 1
    if 'total_reps' not in st.session_state:
        st.session_state.total_reps = 0
    if 'exercise_state' not in st.session_state:
        st.session_state.exercise_state = 'ready'
    if 'form_score' not in st.session_state:
        st.session_state.form_score = 100
    if 'feedback' not in st.session_state:
        st.session_state.feedback = ''
    if 'last_rep_time' not in st.session_state:
        st.session_state.last_rep_time = time.time()
    if 'avg_rep_time' not in st.session_state:
        st.session_state.avg_rep_time = 0

    # App title and description
    st.title("AI Fitness Trainer")
    st.markdown("Real-time pose estimation and form correction")

    # Sidebar for exercise selection and settings
    with st.sidebar:
        st.header("Settings")
        
        # Exercise selection
        selected_exercise = st.selectbox(
            "Select Exercise",
            list(EXERCISES.keys()),
            format_func=lambda x: EXERCISES[x]['name']
        )
        
        # Confidence threshold
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
        
        # Feedback sensitivity
        feedback_sensitivity = st.slider(
            "Feedback Sensitivity",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1
        )
        
        # Reset button
        if st.button("Reset Workout"):
            st.session_state.rep_count = 0
            st.session_state.set_count = 1
            st.session_state.total_reps = 0
            st.session_state.exercise_state = 'ready'
            st.session_state.form_score = 100
            st.session_state.feedback = ''
        
        # Complete set button
        if st.button("Complete Set"):
            st.session_state.set_count += 1
            st.session_state.rep_count = 0
            st.session_state.exercise_state = 'ready'

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        # Video feed placeholder
        video_placeholder = st.empty()
        
    with col2:
        # Stats and feedback
        st.subheader("Progress")
        stats_cols = st.columns(2)
        with stats_cols[0]:
            st.metric("Reps", st.session_state.rep_count)
        with stats_cols[1]:
            st.metric("Sets", st.session_state.set_count)
        
        st.subheader("Form Score")
        st.progress(st.session_state.form_score / 100)
        st.metric("Score", f"{st.session_state.form_score}%")
        
        st.subheader("Feedback")
        st.info(st.session_state.feedback or "Ready to start!")
        
        st.subheader("Session Stats")
        st.text(f"Total Reps: {st.session_state.total_reps}")
        st.text(f"Avg Rep Time: {st.session_state.avg_rep_time:.1f}s")
        st.text(f"Current Exercise: {EXERCISES[selected_exercise]['name']}")

    # Video capture and processing
    cap = cv2.VideoCapture(0)
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to access webcam")
                break

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame with MediaPipe
            results = pose.process(frame_rgb)
            
            if results.pose_landmarks:
                # Draw skeleton
                mp_drawing.draw_landmarks(
                    frame_rgb,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )
                
                # Analyze exercise
                landmarks = results.pose_landmarks.landmark
                
                # Get exercise analysis function
                analysis_funcs = {
                    'pushup': analyze_pushup,
                    'squat': analyze_squat,
                    'curl': analyze_curl,
                    'plank': analyze_plank,
                    'pullup': analyze_pullup,
                    'lunge': analyze_lunge,
                    'press': analyze_press,
                    'row': analyze_row
                }
                
                if selected_exercise in analysis_funcs:
                    new_state, form_score, feedback = analysis_funcs[selected_exercise](landmarks)
                    
                    # Update state and count reps
                    if new_state != st.session_state.exercise_state:
                        if new_state == 'up' and st.session_state.exercise_state == 'down':
                            current_time = time.time()
                            if current_time - st.session_state.last_rep_time > 1:  # Prevent double counting
                                st.session_state.rep_count += 1
                                st.session_state.total_reps += 1
                                
                                # Update average rep time
                                if st.session_state.rep_count > 1:
                                    rep_time = current_time - st.session_state.last_rep_time
                                    st.session_state.avg_rep_time = (
                                        st.session_state.avg_rep_time + rep_time
                                    ) / 2
                                
                                st.session_state.last_rep_time = current_time
                        
                        st.session_state.exercise_state = new_state
                    
                    st.session_state.form_score = form_score
                    st.session_state.feedback = feedback

            # Display the frame
            video_placeholder.image(frame_rgb, channels="RGB", use_column_width=True)

    finally:
        cap.release()

if __name__ == "__main__":
    main() 
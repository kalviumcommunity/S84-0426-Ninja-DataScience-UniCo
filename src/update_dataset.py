import pandas as pd
import random
import os
import sys

# Ensure src directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import RAW_DATA_PATH, PROCESSED_DATA_PATH, COURSES, COURSE_MENTOR_MAP

# New Courses and mappings
course_to_mentor = COURSE_MENTOR_MAP
courses = COURSES

def transform_dataset(filepath):
    # Load dataset
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    df = pd.read_csv(filepath)
    
    # Assign new courses randomly
    df['course_id'] = [random.choice(courses) for _ in range(len(df))]
    
    # Map the mentor based on the assigned course
    df['instructor_id'] = df['course_id'].map(course_to_mentor)
    
    # Optional: Slightly tweak feedback text based on new topics (keep basic for now)
    
    # Save back to CSV
    df.to_csv(filepath, index=False)
    print(f"Successfully transformed dataset at: {filepath}")

if __name__ == "__main__":
    # Transform raw
    transform_dataset(RAW_DATA_PATH)
    
    # If processed exists, you can rebuild it via src/data_utils.py later
    # But let's also transform it if it's there
    if os.path.exists(PROCESSED_DATA_PATH):
        transform_dataset(PROCESSED_DATA_PATH)
    
    print("Dataset populated with real-world names and subjects!")

import pandas as pd
import random
import os

# New Courses and mappings
course_to_mentor = {
    "DSA": "Ojas",
    "OS": "Shivam",
    "How Humans languagues work": "Sai",
    "Tools and Technique": "Sai"
}
courses = list(course_to_mentor.keys())

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
    transform_dataset('data/raw/teaching_quality_dataset.csv')
    
    # If processed exists, you can rebuild it via src/data_utils.py later
    # But let's also transform it if it's there
    if os.path.exists('data/processed/teaching_quality_clean.csv'):
        transform_dataset('data/processed/teaching_quality_clean.csv')
    
    print("Dataset populated with real-world names and subjects!")

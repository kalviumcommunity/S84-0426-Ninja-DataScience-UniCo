import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "teaching_quality_dataset.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_DIR, "processed", "teaching_quality_clean.csv")

# Constants
COURSE_MENTOR_MAP = {
    "DSA": "Ojas",
    "OS": "Shivam",
    "How Humans Languages Work": "Sai",
    "Tools and Technique": "Sai"
}
COURSES = list(COURSE_MENTOR_MAP.keys())

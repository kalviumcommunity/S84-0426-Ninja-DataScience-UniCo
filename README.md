# Teaching Quality & Student Engagement Analysis...

> **Problem Statement:** Universities gather feedback surveys but rarely extract actionable insights on teaching quality, course difficulty, or student satisfaction. How can data-driven dashboards make academic improvements measurable?

This project processes raw student survey responses through a complete Data Science lifecycle to generate structured, actionable insights regarding teaching effectiveness and student engagement.

---

## Key Insights
Based on exploratory data analysis and visualization:
* **Engagement Correlation:** A positive correlation exists between student attendance rates and teaching feedback scores, indicating that disengaged students (lower attendance) often report lower satisfaction.
* **Performance Baselines:** By establishing a statistical mean for teaching feedback, the university gains a measurable key performance indicator (KPI) to track the success of faculty training and course redesigns.
* **Quality Distribution:** Visualizing feedback distribution (via histograms) identifies courses falling significantly below the university average, highlighting areas requiring immediate intervention.

---

## Project Structure
The repository is organized following standard data science practices:

```text
S84-0426-Ninja-DataScience-UniCo/
│
├── data/
│   ├── raw/             # Original datasets
│   └── processed/       # Cleaned, standardized datasets
│
├── notebooks/
│   ├── 01_data_exploration.ipynb   # Cleaning, summaries, and missing value handling
│   └── 02_data_visualization.ipynb # Matplotlib & Seaborn visual EDA
│
├── src/
│   ├── app.py           # Real-Time Streamlit Feedback App
│   ├── data_utils.py    # Reusable Python scripts for data processing
│   └── update_dataset.py# Mentors and Courses updater script
│
└── README.md            # Project documentation
```

---

## Technology Stack
- **Language:** Python 3.12.7
- **Environment Management:** Conda 24.1.2
- **Data Manipulation:** Pandas, NumPy
- **Visualizations:** Matplotlib, Seaborn
- **Workspace:** Jupyter Notebooks

---

## Quick Start Guide

**1. Create and activate the conda environment:**
```bash
conda create -n unico-env python=3.12 pandas numpy jupyter matplotlib seaborn -y
conda activate unico-env
```

**2. Clean the dataset using the utility script:**
```bash
python src/data_utils.py
```

**3. Collect live student feedback via the Web Portal:**
```bash
streamlit run src/app.py
```
This opens an interactive, real-world web form where students can review mentors (Sai, Ojas, Shivam) and courses. Data syncs instantly with the CSV folder!

**4. Run the Jupyter Notebooks:**
Open and run `01_data_exploration.ipynb` and `02_data_visualization.ipynb` directly in your IDE to reproduce the analysis and charts.

---

## Future Roadmap (MVP)
1. **Real-time Survey Integration:** Replace the static dataset with an automated pipeline collecting live student feedback.
2. **Interactive Dashboards:** Transition from static Seaborn visualisations to an interactive dashboard (e.g., Tableau or PowerBI) for university administrators.
3. **Sentiment Analysis:** Implement Natural Language Processing (NLP) on open-text feedback to systematically quantify qualitative student sentiment.

---

# Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

# Guidelines:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request



<!-- TODO: Details for feature/exploratory-visualizations -->


<!-- TODO: Details for fix/handle-missing-values -->


<!-- TODO: Details for feature/preprocessing-pipeline -->

 
<!-- TODO: Details for feature/logging-setup -->
 
 
 
<!-- TODO: Details for experimental/new-algorithm-test -->
 
<!-- TODO: Details for feature/model-evaluation-metrics -->
 
 
<!-- TODO: Details for feature/dashboard-components -->

 
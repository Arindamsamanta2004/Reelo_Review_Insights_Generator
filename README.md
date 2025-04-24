AI-Powered Review Insights Generator 🤖✨
A powerful tool that analyzes customer reviews using Hugging Face's AI models to provide comprehensive insights, sentiment analysis, and detailed summaries.

Features 🚀
Advanced sentiment analysis using emotion detection

Aspect-based review categorization (e.g., food, service, ambiance, value)

Automated summary generation

Actionable recommendations based on patterns

Interactive visualizations with dashboards

Downloadable, shareable analysis reports

Real-time processing for instant insights

Setup 🛠️
Clone this repository

Install dependencies:

bash
Copy code
pip install -r requirements.txt
Usage 📝
Run the Streamlit app:

bash
Copy code
streamlit run app.py
Open your browser and go to the displayed local URL

Upload your CSV file containing reviews

Click 'Generate Insights' to analyze the reviews using Hugging Face AI

CSV Format 📋
Your CSV file should have a column named review with the review content.

Example:

csv
Copy code
review
"Great service and amazing food!"
"The wait time was too long"
Features in Detail 🔍
Sentiment Analysis: Detects emotional tone (happy, angry, neutral, etc.)

Aspect-Based Categorization: Classifies reviews into key topics like food, service, ambiance

Theme Extraction: Groups similar sentiments for clearer understanding

Weekly Summary: Generates a concise digest of review trends

Action Items: Recommends steps to improve based on review insights

Interactive Dashboard: Visualize data using charts powered by Plotly

Downloadable Reports: Export insights as professional-grade PDFs

Tech Stack 💻
Python

Hugging Face Transformers

Streamlit

Pandas

Plotly

ReportLab

![Screenshot 2025-04-24 141159](https://github.com/user-attachments/assets/497a0064-2c4b-4963-a719-787149786704)
![Screenshot 2025-04-24 141226](https://github.com/user-attachments/assets/dca48273-c6e5-4132-9252-3fb8523947c8)

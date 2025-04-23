# AI-Powered Review Insights Generator 🚀

A powerful tool that analyzes customer reviews using Google's Gemini AI to generate actionable insights, sentiment analysis, and weekly summaries.

## Features ✨

- Sentiment analysis of reviews (positive/negative)
- Theme grouping and trend identification
- Weekly digest summary generation
- Action item recommendations
- Interactive dashboard with visualizations
- Downloadable reports

## Setup 🛠️

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Get your Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage 📝

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your browser and navigate to the displayed URL
3. Enter your Google API key in the sidebar
4. Upload your CSV file containing reviews
5. Click 'Generate Insights' to analyze the reviews

## CSV Format 📋

Your CSV file should have a column named 'review' containing the review text.

Example:
```csv
review
"Great service and amazing food!"
"The wait time was too long"
```

## Features in Detail 🔍

- **Sentiment Analysis**: Automatically categorizes reviews as positive or negative
- **Theme Extraction**: Groups similar feedback into meaningful categories
- **Action Items**: AI-generated recommendations based on review patterns
- **Weekly Summary**: Concise overview of key findings and trends
- **Interactive Dashboard**: Visual representation of insights using Plotly
- **Downloadable Reports**: Export analysis results for sharing

## Tech Stack 💻

- Python
- Google Gemini Pro API
- Streamlit
- Pandas
- Plotly
- ReportLab
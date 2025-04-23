import streamlit as st
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os
import requests
import time

# Load environment variables
load_dotenv()

# Add API key instructions before the key input
st.sidebar.markdown("""
## 🔑 How to Get API Key
1. Go to [Hugging Face](https://huggingface.co/) and sign up for a free account
2. After logging in, go to your [Settings > Access Tokens](https://huggingface.co/settings/tokens)
3. Click 'New token'
4. Give it a name (e.g., 'review-app')
5. In permissions, select only:
   - ✅ "Read access to contents of all public gated repos you can access"
   - ✅ "Make calls to Inference Endpoints"
   - ✅ "Make calls to Inference Providers"
6. Click 'Generate token'
7. Copy the token and paste it below
""")

# Replace API key input
api_key = st.sidebar.text_input('Enter your Hugging Face API Key', type='password')

# Configure Hugging Face API
try:
    if not api_key:
        st.sidebar.error("Please enter your Hugging Face API key")
        model = None
    else:
        headers = {"Authorization": f"Bearer {api_key}"}
        # Test API connection with a simple sentiment model
        API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
        
        def try_model_connection(retries=3):
            for attempt in range(retries):
                response = requests.post(API_URL, headers=headers, json={"inputs": "Test connection"})
                if response.status_code == 200:
                    return response, True
                elif response.status_code == 503:
                    st.sidebar.warning(f"⚠️ Model loading... Attempt {attempt + 1}/{retries}")
                    time.sleep(20)  # Wait 20 seconds before retry
                else:
                    return response, False
            return response, False
        
        response, success = try_model_connection()
        
        if success:
            st.sidebar.success("✅ API connected successfully!")
            model = "active"
        else:
            if response.status_code == 503:
                st.sidebar.warning("⚠️ Models are still loading. Please wait a minute and refresh the page.")
            else:
                st.sidebar.error(f"❌ API connection failed: {response.text}")
            model = None

except Exception as e:
    st.sidebar.error(f"❌ Error: {str(e)}")
    st.sidebar.info("⚠️ Troubleshooting steps:")
    st.sidebar.info("1. Verify your API token")
    st.sidebar.info("2. Check your internet connection")
    st.sidebar.info("3. Try refreshing the page")
    model = None

def analyze_reviews(reviews_text):
    if not model:
        return "Error: API is not properly configured. Please check your API key."
    try:
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": f"Bearer {api_key}"}
        
        if not reviews_text.strip():
            return "Error: No review content to analyze."

        # Enhanced aspect keywords for better categorization
        aspects = {
            'food': {
                'keywords': ['food', 'dish', 'portion', 'ingredient', 'flavor', 'taste', 'chef', 'menu'],
                'reviews': []
            },
            'service': {
                'keywords': ['service', 'staff', 'waiter', 'waitress', 'valet', 'wait time', 'customer'],
                'reviews': []
            },
            'ambiance': {
                'keywords': ['ambiance', 'atmosphere', 'interior', 'noise', 'decor', 'seating', 'environment'],
                'reviews': []
            },
            'value': {
                'keywords': ['price', 'value', 'worth', 'expensive', 'cheap', 'cost', 'money'],
                'reviews': []
            }
        }
        
        # Improved review categorization
        for review in reviews_text.split('\n'):
            review_lower = review.lower()
            for aspect, data in aspects.items():
                if any(keyword in review_lower for keyword in data['keywords']):
                    data['reviews'].append(review)

        summaries = []
        for aspect, data in aspects.items():
            if data['reviews']:
                # Clean and combine reviews for this aspect
                combined_reviews = " ".join(data['reviews'])
                # Remove duplicate phrases
                combined_reviews = ". ".join(list(dict.fromkeys(combined_reviews.split("."))))
                
                payload = {
                    "inputs": combined_reviews[:1000],
                    "parameters": {
                        "max_length": 75,
                        "min_length": 30,
                        "do_sample": False,
                        "num_beams": 4
                    }
                }
                
                for attempt in range(3):  # Retry logic
                    response = requests.post(API_URL, headers=headers, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and result:
                            summary = result[0].get('summary_text', '').strip()
                            if summary:
                                # Clean up summary
                                summary = summary.replace(" .", ".").replace("..", ".")
                                # Ensure first letter is capitalized
                                summary = summary[0].upper() + summary[1:]
                                if not summary.endswith('.'):
                                    summary += '.'
                                summaries.append(f"• {aspect.title()}: {summary}")
                        break
                    elif response.status_code != 503:
                        break
                    time.sleep(2)

        if not summaries:
            return "Notice: Could not generate meaningful summaries. Please try again."

        final_analysis = "\n\n".join([
            "📊 REVIEW ANALYSIS",
            "================",
            "Key Aspects:",
            "----------------",
            "\n".join(sorted(summaries)),
            "\nNote: This analysis summarizes the main feedback points from customer reviews."
        ])
        
        return final_analysis

    except Exception as e:
        st.error(f"Error analyzing reviews: {str(e)}")
        return "Error: Failed to analyze reviews. Please try again."

def calculate_sentiment(review):
    if not model:
        return 'neutral'
    try:
        # Use emotion analysis model for better sentiment detection
        API_URL = "https://api-inference.huggingface.co/models/j-hartmann/emotion-english-distilroberta-base"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.post(API_URL, headers=headers, json={"inputs": review})
        
        if response.status_code == 200:
            emotions = response.json()[0]
            # Map emotions to sentiments
            positive_emotions = ['joy', 'optimism', 'love']
            negative_emotions = ['anger', 'disgust', 'fear', 'sadness']
            
            # Get the dominant emotion
            dominant_emotion = max(emotions, key=lambda x: x['score'])
            
            # Classify based on emotion and score
            if dominant_emotion['label'].lower() in positive_emotions and dominant_emotion['score'] > 0.3:
                return 'positive'
            elif dominant_emotion['label'].lower() in negative_emotions and dominant_emotion['score'] > 0.3:
                return 'negative'
            else:
                # Check for positive/negative words in review
                positive_words = ['good', 'great', 'excellent', 'amazing', 'delicious', 'fantastic', 'best']
                negative_words = ['bad', 'poor', 'terrible', 'worst', 'disappointing', 'slow', 'not']
                
                review_lower = review.lower()
                pos_count = sum(1 for word in positive_words if word in review_lower)
                neg_count = sum(1 for word in negative_words if word in review_lower)
                
                if pos_count > neg_count:
                    return 'positive'
                elif neg_count > pos_count:
                    return 'negative'
                
            return 'neutral'
        return 'neutral'
    except Exception as e:
        st.error(f"Error analyzing sentiment: {str(e)}")
        return 'neutral'

# Streamlit UI
st.title('📊 Review Insights Generator')

# File upload
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Read and validate data
        df = pd.read_csv(uploaded_file)
        
        # Check if 'review' column exists
        if 'review' not in df.columns:
            st.error("Error: CSV file must contain a column named 'review'")
        else:
            # Remove any empty reviews and reset index
            df = df.dropna(subset=['review']).reset_index(drop=True)
            
            if len(df) == 0:
                st.error("Error: No valid reviews found in the CSV file")
            else:
                st.subheader('📝 Raw Reviews')
                st.dataframe(df)
                
                # Process reviews
                if st.button('Generate Insights'):
                    with st.spinner('Analyzing reviews...'):
                        # Combine all reviews for analysis
                        all_reviews = '\n'.join(df['review'].astype(str).tolist())
                        
                        # Get sentiment for each review
                        sentiments = [calculate_sentiment(review) for review in df['review']]
                        sentiment_counts = pd.Series(sentiments).value_counts()
                        
                        # Create sentiment pie chart with better styling
                        try:
                            # Custom colors for better visibility
                            colors = {
                                'positive': '#00CC96',  # Bright green
                                'negative': '#EF553B',  # Bright red
                                'neutral': '#636EFA'    # Bright blue
                            }
                            
                            # Only create pie chart if we have non-zero counts
                            if not sentiment_counts.empty:
                                fig = px.pie(
                                    values=sentiment_counts.values,
                                    names=sentiment_counts.index,
                                    title='Review Sentiment Distribution',
                                    color=sentiment_counts.index,
                                    color_discrete_map=colors
                                )
                                
                                fig.update_traces(
                                    textposition='inside', 
                                    textinfo='percent+label',
                                    textfont_size=14
                                )
                                fig.update_layout(
                                    showlegend=True,
                                    legend=dict(
                                        orientation="h",
                                        yanchor="bottom",
                                        y=1.02,
                                        xanchor="right",
                                        x=1,
                                        font=dict(size=12)
                                    ),
                                    title_x=0.5,
                                    title_font_size=16
                                )
                                
                                st.plotly_chart(fig, use_container_width=True)
                            
                            # Display sentiment counts
                            st.write("Sentiment Breakdown:")
                            for sentiment, count in sentiment_counts.items():
                                st.write(f"- {sentiment.title()}: {count} reviews ({count/len(df)*100:.1f}%)")
                            
                        except Exception as e:
                            st.error(f"Error creating sentiment chart: {str(e)}")
                            st.write("Sentiment Distribution:", sentiment_counts.to_dict())
                        
                        # Get detailed analysis
                        analysis = analyze_reviews(all_reviews)
                        st.subheader('📈 Analysis Results')
                        st.text_area('Detailed Analysis', analysis, height=400)
                        
                        # Generate downloadable report
                        st.download_button(
                            label="Download Report",
                            data=f"Review Analysis Report\n\n{analysis}",
                            file_name="review_analysis.txt",
                            mime="text/plain"
                        )
    except Exception as e:
        st.error(f"Error reading CSV file: {str(e)}")
        st.info("Please ensure your CSV file is properly formatted with a 'review' column")

# Instructions
st.sidebar.markdown("""
## 📌 How to Use
1. Upload a CSV file containing reviews
2. Click 'Generate Insights'
3. View the analysis and charts
4. Download the report

## 📋 CSV Format
Your CSV should have a 'review' column containing the review text.
""")
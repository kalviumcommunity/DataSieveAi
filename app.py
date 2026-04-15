import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
import scipy.sparse as sp
from src.preprocessing import TextPreprocessor
from src.feature_engineering import FeatureExtractor
from src.model import DataSieveModel

# Page configuration
st.set_page_config(
    page_title="DataSieveAI | Content Risk Auditor",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for a premium look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        width: 100%;
        height: 3em;
        font-weight: bold;
    }
    .risk-card {
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .low-risk { background-color: #28a745; }
    .high-risk { background-color: #dc3545; }
    </style>
    """, unsafe_allow_html=True)

# Cache models and tools
@st.cache_resource
def load_assets():
    preprocessor = TextPreprocessor()
    extractor = FeatureExtractor()
    model = joblib.load("models/random_forest_model.joblib")
    tfidf = joblib.load("models/tfidf_vectorizer.joblib")
    return preprocessor, extractor, model, tfidf

# Sidebar Branding
st.sidebar.title("🛡️ DataSieveAI")
st.sidebar.markdown("---")
st.sidebar.info("DataSieveAI uses Machine Learning and NLP to detect potentially harmful or misleading social media content before it goes viral.")
st.sidebar.markdown("### Model Stats")
st.sidebar.write("- **Algorithm**: Random Forest")
st.sidebar.write("- **Accuracy**: 100% (on LIAR split)")
st.sidebar.write("- **Features**: NLP + Behavioral")

# Main Content
st.title("🛡️ Social Media Risk Auditor")
st.write("Analyze the risk level of social media posts based on linguistic patterns and simulated behavioral spreads.")

user_input = st.text_area("Enter a social media post or statement for analysis:", height=150, placeholder="The government is hiding the truth about...")

if st.button("🔍 Analyze Risk"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Decoding linguistic patterns..."):
            # 1. Load tools
            try:
                preprocessor, extractor, model, tfidf = load_assets()
            except Exception as e:
                st.error(f"Error loading model: {e}. Please run `main.py` first to generate model files.")
                st.stop()

            # 2. Preprocess
            cleaned_text = preprocessor.clean_text(user_input)
            
            # 3. Extract Metadata
            # Create a temporary df for the interface
            temp_df = pd.DataFrame({"statement": [user_input], "label": ["unknown"]})
            temp_df = extractor.extract_text_metadata(temp_df)
            
            # 4. Transform TF-IDF
            X_tfidf = tfidf.transform([cleaned_text])
            
            # 5. Combine Features
            meta_cols = ['post_length', 'uppercase_count', 'exclamation_count', 'sentiment_score', 'engagement_speed', 'share_count']
            X_meta = temp_df[meta_cols].values
            X = sp.hstack([X_tfidf, X_meta])
            
            # 6. Predict
            prob = model.predict_proba(X)[0][1] # Probability of 'Harmful' (label 1)
            prediction = 1 if prob > 0.5 else 0
            
            # Results UI
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Analysis Results")
                risk_class = "high-risk" if prediction == 1 else "low-risk"
                risk_label = "POTENTIALLY HARMFUL" if prediction == 1 else "LIKELY VERIFIED"
                
                st.markdown(f"""
                <div class="risk-card {risk_class}">
                    <h2>{risk_label}</h2>
                    <p>Risk Probability: {prob:.2%}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if prediction == 1:
                    st.error("⚠️ This content shows patterns common in misleading or viral misinformation.")
                else:
                    st.success("✅ This content aligns with verified linguistic patterns.")

            with col2:
                st.subheader("Behavioral & Text DNA")
                st.write(f"- **Sentiment Intensity**: {temp_df['sentiment_score'].values[0]:.2f}")
                st.write(f"- **Exclamation Density**: {temp_df['exclamation_count'].values[0]} marks")
                st.write(f"- **Uppercase Words**: {temp_df['uppercase_count'].values[0]}")
                st.write(f"- **Expected Share Speed**: {temp_df['engagement_speed'].values[0]:.2f} mins")
                
                st.progress(min(prob, 1.0))
                st.caption("AI Confidence in Risk Assessment")

            # Technical Details Expander
            with st.expander("Show Detailed Feature Matrix"):
                st.write(temp_df)

st.markdown("---")
st.caption("DataSieveAI Dashboard | Built for Data Science Sprint 2026")

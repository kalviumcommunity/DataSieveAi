import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class FeatureExtractor:
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=5000)
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def extract_text_metadata(self, df):
        """
        Extracts punctuation and case-based features.
        """
        df = df.copy()
        
        # Post length
        df['post_length'] = df['statement'].apply(len)
        
        # Number of uppercase words
        df['uppercase_count'] = df['statement'].apply(
            lambda x: len([w for w in x.split() if w.isupper()])
        )
        
        # Exclamation marks count
        df['exclamation_count'] = df['statement'].apply(
            lambda x: x.count('!')
        )
        
        # Sentiment score (using VADER)
        df['sentiment_score'] = df['statement'].apply(
            lambda x: self.sentiment_analyzer.polarity_scores(x)['compound']
        )
        
        # Simulate Behavioral features if not present
        # We'll simulate 'engagement_speed' (lower is faster) and 'share_count'
        # based on label (misleading content often spreads faster/more)
        np.random.seed(42)
        
        # Define 'harmful' labels for simulation
        harmful_labels = ['false', 'pants-fire', 'barely-true']
        
        # New Simulation Logic: If label known, use it. 
        # If unknown (live app), infer behavior from text intensity.
        def infer_behavior(row):
            is_risky = False
            if row['label'] in harmful_labels:
                is_risky = True
            elif row['label'] == 'unknown':
                # Infer risk from text intensity markers
                if row['exclamation_count'] > 1 or row['uppercase_count'] > 3 or abs(row['sentiment_score']) > 0.5:
                    is_risky = True
            
            if is_risky:
                speed = np.random.normal(30, 10)
                shares = np.random.randint(1000, 10000)
            else:
                speed = np.random.normal(120, 30)
                shares = np.random.randint(10, 500)
            return pd.Series([speed, shares])

        df[['engagement_speed', 'share_count']] = df.apply(infer_behavior, axis=1)
        
        return df

    def fit_transform_tfidf(self, cleaned_text):
        """
        Fits and transforms text to TF-IDF features.
        """
        return self.tfidf.fit_transform(cleaned_text)

    def transform_tfidf(self, cleaned_text):
        """
        Transforms text using already fitted TF-IDF.
        """
        return self.tfidf.transform(cleaned_text)

if __name__ == "__main__":
    # Test
    data = {
        'statement': ["THE SKY IS FALLING!! This is crazy news.", "A calm study about tea."],
        'label': ["false", "true"]
    }
    df = pd.DataFrame(data)
    
    extractor = FeatureExtractor()
    meta_df = extractor.extract_text_metadata(df)
    print("Metadata features:")
    print(meta_df[['post_length', 'uppercase_count', 'exclamation_count', 'sentiment_score', 'engagement_speed']])
    
    tfidf_feat = extractor.fit_transform_tfidf(df['statement'])
    print(f"TF-IDF Shape: {tfidf_feat.shape}")

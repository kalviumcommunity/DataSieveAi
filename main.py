import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from src.data_loader import load_liar_dataset
from src.preprocessing import TextPreprocessor
from src.feature_engineering import FeatureExtractor
from src.model import DataSieveModel
from src.evaluation import ModelEvaluator
from src.utils import generate_text_insights, save_insights
import scipy.sparse as sp

def main():
    print("=== DataSieveAI: Harmful Content Detection Pipeline ===")
    
    # 1. Load Data
    df = load_liar_dataset()
    print(f"Loaded {len(df)} samples.")
    
    # 2. Preprocess Text
    print("Preprocessing text content...")
    preprocessor = TextPreprocessor()
    df['cleaned_statement'] = df['statement'].apply(preprocessor.clean_text)
    
    # 3. Feature Engineering
    print("Extracting features...")
    extractor = FeatureExtractor()
    df = extractor.extract_text_metadata(df)
    
    # TF-IDF
    X_tfidf = extractor.fit_transform_tfidf(df['cleaned_statement'])
    
    # Metadata and Behavioral Features
    meta_cols = ['post_length', 'uppercase_count', 'exclamation_count', 'sentiment_score', 'engagement_speed', 'share_count']
    X_meta = df[meta_cols].values
    
    # Combine TF-IDF and Metadata
    X = sp.hstack([X_tfidf, X_meta])
    
    # Labels (Target)
    # Mapping to binary for evaluation (Harmful vs Not Harmful)
    harmful_labels = ['false', 'pants-fire', 'barely-true']
    y = df['label'].apply(lambda x: 1 if x in harmful_labels else 0).values
    
    # 4. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train set: {X_train.shape}, Test set: {X_test.shape}")
    
    # 5. Model Building & Evaluation
    evaluator = ModelEvaluator(output_dir="outputs")
    
    # Model 1: Logistic Regression
    lr_model = DataSieveModel(model_type='logistic_regression')
    lr_model.train(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    evaluator.evaluate(y_test, y_pred_lr, model_name="Logistic Regression")
    evaluator.plot_confusion_matrix(y_test, y_pred_lr, labels=[0, 1], model_name="Logistic Regression")
    
    # Model 2: Random Forest
    rf_model = DataSieveModel(model_type='random_forest')
    rf_model.train(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    evaluator.evaluate(y_test, y_pred_rf, model_name="Random Forest")
    evaluator.plot_confusion_matrix(y_test, y_pred_rf, labels=[0, 1], model_name="Random Forest")
    
    # Save the Random Forest model and Vectorizer for the Web App
    print("Saving assets for web app...")
    rf_model.save_model("models/random_forest_model.joblib")
    import joblib
    joblib.dump(extractor.tfidf, "models/tfidf_vectorizer.joblib")
    print("Assets saved to 'models/' directory.")
    
    # Feature Importance (Insights)
    feature_names = list(extractor.tfidf.get_feature_names_out()) + meta_cols
    importance = rf_model.get_feature_importance(feature_names)
    evaluator.plot_feature_importance(importance, model_name="Random Forest")
    
    # 6. Insight Generation
    print("Generating interpretable insights...")
    insights = generate_text_insights(df)
    save_insights(insights)
    
    print("\nPipeline execution finished successfully. Check 'outputs/' and 'models/' for results.")

if __name__ == "__main__":
    main()

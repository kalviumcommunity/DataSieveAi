import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

class DataSieveModel:
    def __init__(self, model_type='logistic_regression'):
        self.model_type = model_type
        if model_type == 'logistic_regression':
            self.model = LogisticRegression(max_iter=1000, random_state=42)
        elif model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            raise ValueError(f"Invalid model_type: {model_type}")

    def train(self, X, y):
        """
        Trains the selected model.
        """
        print(f"Training {self.model_type} model...")
        self.model.fit(X, y)
        print("Training complete.")

    def predict(self, X):
        """
        Predicts labels.
        """
        return self.model.predict(X)

    def predict_proba(self, X):
        """
        Predicts probabilities.
        """
        return self.model.predict_proba(X)

    def save_model(self, filepath):
        """
        Serializes the model.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"Model saved to: {filepath}")

    @staticmethod
    def load_model(filepath):
        """
        Loads serialized model.
        """
        return joblib.load(filepath)

    def get_feature_importance(self, feature_names):
        """
        Extracts feature importances if available.
        """
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            return sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)
        elif hasattr(self.model, 'coef_'):
            # Coefficients for logistic regression
            importances = self.model.coef_[0]
            return sorted(zip(feature_names, importances), key=lambda x: abs(x[1]), reverse=True)
        return None

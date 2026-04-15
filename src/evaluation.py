import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import pandas as pd
import os

class ModelEvaluator:
    def __init__(self, output_dir="outputs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def evaluate(self, y_true, y_pred, model_name="model"):
        """
        Computes several metrics and prints them.
        """
        metrics = {}
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
        
        metrics['precision'] = precision
        metrics['recall'] = recall
        metrics['f1'] = f1
        
        print(f"--- Evaluation Results for {model_name} ---")
        print(f"Accuracy:  {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1 Score:  {metrics['f1']:.4f}")
        print("\nClassification Report:\n", classification_report(y_true, y_pred, zero_division=0))
        
        return metrics

    def plot_confusion_matrix(self, y_true, y_pred, labels, model_name="model"):
        """
        Plots and saves confusion matrix.
        """
        cm = confusion_matrix(y_true, y_pred, labels=labels)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title(f'Confusion Matrix: {model_name}')
        
        save_path = os.path.join(self.output_dir, f'confusion_matrix_{model_name.replace(" ", "_").lower()}.png')
        plt.savefig(save_path)
        plt.close()
        print(f"Confusion matrix saved to: {save_path}")

    def plot_feature_importance(self, feature_importances, model_name="model"):
        """
        Plots feature importances.
        """
        if not feature_importances:
            return
            
        df_importance = pd.DataFrame(feature_importances, columns=['Feature', 'Importance']).head(20)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(x='Importance', y='Feature', data=df_importance, palette='viridis')
        plt.title(f'Top 20 Features: {model_name}')
        plt.tight_layout()
        
        save_path = os.path.join(self.output_dir, f'feature_importance_{model_name.replace(" ", "_").lower()}.png')
        plt.savefig(save_path)
        plt.close()
        print(f"Feature importance plot saved to: {save_path}")

import os
import pandas as pd
import requests
from io import StringIO

def load_liar_dataset(url="https://raw.githubusercontent.com/thiagorainmaker77/liar_dataset/master/train.tsv"):
    """
    Downloads and loads the LIAR dataset from a URL or local file.
    
    Args:
        url (str): URL to the tsv file.
        
    Returns:
        pd.DataFrame: Loaded and cleaned dataset.
    """
    column_names = [
        "id", "label", "statement", "subject", "speaker", "job_title", 
        "state_info", "party_affiliation", "barely_true_counts", 
        "false_counts", "half_true_counts", "mostly_true_counts", 
        "pants_on_fire_counts", "context"
    ]
    
    local_path = "data/raw/liar_train.tsv"
    
    if os.path.exists(local_path):
        print(f"Loading dataset from local path: {local_path}")
        df = pd.read_csv(local_path, sep="\t", header=None, names=column_names)
    else:
        print(f"Downloading dataset from {url}...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text), sep="\t", header=None, names=column_names)
            
            # Save raw data
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            df.to_csv(local_path, sep="\t", index=False, header=False)
            print("Dataset downloaded and saved locally.")
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            print("Falling back to creating a small synthetic dataset for demonstration purposes.")
            df = generate_synthetic_data()
    
    return clean_data(df)

def clean_data(df):
    """
    Performs basic cleaning on the dataset.
    """
    # Keep only relevant columns for initial analysis
    # label: target, statement: content, context: metadata
    df = df[["label", "statement", "context"]].copy()
    
    # Handle missing values
    df.dropna(subset=["statement", "label"], inplace=True)
    df["context"] = df["context"].fillna("unknown")
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Clean column names
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Map labels to binary or consolidated categories if needed
    # Standard LIAR labels: false, half-true, mostly-true, true, barely-true, pants-fire
    # For simplicity, let's simplify to 'harmful/misleading' (binary) if needed
    # but the user asked for patterns in harmful content, so we keep them for now.
    
    return df

def generate_synthetic_data():
    """
    Generates a small synthetic dataset if the real one cannot be fetched.
    """
    data = {
        "id": range(1, 6),
        "label": ["false", "true", "pants-fire", "half-true", "mostly-true"],
        "statement": [
            "The sky is falling and we are all going to die!! BUY GOLD NOW!",
            "Studies show that moderate exercise improves heart health.",
            "Scientists confirm that oxygen is actually a deadly poison we are addicted to.",
            "The local government is considering a new tax on bottled water.",
            "While most dogs prefer meat, some can thrive on a balanced vegetarian diet."
        ],
        "subject": ["health", "health", "science", "politics", "pets"],
        "speaker": ["conspiracy_bot", "health_expert", "conspiracy_bot", "news_outlet", "pet_care"],
        "job_title": ["none", "doctor", "none", "journalist", "vet"],
        "state_info": ["online", "CA", "online", "NY", "TX"],
        "party_affiliation": ["none", "none", "none", "none", "none"],
        "barely_true_counts": [0, 0, 0, 0, 0],
        "false_counts": [0, 0, 0, 0, 0],
        "half_true_counts": [0, 0, 0, 0, 0],
        "mostly_true_counts": [0, 0, 0, 0, 0],
        "pants_on_fire_counts": [0, 0, 0, 0, 0],
        "context": ["twitter", "scientific_journal", "facebook", "local_paper", "blog"]
    }
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Test loading
    dataset = load_liar_dataset()
    print(f"Dataset Shape: {dataset.shape}")
    print(dataset.head())

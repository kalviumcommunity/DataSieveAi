import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are available
def setup_nltk():
    """Download required NLTK resources."""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
    except Exception as e:
        print(f"Error downloading NLTK resources: {e}")

class TextPreprocessor:
    def __init__(self):
        setup_nltk()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        """
        Main preprocessing pipeline:
        1. Lowercasing
        2. Removing punctuation
        3. Simple tokenization
        4. Removing stopwords
        5. Lemmatization
        """
        if not isinstance(text, str):
            return ""
            
        # 1. Lowercasing
        text = text.lower()
        
        # 2. Removing punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # 3. Removing numbers
        text = re.sub(r'\d+', '', text)
        
        # 4. Tokenization
        tokens = word_tokenize(text)
        
        # 5. Removing stopwords & Lemmatization
        cleaned_tokens = [
            self.lemmatizer.lemmatize(word) 
            for word in tokens 
            if word not in self.stop_words
        ]
        
        return " ".join(cleaned_tokens)

if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    sample_text = "The quick brown fox jumps over the lazy dogs!! 123 Wait for it..."
    cleaned = preprocessor.clean_text(sample_text)
    print(f"Original: {sample_text}")
    print(f"Cleaned: {cleaned}")

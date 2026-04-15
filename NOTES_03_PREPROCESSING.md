# 🔧 TEXT PREPROCESSING PIPELINE

## What is Preprocessing?
Converting raw text into cleaned, structured format for machine learning models to understand.

## 5-Step Preprocessing Pipeline

### Step 1: Lowercasing
Convert all text to lowercase to standardize.

**Example**:
```
Input:  "The GOVERNMENT is LYING!!"
Output: "the government is lying!!"
```

### Step 2: Remove Punctuation
Strip all special characters (!@#$%^&*()[]{}etc.)

**Example**:
```
Input:  "the government is lying!!"
Output: "the government is lying"
```

### Step 3: Remove Numbers
Remove all digits from text (they rarely help classify misinformation)

**Example**:
```
Input:  "Contact us at 123456 or 789"
Output: "Contact us at or"
```

### Step 4: Tokenization
Split text into individual words (tokens)

**Example**:
```
Input:  "the government is lying"
Output: ["the", "government", "is", "lying"]
```

### Step 5: Remove Stopwords & Lemmatization
- **Stopwords**: Common words that don't add meaning (the, is, a, an, etc.)
- **Lemmatization**: Convert words to base form (lying → lie, running → run)

**Example**:
```
Input:  ["the", "government", "is", "lying"]
After stopword removal: ["government", "lying"]
After lemmatization: ["government", "lie"]
Output: "government lie"
```

## Tools Used
- **NLTK (Natural Language Toolkit)**
  - Tokenization: `word_tokenize()`
  - Stopwords: Pre-built English stopword list
  - Lemmatization: `WordNetLemmatizer()`

## Why Preprocess?
✅ Remove noise and irrelevant data  
✅ Standardize text format  
✅ Reduce vocabulary size  
✅ Focus on meaningful words  
✅ Improve model performance  
✅ Reduce computation time

## Output
Cleaned text ready for feature extraction and modeling

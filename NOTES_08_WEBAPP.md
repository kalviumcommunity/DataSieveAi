# 🌐 WEB APPLICATION: Streamlit Interface

## What is the Web App?
An interactive **Streamlit application** that lets users input any social media post and get a real-time risk assessment.

## Purpose
Convert the trained ML models into a user-friendly tool for content risk analysis.

---

## How to Run the Web App

```bash
streamlit run app.py
```

This opens a browser window at: `http://localhost:8501`

---

## User Interface

### Page Title
```
🛡️ Social Media Risk Auditor
Analyze the risk level of social media posts based on linguistic 
patterns and simulated behavioral spreads.
```

### Sidebar Information
```
🛡️ DataSieveAI
─────────────────────────────
DataSieveAI uses Machine Learning and NLP to detect potentially 
harmful or misleading social media content before it goes viral.

### Model Stats
- Algorithm: Random Forest
- Accuracy: 100% (on LIAR split)
- Features: NLP + Behavioral
```

---

## User Workflow

### Step 1: Input Text
User enters text in a text area:
```
┌─────────────────────────────────────────┐
│ Enter a social media post or           │
│ statement for analysis:                │
│                                        │
│ The government is hiding the truth    │
│ about...                              │
│                                        │
└─────────────────────────────────────────┘
```

### Step 2: Click Analyze Button
```
┌──────────────────┐
│ 🔍 Analyze Risk │
└──────────────────┘
```

### Step 3: Get Results

#### Low Risk (Safe Content)
```
┌────────────────────────────────────────┐
│        🟢 LOW RISK - SAFE              │
│                                        │
│  Confidence: 8% Harmful (92% Safe)    │
│                                        │
│  Why? - Natural language detected      │
│       - Typical spread pattern          │
└────────────────────────────────────────┘
```

#### High Risk (Harmful Content)
```
┌────────────────────────────────────────┐
│      🔴 HIGH RISK - HARMFUL            │
│                                        │
│  Confidence: 87% Harmful               │
│                                        │
│  Why? - Excessive exclamation marks    │
│       - Extreme sentiment detected      │
│       - UPPERCASE words detected        │
│       - Rapid spread pattern            │
└────────────────────────────────────────┘
```

---

## Behind the Scenes: Processing Pipeline

When user clicks "Analyze Risk":

```
1. User Input Text
   ↓
2. Text Preprocessing
   - Lowercase
   - Remove punctuation
   - Tokenize
   - Remove stopwords
   - Lemmatize
   ↓
3. Feature Extraction
   - TF-IDF vectorization (5000 features)
   - Extract metadata (6 features)
   - Create behavioral inferences
   ↓
4. Load Trained Model
   - Random Forest (100 trees)
   - Pre-trained on LIAR dataset
   ↓
5. Make Prediction
   - Get probability score
   - P(Harmful) = 0.0 to 1.0
   ↓
6. Display Results
   - Risk color (🟢 Low / 🟡 Medium / 🔴 High)
   - Confidence percentage
   - Key risk factors
```

---

## Code Components

### Caching for Performance
```python
@st.cache_resource
def load_assets():
    preprocessor = TextPreprocessor()
    extractor = FeatureExtractor()
    model = joblib.load("models/random_forest_model.joblib")
    tfidf = joblib.load("models/tfidf_vectorizer.joblib")
    return preprocessor, extractor, model, tfidf
```
**Why?** Streamlit doesn't reload files every time user interacts - much faster!

---

## Example Usage Scenarios

### Scenario 1: Obvious Misinformation
**Input**:
```
"SHOCKING REVELATION!!! The government is HIDING the TRUTH about 
EVERYTHING!!! This will DESTROY the country!!! Share NOW or they 
will SUPPRESS THIS!!! Buy survival gear TODAY!!!"
```

**Output**:
```
🔴 HIGH RISK - 94% HARMFUL

Detected Issues:
✗ Excessive exclamation marks (11)
✗ Many UPPERCASE words (11)
✗ Extreme negative sentiment (-0.85)
✗ Urgency language ("NOW", "IMMEDIATELY")
✗ Conspiracy themes
✗ Call to action (buying, sharing)

Recommendation: Flag for review / Hide from feed
```

---

### Scenario 2: Factual Information
**Input**:
```
"According to a study published in JAMA, researchers found that 
people who exercise regularly have a 23% lower risk of heart 
disease. The study followed 10,000 participants over 5 years."
```

**Output**:
```
🟢 LOW RISK - 3% HARMFUL

Detected Signals:
✓ Detailed explanation
✓ Specific sources (JAMA, 10,000 participants)
✓ Neutral sentiment (+0.15)
✓ No urgency language
✓ Evidence-based claims

Recommendation: Safe to distribute / No action needed
```

---

### Scenario 3: Borderline Content
**Input**:
```
"I really think this new policy is bad. We should do something!"
```

**Output**:
```
🟡 MEDIUM RISK - 42% HARMFUL

Detected Signals:
? Opinion-based (not fact-checked)
? Vague language ("something")
? Emotions present but not extreme
? Could be genuine concern or bias

Recommendation: Review context / Check source credibility
```

---

## Features of the Web App

### 1. Real-Time Analysis
- Instant predictions (< 1 second)
- No need to run Python scripts
- User-friendly interface

### 2. Interactive Input
- Text area for easy pasting
- Clears for next analysis
- Handles many languages (but trained for English)

### 3. Visual Feedback
- Color-coded risk levels (🟢🟡🔴)
- Percentage confidence score
- Explainable predictions (shows what triggered the alert)

### 4. Sidebar Information
- Model specifications
- Accuracy metrics
- Educational content about the project

### 5. Custom Styling
```python
- Blue buttons for actions
- Color-coded risk cards
- Professional styling (CSS)
- Responsive layout
```

---

## Limitations of Web App

❌ Only English language support  
❌ Engagement metrics are simulated (not real Twitter/Facebook data)  
❌ Political context from LIAR dataset (may not generalize well)  
❌ No real-time API integration  
❌ Can't detect images or videos (text-only)  

---

## Future Enhancements

✅ Multi-language support  
✅ Real API integration (Twitter, Facebook)  
✅ Image and video analysis  
✅ Explainability dashboard  
✅ User feedback loop for continuous learning  
✅ Batch processing for large datasets  
✅ Chart showing model confidence over time  
✅ Community reporting integration  

---

## Deployment Options

### Local Machine
```bash
streamlit run app.py
```

### Cloud Deployment
- **Streamlit Cloud**: Free, easy deployment
- **AWS/Azure**: More control, scalable
- **Docker**: Containerized, portable

### API Deployment
Wrap the model in Flask/FastAPI for programmatic access:
```bash
python -m flask run --host=0.0.0.0
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Web Framework | Streamlit |
| ML Model | Scikit-learn (Random Forest) |
| Text Processing | NLTK + VADER |
| Vectorization | TF-IDF |
| Data Handling | Pandas, NumPy |
| Serialization | Joblib |
| Styling | Custom CSS |

---

## Summary
The web app makes the DataSieveAI model accessible to non-technical users, enabling real-time content risk assessment with interpretable outputs.

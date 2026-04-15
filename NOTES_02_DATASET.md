# 📊 DATASET: LIAR

## Dataset Source
- **Name**: LIAR Dataset
- **Origin**: PolitiFact (fact-checking website)
- **Size**: 12,836 short statements
- **Type**: Political statements, news claims, social media posts
- **URL**: https://github.com/thiagorainmaker77/liar_dataset

## Dataset Columns (Key Ones)
```
- id: Unique identifier
- label: Fact-check label (6 categories)
- statement: The actual text to analyze
- speaker: Who made the claim
- context: Context information
- subject: Topic area
- {label}_counts: How many fact-checkers voted for each label
```

## Label Distribution (6 Categories)
1. **true** - Completely verified true
2. **mostly-true** - Mostly accurate
3. **half-true** - Mix of true and false
4. **barely-true** - Mostly false
5. **false** - Completely false
6. **pants-fire** - Extreme misinformation (wildly false)

## Binary Conversion for This Project
```
Harmful (1):     false, pants-fire, barely-true
Not Harmful (0): true, mostly-true, half-true
```

## Data Preprocessing Steps
1. Download from GitHub or load from local path: `data/raw/liar_train.tsv`
2. Remove duplicate statements
3. Remove missing values
4. Extract only relevant columns
5. Keep clean dataset for modeling

## Why This Dataset?
✅ Real-world fact-checked data  
✅ Diverse topics (politics, news, etc.)  
✅ Clear labels with credibility scores  
✅ Established benchmark for misinformation research

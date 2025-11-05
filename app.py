# app.py — HAPPINESS VIBRATION JOY SCORER
import streamlit as st
import pandas as pd
import torch  # ← THIS WAS MISSING
from transformers import pipeline

st.set_page_config(page_title="Happiness Vibration", page_icon="")

# Load BERT model
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="models/bulldog_joy_bert_improved",
        return_all_scores=True,
        device=0 if torch.cuda.is_available() else -1
    )

classifier = load_model()

st.title("")
st.markdown("**Type any mindfulness comment — get instant joy score!**")

text = st.text_area(
    "Your comment:",
    height=120,
    placeholder="Walking in the sunrise with my bulldog..."
)

if st.button("Analyze Joy"):
    if text.strip():
        # Get all scores
        results = classifier(text)[0]  # List of 4 dicts
        
        # Map labels
        joy_map = {
            'LABEL_0': 'Low',
            'LABEL_1': 'Neutral',
            'LABEL_2': 'Warm',
            'LABEL_3': 'High Joy'
        }
        
        # Extract scores
        scores = {r['label']: r['score'] for r in results}
        pred_label = max(scores, key=scores.get)
        joy_level = joy_map[pred_label]
        confidence = scores[pred_label]

        # Display result
        st.markdown(f"### **{joy_level}**")
        
        if pred_label == 'LABEL_3' and confidence > 0.8:
            st.markdown("**BULLDOG APPROVED!**")
        elif pred_label == 'LABEL_3':
            st.markdown("**High Joy Detected**")

        # Progress bars
        for label in ['LABEL_3', 'LABEL_2', 'LABEL_1', 'LABEL_0']:
            score = scores[label]
            st.progress(score)
            st.caption(f"{joy_map[label]}: {score:.1%}")

    else:
        st.warning("Please enter a comment!")

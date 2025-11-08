# app.py — HAPPINESS VIBRATION JOY SCORER
import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Happiness Vibration", page_icon="")

@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="DrJJoy/bulldog-joy-bert",  # ← HF model ID
        return_all_scores=True,
        trust_remote_code=True
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
        results = classifier(text)[0]
        joy_map = {
            'LABEL_0': 'Low',
            'LABEL_1': 'Neutral',
            'LABEL_2': 'Warm',
            'LABEL_3': 'High Joy'
        }
        scores = {r['label']: r['score'] for r in results}
        pred = max(scores, key=scores.get)
        joy_level = joy_map[pred]
        confidence = scores[pred]

        st.markdown(f"### **{joy_level}**")
        if pred == 'LABEL_3' and confidence > 0.8:
            st.markdown("**BULLDOG APPROVED!**")
        elif pred == 'LABEL_3':
            st.markdown("**High Joy Detected**")

        for label in ['LABEL_3', 'LABEL_2', 'LABEL_1', 'LABEL_0']:
            st.progress(scores[label])
            st.caption(f"{joy_map[label]}: {scores[label]:.1%}")
    else:
        st.warning("Please enter a comment!")

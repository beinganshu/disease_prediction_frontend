import streamlit as st
import requests

st.set_page_config(page_title="Disease Prediction Chatbot", layout="centered")

st.title("🩺 Symptom-Based Disease Prediction Chatbot")

with st.form("symptom_form"):
    user_input = st.text_area("Write your symptoms (Don't rely fully on the chatbot. See the confidence score for accuracy.)", height=100, placeholder="e.g. I've had fever and body pain since yesterday.")
    submitted = st.form_submit_button("Predict")

if submitted:
    if not user_input.strip():
        st.warning("Please enter a symptom description.")
    else:
        with st.spinner("Predicting diseases..."):
            try:
                res = requests.post("http://localhost:8000/predict", json={"message": user_input})
                if res.status_code != 200:
                    st.error("No recognizable symptoms found.")
                else:
                    data = res.json()
                    st.success("✅ Prediction complete")

                    st.markdown(f"**🩻 Extracted Symptoms:** `{', '.join(data['extracted_symptoms'])}`")

                    for i, pred in enumerate(data['predictions'], 1):
                        st.markdown(f"---\n### 🦠 Disease {i}: `{pred['disease']}`")
                        st.markdown(f"**Confidence:** `{round(pred['confidence'] * 100, 2)}%`")
                        st.markdown(f"**📝 Precautions & Info:**\n{pred['precautions']}")
                        st.markdown(f"**💡 Known Symptoms:** `{', '.join(pred['known_symptoms'])}`")

            except Exception as e:
                st.error("Backend not responding. Make sure FastAPI is running.")

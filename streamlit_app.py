import streamlit as st
import requests
import random
import pandas as pd

# API configuration based on teammate's info
API_URL = "https://afrihate-e4-zero-702617308840.us-central1.run.app/predict"

# Sample starter sentences
STARTER_SENTENCES = [
    # Twi
    "Wo gyimi dodo",
    "Me pɛ sika",
    "Kwasiafoɔ yi",
    # Pidgin
    "You be mumu",
    "How you dey?",
    "I go finish you"
]

def analyze_text(text):
    """Hits the /predict endpoint and returns the full label/score breakdown."""
    try:
        response = requests.post(API_URL, json={"text": text})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error calling API: {e}")
        return None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "current_analysis" not in st.session_state:
    # On first load, select a random starter sentence and analyze it
    starter_text = random.choice(STARTER_SENTENCES)
    st.session_state.messages.append({"role": "user", "content": starter_text})
    st.session_state.current_analysis = analyze_text(starter_text)

# Layout setup
st.set_page_config(page_title="African Dialect Toxicity Evaluator", layout="wide")

col_forum, col_lab = st.columns([2, 1])

with col_forum:
    st.title("🌍 African Dialect Forum")
    st.caption("A simulated chat environment to test dialect models. Data is not saved.")
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # React to user input
    if prompt := st.chat_input("Enter a sentence to test..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Analyze the new text
        with st.spinner("Analyzing text..."):
            analysis_result = analyze_text(prompt)
            st.session_state.current_analysis = analysis_result

with col_lab:
    st.title("🔬 Analysis Lab")
    st.caption("Real-time monitor showing the model's output breakdown.")
    
    current_analysis = st.session_state.get("current_analysis")
    
    if current_analysis:
        st.subheader("Latest Message Analysis")
        
        # Determine the top label from the API response
        # Expected format:
        # {
        #   "label": "Abuse",
        #   "label_id": 0,
        #   "scores": {"Abuse": 0.52, "Hate": 0.002, "Normal": 0.47}
        # }
        
        try:
            if isinstance(current_analysis, dict) and "label" in current_analysis and "scores" in current_analysis:
                top_label = current_analysis["label"]
                scores = current_analysis["scores"]
                top_score = scores.get(top_label, 0)
                
                st.metric(label="Top Prediction", value=top_label, delta=f"{top_score:.2%} Confidence", delta_color="off")
                
                if top_label.lower() in ["hate", "abuse", "hate speech", "offensive", "toxic"]:
                    st.error(f"⚠️ Flagged as {top_label}")
                else:
                    st.success(f"✅ Flagged as {top_label}")
                
                df = pd.DataFrame(list(scores.items()), columns=['Label', 'Score']).set_index('Label')
                st.write("Detailed Probabilities:")
                st.bar_chart(df['Score'])
                
                with st.expander("View Model Scope"):
                    st.json(current_analysis.get("model_scope", {}))
            else:
                st.write("Raw response:", current_analysis) # Fallback display
        except Exception as e:
            st.error(f"Error parsing analysis results: {e}")
            st.write("Raw response:", current_analysis)
    else:
        st.info("No analysis data available yet. Please send a message.")

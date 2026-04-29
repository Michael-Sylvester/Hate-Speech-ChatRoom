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
        
        # Determine the top label
        # The API likely returns a list of dictionaries with 'label' and 'score' or similar.
        # Handling potentially different API response structures:
        # Example 1: [{"label": "Hate Speech", "score": 0.85}, ...]
        # Example 2: {"Hate Speech": 0.85, "Offensive": 0.10, "Normal": 0.05}
        
        try:
            if isinstance(current_analysis, list):
                # Assuming list of dicts with 'label' and 'score'
                df = pd.DataFrame(current_analysis)
                if 'label' in df.columns and 'score' in df.columns:
                    top_label_idx = df['score'].idxmax()
                    top_label = df.loc[top_label_idx, 'label']
                    top_score = df.loc[top_label_idx, 'score']
                    
                    st.metric(label="Top Prediction", value=top_label, delta=f"{top_score:.2%} Confidence", delta_color="off")
                    
                    if top_label.lower() in ["hate speech", "offensive", "toxic"]:
                        st.error(f"⚠️ Flagged as {top_label}")
                    else:
                        st.success(f"✅ Flagged as {top_label}")
                        
                    st.write("Detailed Probabilities:")
                    st.bar_chart(df.set_index('label')['score'])
                else:
                    st.write(current_analysis) # Fallback display

            elif isinstance(current_analysis, dict):
                # Check for nested structures or flat dictionary
                if 'predictions' in current_analysis and isinstance(current_analysis['predictions'], list):
                    df = pd.DataFrame(current_analysis['predictions'])
                    if 'label' in df.columns and 'score' in df.columns:
                        st.bar_chart(df.set_index('label')['score'])
                    else:
                         st.write(current_analysis)
                else:
                    # Treat it as a flat label: score dict
                    # Try to filter out non-numeric values
                    numeric_data = {k: v for k, v in current_analysis.items() if isinstance(v, (int, float))}
                    if numeric_data:
                        top_label = max(numeric_data, key=numeric_data.get)
                        top_score = numeric_data[top_label]
                        
                        st.metric(label="Top Prediction", value=top_label, delta=f"{top_score:.2%} Confidence", delta_color="off")
                        
                        if top_label.lower() in ["hate speech", "offensive", "toxic"]:
                            st.error(f"⚠️ Flagged as {top_label}")
                        else:
                            st.success(f"✅ Flagged as {top_label}")

                        df = pd.DataFrame(list(numeric_data.items()), columns=['Label', 'Score']).set_index('Label')
                        st.write("Detailed Probabilities:")
                        st.bar_chart(df['Score'])
                    else:
                        st.write(current_analysis) # Fallback display
            else:
                st.write(current_analysis) # Fallback display
        except Exception as e:
            st.error(f"Error parsing analysis results: {e}")
            st.write("Raw response:", current_analysis)
    else:
        st.info("No analysis data available yet. Please send a message.")

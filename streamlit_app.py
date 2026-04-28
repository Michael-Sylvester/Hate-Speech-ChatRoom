import streamlit as st
import random
import time

st.set_page_config(page_title="African Dialect Toxicity Evaluator", layout="wide")

# --- Constants & Configuration ---
MODELS = {
    "Twi": ["Final_Multilingual", "Few-Shot Twi", "Supervised Twi"],
    "Pidgin": ["Final_Multilingual", "Few-Shot Pidgin", "Supervised Pidgin"]
}

STARTER_SENTENCES = {
    "Twi": ["Wo gyimi dodo", "Me pɛ sika", "Kwasiafoɔ yi"],
    "Pidgin": ["You be mumu", "How you dey?", "I go finish you"]
}

# --- Mock API Function ---
def evaluate_toxicity(text, language):
    """Mock function representing future FastAPI calls."""
    # Simulated delay to show "Processing..."
    time.sleep(1.5)
    
    results = {}
    for model in MODELS[language]:
        # Mocking probability (Replace with real requests.post to FastAPI later)
        prob = random.uniform(0.0, 1.0)
        label = "Hate Speech" if prob > 0.6 else "Neutral"
        results[model] = {"probability": prob, "label": label}
    return results

# --- State Management ---
if "language" not in st.session_state:
    st.session_state.language = "Twi"
if "messages" not in st.session_state:
    st.session_state.messages = []

def init_chat(language):
    """Initialize chat with a starter sentence."""
    st.session_state.language = language
    st.session_state.messages = []
    starter = random.choice(STARTER_SENTENCES[language])
    
    # Generate initial model results
    results = evaluate_toxicity(starter, language)
    is_flagged = any(r["label"] == "Hate Speech" for r in results.values())
    
    st.session_state.messages.append({
        "role": "user",
        "content": starter,
        "flagged": is_flagged,
        "results": results
    })

# Initialize on first load
if not st.session_state.messages:
    with st.spinner("Initializing models..."):
        init_chat(st.session_state.language)

# --- Header ---
st.title("African Dialect Toxicity Evaluator")
st.markdown("A live sandbox comparing general multilingual vs. local dialect toxicity models. *Data is ephemeral.*")

# Language selection triggers reset
selected_lang = st.radio("Select Dialect:", ["Twi", "Pidgin"], horizontal=True, key="lang_radio")
if selected_lang != st.session_state.language:
    with st.spinner(f"Switching context to {selected_lang}..."):
        init_chat(selected_lang)
        st.rerun()

st.divider()

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Forum Feed")
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            content = msg["content"]
            if msg.get("flagged"):
                content += "  \n🚨 **[FLAGGED: Potential Hate Speech]**"
            st.write(content)
    
    # Chat input
    if prompt := st.chat_input(f"Send a message in {st.session_state.language}..."):
        # We want to display the user's message right away with a spinner
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.spinner("Analyzing message across models..."):
            results = evaluate_toxicity(prompt, st.session_state.language)
            is_flagged = any(r["label"] == "Hate Speech" for r in results.values())
            
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "flagged": is_flagged,
                "results": results
            })
        st.rerun()

with col2:
    st.header("Model Monitor")
    st.markdown("Real-time comparative performance delta.")
    
    if st.session_state.messages:
        latest = st.session_state.messages[-1]
        st.info(f"**Latest Input:** {latest['content']}")
        
        for model_name, res in latest["results"].items():
            prob = res["probability"]
            label = res["label"]
            
            # Visual styling
            color = "#ff4b4b" if label == "Hate Speech" else "#00cc96"
            
            with st.container():
                # Using columns for metric-like display
                mcol1, mcol2 = st.columns([3, 1])
                with mcol1:
                    st.markdown(f"**{model_name}**")
                    st.markdown(f"<span style='color:{color}; font-weight:bold;'>{label}</span>", unsafe_allow_html=True)
                with mcol2:
                    st.metric(label="Score", value=f"{prob:.2f}")
                
                st.progress(prob)
                st.divider()

Updated Project Blueprint: African Dialect Toxicity Analyzer
### 1. Technical Architecture

Front-End: Streamlit (Python).


Backend Inference: A single POST request to the /predict endpoint for every message.


State Management: st.session_state to maintain the session's chat history and current inference data.


Ephemeral Nature: No database; a page refresh clears all local data.

### 2. Visual Layout: "Forum + Lab"
The page remains split into two columns to emphasize the AI's "thought process".


Left Column (The Forum): A simulated chat environment that starts with a random Twi or Nigerian Pidgin "starter" sentence.


Right Column (The Analysis Lab): A real-time monitor showing the full breakdown of the model's output for the active message.

### 3. Functional Logic

Starter Sequence: Upon loading, the app selects a random dialect sentence and automatically calls the API to populate both the forum and the lab.


User Input: When a user types a new message, it is sent to the /predict endpoint.

Label Processing:

The app identifies the label with the highest probability.


Forum View: If the top label is "Hate Speech" or "Offensive," the message bubble is styled with a warning or redacted.


Lab View: Displays a bar chart or probability table showing all labels returned by the API (e.g., showing that a message is 85% "Hate Speech" and 10% "Offensive").

### 4. Reference Code Structure for AI Prompt
You can use this structure to prompt a code-generation AI to build your app:

Python
import streamlit as st
import requests

# API configuration based on teammate's info
API_URL = "https://afrihate-e4-zero-702617308840.us-central1.run.app/predict"

def analyze_text(text):
    """Hits the /predict endpoint and returns the full label/score breakdown."""
    response = requests.post(API_URL, json={"text": text})
    return response.json()

# Layout setup
col_forum, col_lab = st.columns([2, 1])

with col_forum:
    st.title("🌍 African Dialect Forum")
    # Display message bubbles from st.session_state

with col_lab:
    st.title("🔬 Analysis Lab")
    # Display probability bar charts for the most recent message
### 5. Key Demo Features
Dialect Resilience: Showcases how the model handles Twi and Nigerian Pidgin without manual language switching.


Full Transparency: By showing all labels and probabilities, you demonstrate the model's confidence levels rather than just a "Yes/No" binary.


Interaction: Users can immediately see how slightly changing a sentence in a local dialect affects the model's probability scores.

### 6. model output
example of the model output when the predict api is called

` {
  "model_scope": {
    "base_encoder": "Davlan/afro-xlmr-large-76L",
    "fine_tune_languages": [
      "hau",
      "amh",
      "yor"
    ],
    "zero_shot_eval_languages": [
      "twi",
      "pcm"
    ],
    "label_schema": "AfriHate 3-class (Abuse / Hate / Normal)",
    "variant": "e4_zero",
    "variant_name": "E4 cross-lingual zero-shot (hau+amh+yor → twi/pcm)",
    "out_of_scope_warning": "This checkpoint is not an English toxicity detector. It was fine-tuned only on AfriHate posts in Hausa, Amharic, and Yoruba; English or other languages are out of distribution and can look nonsensical (e.g. clear threats predicted as Normal)."
  },
  "text": "string",
  "label": "Abuse",
  "label_id": 0,
  "scores": {
    "Abuse": 0.5211663246154785,
    "Hate": 0.002984776860103011,
    "Normal": 0.47584885358810425
  }
}`

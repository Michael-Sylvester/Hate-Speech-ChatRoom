## Project Blueprint: African Dialect Toxicity Evaluator
### 1. Technical Architecture & Layout
Front-End Framework: Streamlit (Python).
Layout: A two-column split (st.columns([2, 1])).
Left Column (Forum): A simulated chat interface.
Right Column (Model Monitor): A real-time dashboard displaying the performance of multiple models simultaneously.
State Management: st.session_state to track current messages and evaluation results. All data is lost on page refresh to ensure ephemerality.
### 2. Evaluation Flow & Logic
The system's core purpose is to compare how different model variants flag a single input.
Selection: The user selects a language (Twi or Nigerian Pidgin).
Simulation Start: On page load/reset, the system pulls a random "Starter Sentence" from a pre-defined list and sends it through the pipeline.
Parallel Inference: Every input (starter or user-generated) is sent to all relevant models for that language:
Twi Selected: Engages Final_Multilingual, Few-Shot Twi, and Supervised Twi.
Pidgin Selected: Engages Final_Multilingual, Few-Shot Pidgin, and Supervised Pidgin.
Display:
The Forum displays the message (flagged if any model crosses the threshold).
The Monitor displays a comparative table showing each model's label and probability score.

### 3. Comparative "Monitor" Specifications
The Monitor side should provide an "at-a-glance" performance view:
Score Comparison: A table or set of metric cards showing the Toxicity Probability for each active model.
Model Labels: Color-coded status for each model (e.g., Green for "Neutral", Red for "Hate Speech").
Performance Delta: Highlighting cases where one model flags a sentence (e.g., Few-Shot) while another misses it (e.g., Multilingual).

### 4. Reference Implementation Details
#### Sample Data Pool (African Dialects)
Language
Sample Starter Sentences
Twi
"Wo gyimi dodo" (Toxic), "Me pɛ sika" (Neutral), "Kwasiafoɔ yi" (Toxic)
Pidgin
"You be mumu" (Toxic), "How you dey?" (Neutral), "I go finish you" (Toxic)

#### Logic Hook for AI Implementation
Python
# Model Mapping Logic
MODELS = {
    "Twi": ["Final_Multilingual", "Few-Shot Twi", "Supervised Twi"],
    "Pidgin": ["Final_Multilingual", "Few-Shot Pidgin", "Supervised Pidgin"]
}

# Column Setup
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Forum Feed")
    # Display message bubbles and handle chat_input

with col2:
    st.header("Model Monitor")
    # Loop through active models and display inference results
    # st.metric(label=model_name, value=f"{prob:.2f}", delta=label)


### 5. Key Success Metrics for the Demo
Accuracy Visualization: The goal is to show where specific local dialect models outperform general multilingual models.
Transparency: Use a "Processing..." spinner for each model to indicate independent analysis.
No Persistence: Remind viewers that the forum is a "live sandbox" only.

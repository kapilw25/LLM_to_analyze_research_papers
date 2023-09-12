import streamlit as st
from main import extract_features_from_pdf, pdf_texts, pdf_names
import sys

st.write(sys.executable)

def get_features_for_pdf(pdf_text):
    #st.write("Fetching features for PDF text...")  # Debug
    features = extract_features_from_pdf(pdf_text)
    #st.write(f"Extracted features: {features}")  # Debug
    return features

def main():
    st.title("Chatbot (GPT-3.5) to study research papers for Drone Surveillance Under Prof. Jerry Gao")
    
    selected_paper = st.selectbox("Choose a research paper:", pdf_names)
    index = pdf_names.index(selected_paper)
    
    if st.button("Display Features"):
        features = get_features_for_pdf(pdf_texts[index])
        for feature, data in features.items():
            st.write(f"{feature}: {data}")

if __name__ == "__main__":
    main()

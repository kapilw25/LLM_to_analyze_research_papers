import os
import re
from pdfminer.high_level import extract_text
import openai
import spacy
import streamlit as st

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

SECTIONS = [
    "Title", "Abstract", "Introduction", "Literature Review", "Methodology", 
    "Methods", "Experiment", "Results", "Discussion", "Conclusion", 
    "Future Work", "Recommendations", "Acknowledgments", "References", "Bibliography", "Appendices"
]

SECTION_REGEX = r'(?i)(\d+\.?\s*)?({})'

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def get_pdf_files_from_directory(directory_path):
    all_files = os.listdir(directory_path)
    pdf_files = [f for f in all_files if f.lower().endswith('.pdf')]
    return [os.path.join(directory_path, pdf_file) for pdf_file in pdf_files]

def extract_sections_from_text(text):
    sections_content = {}
    for section in SECTIONS:
        match = re.search(SECTION_REGEX.format(section), text)
        if match:
            start_idx = match.start()
            next_sections = [re.search(SECTION_REGEX.format(s), text[start_idx+1:]) for s in SECTIONS if s != section]
            next_sections = [ns for ns in next_sections if ns]
            end_idx = next_sections[0].start() + start_idx + 1 if next_sections else None
            sections_content[section] = text[start_idx:end_idx].strip()
    return sections_content

directory_path = '/Users/kapilwanaskar/Library/CloudStorage/GoogleDrive-kapil.wanaskar@sjsu.edu/My Drive/Projects/LLM_to_analyze_research_papers/PDFs'
pdf_paths = get_pdf_files_from_directory(directory_path)
pdf_texts = [extract_text_from_pdf(pdf) for pdf in pdf_paths]
pdf_names = [os.path.basename(pdf)[:-4] for pdf in pdf_paths]

openai.api_key = os.getenv("OPENAI_API_KEY")


def chunk_content(text, max_length=4000):
    """Breaks the text into chunks that don't exceed max_length characters, and does not cut off in the middle of a sentence."""
    doc = nlp(text)
    chunks = []
    current_chunk = ""
    current_length = 0
    for sentence in doc.sents:
        current_length += len(sentence.text)
        if current_length < max_length:
            current_chunk += sentence.text
        else:
            chunks.append(current_chunk)
            current_chunk = sentence.text
            current_length = len(sentence.text)
    if current_chunk:  # For the last chunk
        chunks.append(current_chunk)
    return chunks

def get_gpt_response(prompts, pdf_text):
    CHUNK_SIZE = 4000  # Adjust if needed
    
    # Break pdf_text into chunks using spaCy's sentence tokenization
    chunks = chunk_content(pdf_text, CHUNK_SIZE)
    
    #st.write(f"Number of chunks: {len(chunks)}")  # Debug
    
    responses = []
    for chunk in chunks:
        combined_prompts = "\n".join([f"{key}: {value}" for key, value in prompts.items()])
        prompt_with_context = f"The following is an excerpt from a research paper on Drone Surveillance:\n\n{chunk}\n\n{combined_prompts}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt_with_context,
            max_tokens=300  # Increasing max tokens as we're asking multiple questions.
        )
        responses.append(response.choices[0].text.strip())
    
    # Combine responses
    combined_response = "\n".join(responses)
    #st.write(f"GPT-3 combined response: {combined_response}")  # Debug
    return combined_response



def extract_features_from_pdf(pdf_text):
    features_prompts = {
        'Dataset': "Which video dataset recorded by drones is mentioned?",
        'Proposed Model': "What is the proposed model or algorithm for anomaly detection?",
        'Baseline Models': "Which models are used as a baseline or for evaluation purposes?",
        'Anomaly Type': "What kind of anomalies are discussed?",
        'Context': "In what context or setting is the drone surveillance applied?",
        'Metrics': "Which performance or evaluation metrics are used?"
    }
    
    response = get_gpt_response(features_prompts, pdf_text)
    # Parsing the response to extract answers to each question
    lines = response.split("\n")
    features_data = {}
    for line in lines:
        for key in features_prompts.keys():
            if line.startswith(key):
                split_line = line.split(":")
                if len(split_line) > 1:
                    features_data[key] = split_line[1].strip()
                else:
                    features_data[key] = ""  # or some default value

    return features_data

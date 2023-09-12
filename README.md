# LLM to Analyze Research Papers

This project extracts and studies features from research papers on Drone Surveillance using GPT-3.5 and presents the results using the Streamlit framework.

## Overview

1. `main.py`: This script is responsible for:
    - Extracting text from provided PDF files.
    - Breaking the text content into readable chunks.
    - Interacting with the OpenAI GPT-3.5 model to understand and extract features from the papers.

2. `streamlit_app.py`: A Streamlit web application where users can select a specific research paper and view its extracted features.

## Features

The system will extract the following sections from research papers:
- Title
- Abstract
- Introduction
- Literature Review
- Methodology
- Methods
- Experiment
- Results
- Discussion
- Conclusion
- Future Work
- Recommendations
- Acknowledgments
- References
- Bibliography
- Appendices

Furthermore, specific features such as the dataset used, proposed model, baseline models, anomaly type, context, and evaluation metrics are derived with the help of the GPT-3.5 model.

## Prerequisites

- Python 3.x
- [pdfminer](https://pypi.org/project/pdfminer.six/)
- [openai](https://pypi.org/project/openai/)
- [spacy](https://spacy.io/)
- [streamlit](https://www.streamlit.io/)
- [spaCy model](https://spacy.io/models/en) (`en_core_web_sm`)

## Usage

1. Ensure you have all the necessary prerequisites installed.
2. Clone the repository:
    ```
    git clone https://github.com/kapilw25/LLM_to_analyze_research_papers.git
    ```
3. Navigate to the cloned repository's directory.
4. Run the Streamlit application:
    ```
    streamlit run streamlit_app.py
    ```

## Note

Make sure to set your OpenAI API key in the environment variables as `OPENAI_API_KEY` to ensure proper functioning of the GPT-3.5 model interactions.

## Future Work

- Improve section extraction for better accuracy.
- Incorporate more features based on feedback.

---

**Author:** Kapil Wanaskar
**Project Under:** Prof. Jerry Gao

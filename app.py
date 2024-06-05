import streamlit as st
from main import *
from utils.htmlTemplates import css

# Streamlit UI
def streamlit_ui():
    
    st.title("Webscraper Chatbot")
    query = st.text_input("Enter your question:")
    if st.button("Ask"):
        obtain_db = main()
        if obtain_db:
            response = query_model(query, obtain_db)
            response = response['output_text']
            st.markdown(f'<div class="response"><p class="response-text">{response}</p></div>', unsafe_allow_html=True)
        else:
            st.error("Failed to obtain database.")


def render():
    st.write(css, unsafe_allow_html=True)
    streamlit_ui()

if __name__ == "__main__":
    render()
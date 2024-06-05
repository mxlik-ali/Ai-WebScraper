from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import retrieval_qa
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import numpy as np 

def vector_db(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(chunks,embedding = embeddings)
    vector_store.save_local("faiss_index")


def get_conversational_chain():
    prompt_template ="""
    Answer the questions as detailed as possible from the provided context, make sure toprovide all details,
    if the answer is not in the provided context just say "Answer is not available in the context".
    Make it descriptive as much as you like make sure to give specific important details
    Dont provide the wrong answer\n
    context:\n {context} \n
    Question: \n {question} \n

    Answer:
    """
    model= ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context","question"])
    chain = load_qa_chain(model,chain_type="stuff",prompt=prompt)
    return chain



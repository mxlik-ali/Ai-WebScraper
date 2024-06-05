from utils.chunks import convert_to_chunks
from utils.vector_db import vector_db, get_conversational_chain
from utils.htmlTemplates import css  
from api_config.vision import *
from api_config.vision_scrape import *

import google.generativeai as genai
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_qa_with_sources_chain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_google_genai import ChatGoogleGenerativeAI

import os
import json
import glob
import time
import streamlit as st
# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

def get_all_jpg_files(folder_path):
    # Ensure the folder path exists
    if not os.path.isdir(folder_path):
        raise ValueError(f"Folder {folder_path} does not exist")
    
    # Get all .jpg files in the folder
    jpg_files = glob.glob(os.path.join(folder_path, "*.jpg"))
    
    return jpg_files

def existence(path):
    return os.path.exists(path)

def query_model(query, new_db):
    if new_db:
        docs = new_db.similarity_search(query)
        chain = get_conversational_chain()
        response = chain.invoke(
            {"input_documents": docs, "question": query},
            return_only_outputs=True
        )
        print('Response generated with status code 200')
    else:
        print("Database not available for querying.")
    return response

def wait_for_images(folder_path, expected_count, max_wait_time=60, check_interval=2):
    elapsed_time = 0
    while elapsed_time < max_wait_time:
        jpg_files = get_all_jpg_files(folder_path)
        if len(jpg_files) >= expected_count:
            return jpg_files
        time.sleep(check_interval)
        elapsed_time += check_interval
        print(f"Waiting for images... {elapsed_time}/{max_wait_time} seconds elapsed")
    return jpg_files

def main():
    # Paths for files
    url = os.getenv('URL')
    sitemap_path = './scrape/sitemap.json'
    faiss_index_path = "./faiss_index"
    # query = 'Who is Luke Skywalker?'
    try:
        sitemap_exists = existence(sitemap_path)
        print(f'Does site map exists : {sitemap_exists}')
        


        if not sitemap_exists:
            # URL of the Wikipedia page
            print('Starting the webscraping process')
            url = url
            input_for_vision = scraper_main(url)
            folder_path = './image_saves'
            expected_image_count = 2  # Adjust based on your expected count
            jpg_files = wait_for_images(folder_path, expected_image_count)



            # Debugging print to check if jpg_files list is populated
            print(f"Extracted files from the website in jpg form: {jpg_files}")

            if not jpg_files:
                raise ValueError("No jpg files found in the scrape folder.")
            page_structure = []

            for files in jpg_files:
                b64_image = image_b64('./image_saves/screenshot1.jpg')
                print('Processing the generated images')
                response = gen_vision(b64_image)
                page_structure.append(response)
            

            with open(sitemap_path, 'w', encoding='utf-8') as f:
                json.dump(page_structure, f, ensure_ascii=False, indent=4)

            # with open('html.txt', 'w', encoding='utf-8') as f:
            #     f.write(str(page_structure))

        faiss_exists = existence(faiss_index_path)
        # print(faiss_exists)
        if not faiss_exists:
            # Load the sitemap from file
            if  sitemap_exists:
                with open(sitemap_path, 'r', encoding='utf-8') as f:
                    page_structure = json.load(f)
                    print('opened sitemap')

            chunks = convert_to_chunks(str(page_structure))
            with open('./test/chunks.txt', 'w', encoding='utf-8') as f:
                f.write(str(chunks))

            # Create and save FAISS index
            vectorized_embedding = vector_db(chunks)
            new_db = FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)
        

        else:
            # Load the FAISS index
            new_db = FAISS.load_local("faiss_index",embeddings,allow_dangerous_deserialization=True)
        
        
        return new_db
    except Exception as e:
        print(f"An error occurred: {e}")




if __name__ == "__main__":
    main()
    print('Webscraping process completed , Run app.py to access the Chatbot !!!')




## IGNORE
# query = 'give me a summary of the information you have'     
# obtain_db = main()
# query_model(query,obtain_db)

import base64
import os
from PIL import Image
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import google.generativeai as genai
#data:image/jpeg;base64,
def image_b64(image):
    with open(image,"rb") as f:
        return base64.b64encode(f.read()).decode()

def gen_vision(image_path):
    # Load environment variables from a .env file
    load_dotenv()

    # Get the Google API key from environment variables
    API_KEY = os.getenv('GOOGLE_API_KEY')
    if not API_KEY:
        raise ValueError("Google API key not found in environment variables")

    # Configure the ChatGoogleGenerativeAI model with the appropriate settings
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    max_tokens= 150000
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3,max_tokens=max_tokens)
    

    # Prepare the prompt


    llm = ChatGoogleGenerativeAI(model="gemini-pro-vision")
    # example
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": '''U are a webscraper that uses vision pro api to scrape the message content.
                            Do Not provide any type of information from any other knowledge base u have u just extract the information , and copy paste it
                            Now scrape everything ALL THE CONTENT inside and dont skip any part store it and make sure to give a response in json format(do not include any html tags), And do maintain the heirarchy
                            Even remember to skip the content that occurs twice or thrice in terms of data cleaning which is equal in all terms but if the year or anything is different count it
                            Please provide me full webscaping do not leave any content, The format of json is given below. Ive seen u skipping make part make sure to include the paragraphs present
                            ```
                            json
                            {
                                heading: 
                                content: write all text extracted in this subsection
                                subsection :{
                                                subsection:
                                                content: write all text extracted inside this subsection}#if subsection is present
                                {   
                                    skip using headers everytimeas key value instead frovide a list when it comes to rows and headers continue in same line
                                    table:
                                    headers:[1,2,3,4,5]#header example if present then only
                                    rows:[1,2,3,4,5]#row example (dont start all row elements on new line, one whole row in one line,
                                    
                                }
                            }''',
            },  # You can optionally provide text parts
            {"type": "image_url", "image_url":f"data:image/jpeg;base64,{image_path}"},
        ]
    )
    response = llm.invoke([message])
    return (response.content)



# b64_image = Image.open('./image_saves/combined_screenshots.jpg')
# b64_image = image_b64('./image_saves/screenshot1.jpg')
# response = gen_vision(b64_image)
# print(response)
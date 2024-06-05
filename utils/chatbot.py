import json
from dotenv import load_dotenv
import gradio
import os

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_qa_with_sources_chain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatOpenAI

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


# Initialize memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define the condense question prompt
condense_question_prompt = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.\
Make sure to avoid using any unclear pronouns.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
condense_question_chain = llm | PromptTemplate.from_template(condense_question_prompt)

# Define the QA chain
qa_chain = create_qa_with_sources_chain(llm)

# Define the document prompt
doc_prompt = PromptTemplate(
    template="Content: {page_content}\n",
    input_variables=["page_content"],
)

# Define the final QA chain
final_qa_chain = StuffDocumentsChain(
    llm_chain=qa_chain,
    document_variable_name="context",
    document_prompt=doc_prompt,
)

# Initialize the ConversationalRetrievalChain
retrieval_qa = ConversationalRetrievalChain(
    question_generator=condense_question_chain,
    retriever=db.as_retriever(),
    memory=memory,
    combine_docs_chain=final_qa_chain,
)

# Define the predict function
def predict(message, history):
    response = retrieval_qa.invoke({"question": message})
    print(response)

    responseDict = json.loads(response)
    answer = responseDict["answer"]
    # sources = responseDict["sources"]

    # if type(sources) == list:
    #     sources = "\n".join(sources)

    # if sources:
    #     return answer + "\n\nSee more:\n" + sources
    return answer

# Launch the Gradio interface
gradio.ChatInterface(predict).launch()
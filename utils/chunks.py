import json
from typing import List, Dict
from langchain.text_splitter import CharacterTextSplitter

# Function to convert the page structure into text chunks
def convert_to_chunks(page_structure: Dict) -> List[str]:
    

    # Add the intro section
    # if page_structure.get('intro'):
    #     chunks.append(page_structure['intro'])

    # Add each section and subsection
    # for section in page_structure['sections']:
    #     section_text = section['title'] + "\n" + "\n".join(section['content'])
    #     chunks.append(section_text)
    #     for subsection in section['subsections']:
    #         subsection_text = subsection['title'] + "\n" + "\n".join(subsection['content'])
    #         chunks.append(subsection_text)
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(page_structure)
    
    return chunks

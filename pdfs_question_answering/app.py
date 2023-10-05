import yaml
import streamlit as st

from langchain import OpenAI, VectorDBQA, LLMChain
from langchain.prompts import PromptTemplate

from pdf_loaders import PdfToTextLoader
from dataset_vectorizers import DatasetVectorizer

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

OPENAI_API_KEY = config['OPENAI_KEY']
PDFS, NAMES, TXTS = [], [], []
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 500

# ----- Header of the app -----
st.title("Moto Repair assistant")
st.write("Hey i'm your repair copilot, please feed me some repair documents and i'll be able to adress all your questions")

# ----- Select and upload the files one by one -----
st.header("Select the files to compare")
st.write("The files should be in PDF format ( With selectable text ).")
file_1 = st.file_uploader("File 1")
name_1 = st.text_input("Name of file 1", value="Plan 1")

# ----- Load the files -----
if file_1:

    with open("./data/" + file_1.name, "wb") as f:
        f.write(file_1.getbuffer())

    PDFS = ["./data/" + file_1.name]
    NAMES = [name_1]

    for pdf_path in PDFS:
        txt_path = pdf_path.replace(".pdf", ".txt")
        pdf_loader = PdfToTextLoader(pdf_path, txt_path)
        text = pdf_loader.load_pdf()
        TXTS.append(txt_path)
    st.write("Files loaded successfully.")

    dataset_vectorizer = DatasetVectorizer()
    documents_1, texts_1, docsearch_1 = dataset_vectorizer.vectorize([TXTS[0]], chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP, openai_key=OPENAI_API_KEY)
    llm = OpenAI(model_name='text-davinci-003', temperature=0, openai_api_key=OPENAI_API_KEY)
    qa_chain_1 = VectorDBQA.from_chain_type(llm=llm, chain_type='stuff', vectorstore=docsearch_1)
    st.write("Files vectorized successfully.")

    # ----- Write questions separated by a new line -----
    st.header("Questions : ")

    st.write("The questions should be separated by a new line.")
    questions = st.text_area("Questions", 
                             value = """
            How to know when to change the fuel ?""")
    QUESTIONS = questions.split("\n")
    QUESTIONS = [q.strip() for q in QUESTIONS if len(q) > 0]
  
    # ----- Generate the intermediate answers for the document summary -----
    summary_of_answers = ""
    for q in QUESTIONS:
        print(q)
        answer_1  = qa_chain_1.run(q)
        summary_of_answers += "Question: " + q + "\n"
        summary_of_answers += f"{NAMES[0]} answer: " + answer_1
        
    template = """
    I want you to act motor repair expert. 
    I have search the repair manual trying to answer the following questions :

    {QUESTIONS}
    Here is a list of answers i found in the repair manual
    {summary_of_answers}
    Your answer:
    """
    
    prompt = PromptTemplate(
        input_variables=["QUESTIONS","summary_of_answers"],
        template=template,
    )
    
    answer = ""
    llm = OpenAI(model_name='text-davinci-003', temperature=0, openai_api_key=OPENAI_API_KEY, request_timeout=60)
    chain = LLMChain(llm=llm, prompt=prompt)
    answer = chain.run({'summary_of_answers': summary_of_answers, 'QUESTIONS': QUESTIONS})
    # ----- Generate the final answer -----
    st.header("Final answer")
    st.write(answer)




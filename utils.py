import random
from pathlib import Path

from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from configs import *

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

FILES_PATH = Path(__file__).parent / "files"


def document_load():
    documents = []
    for file in FILES_PATH.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        document_file = loader.load()
        documents.extend(document_file)
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=250,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    documents = splitter.split_documents(documents)
    for i, doc in enumerate(documents, 1):
        doc.metadata['source'] = doc.metadata['source'].split("/")[-1]
        doc.metadata['doc_id'] = i

    return documents


def create_vector_store(documents):
    embedding_model = OpenAIEmbeddings()
    vector_store = FAISS.from_documents(
        documents = documents,
        embedding = embedding_model
    )


    return vector_store


def create_chat_chain():
    print(":: Carregando documentos")
    documents = document_load()
    print(":: Splitting documentos")
    documents = split_documents(documents)
    print(":: Criando vector store")
    vector_store = create_vector_store(documents)

    chat = ChatOpenAI(model=get_config("model_name"))
    memory = ConversationBufferMemory(
        return_messages=True, 
        memory_key="chat_history", 
        output_key='answer')
    
    retriever = vector_store.as_retriever(
        search_type=get_config("retrieval_search_type"),
        search_kwargs=get_config("retrieval_kwargs")
    )

    prompt_template = PromptTemplate.from_template(get_config("prompt"))
    
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        memory=memory,
        return_source_documents=True,
        verbose=True,
        retriever=retriever, 
        combine_docs_chain_kwargs={'prompt':prompt_template}
    )
    return chat_chain

def random_code():
    codigo = ''.join([str(random.randint(0, 9)) for _ in range(10)])
    return codigo



if __name__ == "__main__":
    
    chain = create_chat_chain()
    print(chain)

    resp = chain.invoke({'question':"Quem é José Wilson?"})
    print(resp['chat_history'])
    print(resp['chat_history'][-1].content)

import streamlit as st

MODEL_NAME = "gpt-4o"
RETRIEVAL_SEARCH_TYPE = "mmr"
RETRIEVAL_KWARGS = {
    'k': 5,
    'fetch_k': 20
}
PROMPT = """
    Você é um chatbot que responde perguntas sobre documentos PDF. Seu nome é Rebeca.
    No context o fornecido estão as informações dos documentos do usuário, utilize o contexto
    para responder as perguntas do usuário.
    Se vocêo não sabe a resposta, apenas diga que não sabe e não tente inventar a resposta.

    Contexto:
    {context}

    Conversa atual:
    {chat_history}

    Human: {question}
    AI: 
"""


def get_config(config_name):
    if config_name.lower() in st.session_state:
        return st.session_state[config_name.lower()]
    elif config_name.lower() == 'model_name':
        return MODEL_NAME
    elif config_name.lower() == 'retrieval_search_type':
        return RETRIEVAL_SEARCH_TYPE
    elif config_name.lower() == 'retrieval_kwargs':
        return RETRIEVAL_KWARGS
    elif config_name.lower() == 'prompt':
        return PROMPT
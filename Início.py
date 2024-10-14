import streamlit as st
from pathlib import Path
import time
from langchain.memory import ConversationBufferMemory

from utils import FILES_PATH, create_chat_chain, random_code


def sidebar():
    uploaded_files = st.file_uploader("Adicione seus arquivos", type=[".pdf"], 
                     accept_multiple_files=True)
    if uploaded_files:
        for file in FILES_PATH.glob("*.pdf"):
            file.unlink()

        for pdf in uploaded_files:
            with open(FILES_PATH / pdf.name, "wb") as f:
                f.write(pdf.read())    

    button_label = "Iniciar Chatbot"
    if 'chain' in st.session_state:
        button_label = "Atualizar Chatbot"
    
    if st.button(button_label, use_container_width=True):
        if len(list(FILES_PATH.glob("*.pdf"))) == 0:
            st.error("Nenhum arquivo foi carregado. Adicione algum arquivo PDF.")
        else:
            st.success("Iniciando chatbot...")
            chain = create_chat_chain()
            st.session_state['chain'] = chain
            st.rerun()

def chat_window():
    st.header("Bem-vindo ao nosso agente analisador de PDF's 🤖", divider=True)
    if not 'chain' in st.session_state:
        st.error("Para começar, adicione um arquivo PDF no menu lateral.")
        st.stop()

    chain = st.session_state['chain']
    memory = chain.memory

    messages = memory.load_memory_variables({})['chat_history']

    container = st.container()
    for msg in messages:
        chat = container.chat_message(msg.type)
        chat.markdown(msg.content)


    user_input = st.chat_input("Digite sua pergunta:")

    if user_input:
        chat = container.chat_message("human")
        chat.markdown(user_input)

        chat = container.chat_message("ai")
        chat.markdown("Gerando resposta...")


        chain.invoke({"question": user_input})
        st.rerun()



def main():
    with st.sidebar:
        sidebar()
    chat_window()


if __name__ == "__main__":
    main()
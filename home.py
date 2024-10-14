import streamlit as st
from pathlib import Path
import time

from utils import random_code

FILES_PATH = Path(__file__).parent / "files"

def create_session_chain():
    st.session_state['chain'] = True
    st.session_state['chain_code'] = random_code()
    time.sleep(1) 
    

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
            create_session_chain()
            st.rerun()


def chat_window():
    st.header("Bem-vindo ao nosso agente analisador de PDF's 🤖", divider=True)
    if not 'chain' in st.session_state:
        st.write("Para começar, adicione um arquivo PDF no menu lateral.")
        st.stop()

def main():
    with st.sidebar:
        sidebar()
    chat_window()


if __name__ == "__main__":
    main()
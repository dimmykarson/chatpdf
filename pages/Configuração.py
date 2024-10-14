from utils import FILES_PATH, create_chat_chain
import streamlit as st
from configs import get_config
import json

def config_page():
    st.header("Página de Configuração", divider=True)

    model_name = st.text_input('Modifique o modelo', 
                               value=get_config('model_name'))
    retrieval_search_type = st.text_input('Modifique o tipo de retrieval', 
                                          value=get_config('retrieval_search_type'))
    retrieval_kwargs = st.text_input('Modifique os parâmetros de retrieval', 
                                     value=json.dumps(get_config('retrieval_kwargs')))
    prompt = st.text_area('Modifique o prompt padrão', height=350, 
                          value=get_config('prompt'))
    
    if st.button("Salvar configurações",  use_container_width=True):
        st.session_state['model_name'] = model_name
        st.session_state['retrieval_search_type'] = retrieval_search_type
        st.session_state['retrieval_kwargs'] = json.loads(retrieval_kwargs)
        st.session_state['prompt'] = prompt
        st.success("Configurações salvas com sucesso!")

    if st.button('Atualizar ChatBot', use_container_width=True):
       if len(list(FILES_PATH.glob('*.pdf'))) == 0:
           st.error('Adicione arquivos .pdf para inicializar o chatbot')
       else:
           st.success('Inicializando o ChatBot...')
           create_chat_chain()
           st.rerun()

config_page()
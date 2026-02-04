import ollama
import streamlit as st

st.set_page_config(
    page_title='Chat with some AI!',
    page_icon=':robot:',
    layout='wide'
)

available_models = ['phi3', 'gemma:2b', 'qwen3:8b']
selected_model = st.sidebar.selectbox('Выберите модель:', available_models)
MODEL_NAME = selected_model

def ensure_model_available():
    try:
        ollama.show(MODEL_NAME)
    except:
        with st.spinner(f'Загружаем модель {MODEL_NAME}... Это может занять несколько минут.'):
            ollama.pull(MODEL_NAME)

# Добавьте это в начало после определения MODEL_NAME
ensure_model_available()

if 'chat' not in st.session_state:
    st.session_state.chat = []

st.title('Чат с локальным Nскуственным Nнтеллектом!')

for message in st.session_state.chat:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

def get_ollama_response(messages):
    try:
        ollama_messages = []
        for msg in messages:
            role = 'user' if msg['role'] == 'user' else 'assistant'
            ollama_messages.append({'role': role, 'content': msg['text']})
        
        response = ollama.chat(
            model=MODEL_NAME,
            messages=ollama_messages,
            options={
                'temperature': 0.7,
                'top_p': 0.9,
                'max_tokens': 500,
            }
        )
        
        return response['message']['content']
    except Exception as e:
        return f'Ошибка при обращении к модели: {str(e)}'

if prompt := st.chat_input("Что спрашиваем?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.chat.append({'role': 'user', 'text': prompt})
    
    with st.chat_message('model'):
        with st.spinner('Думаю...'):
            response = get_ollama_response(st.session_state.chat)
        st.markdown(response)
    
    st.session_state.chat.append({'role': 'model', 'text': response})

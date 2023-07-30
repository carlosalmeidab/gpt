import openai
import streamlit as st

titulo = st.title("Chat GPT - Meu Orientador")
st.session_state["openai_model"] = st.selectbox("Modelo: ", ('gpt-4', 'gpt-3.5-turbo'))

openai.api_key = st.secrets["OPENAI_API_KEY"]

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Você é um assitente carismático"}]

with st.sidebar:
    with st.expander("Instruções para Assistente"):
        system = st.text_area("System")
           
for message in st.session_state.messages:
    if message["role"]!="system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    elif message["role"]=="system":
        message["content"]= system
      
if prompt := st.chat_input("Digite aqui sua mensagem?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        titulo = "maralhi"


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
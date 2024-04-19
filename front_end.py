import streamlit as st
import lang_stuff as lang_stuff
from PIL import Image

st.title("Stock Visualization")
st.divider()

if 'log_user' not in st.session_state:
    st.session_state.log_user = []
    st.session_state.log_assistant = []
    st.session_state.log_graphs = []

prompt = st.chat_input(key="test", placeholder='Type prompt here...', disabled=False)
if prompt:
    try:
        if ("PE" in prompt) or ("news" in prompt) or ("pe" in prompt) or ("p/e" in prompt)or ("news" in prompt) or ("p/e" in prompt) or ("min" in prompt) or ("max" in prompt) or ("summarize" in prompt):
            result = lang_stuff.analysis_answer.run(prompt)
        elif ("chart" in prompt) or ("visualize" in prompt) or ("graph" in prompt):
            result = lang_stuff.basic_visual_answer.run(prompt)
        else:
            result = lang_stuff.wiki_answer.run(prompt)
    except: 
        result = "Prompt resulted in error."

    st.session_state.log_user.append(prompt)
    try:
        st.session_state.log_assistant.append(result["output"])
    except:
        st.session_state.log_assistant.append(result)
    
    img = Image.open('test.jpeg')
    st.session_state.log_graphs.append(Image.open('test.jpeg'))

    for i in range(len(st.session_state.log_assistant)):
        new_user = st.chat_message("user")
        new_user.write(st.session_state.log_user[i])
        new_assistant = st.chat_message("assistant")
        new_assistant.write(st.session_state.log_assistant[i])
        img = st.session_state.log_graphs[i]
        st.image(img,caption='Latest Graph')
        st.divider()
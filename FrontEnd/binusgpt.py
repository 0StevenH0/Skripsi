import streamlit as st
from openai import OpenAI


import streamlit as st

# Custom CSS for layout
st.markdown(
    """
    <style>
    .top-left {
        position: fixed;
        top: 50px;
        left: 50px;
        display: flex;
        align-items: center;
    }
    .top-left img {
        height: 40px;  
        margin-right: 10px;
    }
    .top-right {
        position: fixed;
        top: 50px;
        right: 50px;
    }
    .top-right button {
        font-size: 30px;  /* Adjust button size as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Place logo and text
st.markdown(
    """
    <div class="top-left">
        <img src="https://drive.google.com/file/d/1nCNeKbbvD0bL_P0G4wLHquMO8JRkxMh6" alt="Logo">
        <span><b>BINUSGPT</b></span>
    </div>
    """,
    unsafe_allow_html=True
)


# Place settings button
st.markdown(
    """
    <div class="top-right">
        <button onclick="alert('Settings clicked')">⚙</button>
    </div>
    """,
    unsafe_allow_html=True
)

client = OpenAI(api_key=st.secrets["OPENAI_API_SECRET_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Init chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
prompt = st.chat_input("Ask me about BINUS Enrichment Program...")
if prompt:
    # Display user message in chat message container
    with st.chat_message("user", avatar="👱🏻‍♂"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"{prompt}"

    # Display assistant message in chat message container

    # Openai based
    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""
    #     for response in client.chat.completions.create(model = st.session_state["openai_model"],
    #     messages = [
    #         {"role" : m["role"], "content" : m["content"]}
    #         for m in st.session_state.messages
    #     ],
    #     stream = True):

    #         full_response += response.choices[0].delta.get("content", "")
    #         message_placeholder.markdown(full_response + "⎸ ")
    #     message_placeholder.markdown(full_response)
    # st.session_state.messages.append({"role" : "assistant", "content" : full_response})





    ### Code to make assitant repeat user prompt
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content":response})
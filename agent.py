from dotenv import load_dotenv
import streamlit as st

from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


load_dotenv() #load OpenAI key

# app config
st.set_page_config(page_title="Artist Creativity Tool")
st.title("Artist Creativity Tool")

#agent
def artist_style(user_query, chat_reply):

    template = """
    You are a creative writer and curator. In the {user_question} you will receive an artist name and it's style.
    Learn from the style. 
    
    Ask: "Please type another word".
     
    Think: Use what you have learned from the previous style as inspiration to explain the new word that the user will input in {chat_reply} in the same style.
    Find synonyms for the adjectives and use them instead. Don't refer to artist name in reply, or mention art or artwork.
    
    Begin!
    
    Chat reply: {chat_reply}

    User question: {user_question}

    

    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatOpenAI(temperature=0.6) #tweak imagination
        
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({
        "chat_reply": chat_reply,
        "user_question": user_query,
    })

# session state
if "chat_reply" not in st.session_state:
    st.session_state.chat_reply = [
        AIMessage(content="Hello, I am your creative assisant."),
    ]

    
# conversation
for message in st.session_state.chat_reply:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# user input
user_query = st.chat_input("Enter the artist name and description")
if user_query is not None and user_query != "":
    st.session_state.chat_reply.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = st.write_stream(artist_style(user_query, st.session_state.chat_reply))

    st.session_state.chat_reply.append(AIMessage(content=response))
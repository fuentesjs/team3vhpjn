from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client
from qdrant_client import QdrantClient
import streamlit as st
import os

def stMain():

  os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
  qdrant_api_key = st.secrets['API_KEY']
  os.environ['API_KEY'] = qdrant_api_key 

  st.header(":blue[_Virtual Student Advisor for Franklin University_]")
  new_session = False
  end_chat = False
  new_session = st.sidebar.checkbox("Reset Chat History")
  end_chat = st.sidebar.checkbox("Exit Chat")

  embed_model = 'local:hkunlp/instructor-large'
  Settings.embed_model = embed_model

  # Initialize Qdrant Client
  qdrant_client = QdrantClient(
      url="https://4f411c47-4cba-4085-810c-dafbb4ca3bc3.us-east4-0.gcp.cloud.qdrant.io:6333",
      api_key=qdrant_api_key ,
  )

  #load vector store from Qdrant db
  vector_store = QdrantVectorStore(client=qdrant_client, collection_name="mycollection", enable_hybrid=True)

  #Get vector index from vector store
  vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

  #memory = ChatMemoryBuffer.from_defaults(token_limit=1048)

  #initialize chat engine
  chat_engine = vector_index.as_chat_engine(chat_mode="context",response_mode="compact",max_new_tokens=1024,
                                        system_prompt=("You are a chatbot, able to have normal interactions, as well as talk about Franklin University")
                                        )
  count = 0

  while not end_chat:
    count += 1

    #request prompt from user
    prompt = None
    st_message = st.chat_message("user")
    prompt = st_message.chat_input("Ask me a question about Franklin University!")
    more = True

    #wait for prompt from user
    #with st.sidebar.status("Waiting for prompt from you ..."):
    while more:
        if( prompt is None or len(prompt) <= 0):
            more = True
        else:
            more = False

    #write prompt on chat window
    if prompt is not None or len(prompt) > 0:
        prompt = str(prompt)
        st_message = st.chat_message("user")
        st_message.write(prompt)
        st.write(" ")

        #Get response for user from chat engine
        response = None
        #with st.sidebar.status("Waiting for response from AI..."):
        response = chat_engine.chat(prompt)

        #write response on chat window
        if response is not None or len(response) > 0:
            response = str(response)
            if prompt and response:
                st_message = st.chat_message("assistant")
                st_message.write(response)
                st.write(" ")

    new_session = st.sidebar.checkbox("Reset Chat History")
    end_chat = st.sidebar.checkbox("Exit Chat")
    
    # reset chat history
    if new_session:
       chat_engine.reset()
       new_session = False

    #rerun chat to avoid multiple instances and out of memory
    st.stop()
    st.rerun()
    st.header(":blue[_Virtual Student Advisor for Franklin University_]")
    new_session = False
    #end_chat = False
    new_session = st.sidebar.checkbox("Reset Chat History")
    end_chat = st.sidebar.checkbox("Exit Chat")

  st.stop()


if __name__ == "__main__":
  stMain()

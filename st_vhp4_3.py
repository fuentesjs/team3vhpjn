from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import Settings
import streamlit as st
import os
from google.colab import userdata


def initSession():
  st.session_state["count"] = "0"
  st.session_state["exit_chat"] = False
  st.session_state["reset_chat"] = False
  st.session_state["prompt"] = False
  st.session_state["response"] = False
  st.session_state["user_prompt"] = ""
  st.session_state["assistant_response"] = ""
  
  
  
def startChat():

  st.header(":blue[_Virtual Student Advisor for Franklin University_]")
  st.session_state["reset_chat"] = st.sidebar.checkbox("Reset Chat History",value=False,on_change=onResetChat)
  st.session_state["exit_chat"] = st.sidebar.checkbox("Exit Chat", value=False, on_change=onExitChat)

  exit_chat = st.session_state["exit_chat"]
  if exit_chat:
    exitChat()

  reset_chat = st.session_state["reset_chat"]
  if reset_chat:
    resetChat()

  os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
  openai_api_key = userdata.get('OPENAI_API_KEY')
  os.environ['OPENAI_API_KEY'] = openai_api_key

  embed_model = 'local:hkunlp/instructor-large'
  Settings.embed_model = embed_model

  # rebuild storage context from context store
  storage_context = StorageContext.from_defaults(persist_dir="/content/context")

  # load index from storage context
  index_id = "b222c1d4-6938-493c-b340-5e714a0fd621"
  vector_index = load_index_from_storage(storage_context,index_id)

  #memory = ChatMemoryBuffer.from_defaults(token_limit=1048)

  #initialize chat engine
  chat_engine = vector_index.as_chat_engine(chat_mode="context",response_mode="compact",max_new_tokens=1024,
                                        system_prompt=("You are a chatbot, able to have normal interactions, as well as talk about Franklin University")
                                        )

  #Initialize chat history if it has not
  if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

  # Display chat history
  for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
      st.markdown(message["string"])

  st.session_state["count"] = "0"
  count = int(st.session_state["count"])
  print(f"Count S0: {count}")
  count += 1
  print(f"Count S1: {count}")
  st.session_state["count"] = str(count)
  print(f"Count S2: {str(count)}")
  with st.chat_message("assistant"):
    st.session_state["user_prompt"] = st.chat_input("Ask me a question about Franklin University!",key=str(count))
    if st.session_state["user_prompt"]:
        onChatInput(chat_engine)


def resetChat():
  st.session_state.chat_history= []

def onResetChat():
  st.session_state["reset_chat"] = not st.session_state["reset_chat"]
  reset_chat = st.session_state["reset_chat"]
  print(f"This is reset chat History {reset_chat}")

def exitChat():
  st.session_state.chat_history= []
  print("Exiting Chat")
  #Stop Streamlit Execution
  st.stop()

def onExitChat():
  st.session_state["exit_chat"] = not st.session_state["exit_chat"] 
  exit_chat = st.session_state["exit_chat"]
  print(f"This is exit chat {exit_chat}")

def onChatInput(chat_engine):
  count = st.session_state["count"]
  #Update prompt from last prompt in session state
  prompt = st.session_state["user_prompt"]
  if prompt == None:
    print(f"Prompt is None: {prompt}, Count: {count}, Initializing Session")
    initSession()
    return
  else:
    print(f"Prompt: {prompt}, Count: {count}")
    
    if prompt:
        #Add prompt to chat history
        prompt = str(prompt)
        st.session_state.chat_history.append({"role": "user", "string": prompt})

        #Get response for user from chat engine
        response = None
        response = chat_engine.chat(prompt)
        #update last assistant response
        st.session_state["assistant_response"] = response
        print(f"Response: {response}, Count: {count}")

        
        if response:
            #Add response to chat history
            response = str(response)
            st.session_state.chat_history.append({"role": "assistant", "string": response})

    count = int(st.session_state["count"])
    print(f"Count R0: {count}")
    count += 1
    print(f"Count R1: {count}")
    st.session_state["count"] = str(count)
    print(f"Count R2: {str(count)}")
    #with st.chat_message("assistant"):
    #st.session_state["user_prompt"] = st.chat_input("Ask me a question about Franklin University!",key=str(count),on_submit=onChatInput)


if __name__ == "__main__":
  loop = 0
  print(f"Looping {loop}")
  #Start Streamlit Chat
  startChat()

  st.stop()
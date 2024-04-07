from ast import And
import streamlit as st

st.title("Virtual Human Advisor")

prompt = st.chat_input("Enter your query")

response = 'The requirements for your query vary.  Please consult with your advisor'

if prompt and response:
    st.write(response)

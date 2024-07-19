import streamlit as st
import cohere
import anthropic
import os
from dotenv import load_dotenv

#Retrive all API KEYS
load_dotenv()

anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
cohere_api_key = os.getenv('COHERE_APY_KEY')

#Set Streamlit Objects
st.title("*UNIVERSITY INTERN PROJECT*")

#form to prompts
with st.form("Main form"):
   
   ml_selected = st.radio(
    "**Select one of the language model**",
    ["*Claude 3.5 Sonnet*",  "*Cohere R+*"],
   )
   
   #Text prompts
   prompt_message = st.text_area(
    "*Text*",
    "Ask me everything",
    max_chars= 100,
    placeholder="e.g. Explain the Bayes Theorem"
    )
   
   #image prompts
   #uploaded_file = st.file_uploader("Upload file")

   submit_button = st.form_submit_button(label='Submit')

   if submit_button:
        st.write("Model language selected: ", ml_selected)
        st.write("Prompt message : ", prompt_message)

        #Select Language model to use
        match ml_selected:
            #Anthropic Claude 3.5 Sonnet
            case "*Claude 3.5 Sonnet*":
                client = anthropic.Anthropic(api_key=anthropic_api_key)
                message = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=200,
                    temperature=0,
                    system="",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt_message
                                }
                            ]
                        }
                    ]                
                )
                print("Tipo message: "+ type(message).__name__ + " Tipo message.content " + type(message.content).__name__)
                print(message.content)
                #Message un oggetto che contiene come attributo content(tipo lista) e ogni elemento della lista contiene un blocco testo(text)
                for block_text in message.content:
                    st.write(block_text.text)                

                st.write()
            #Cohere R+
            case "*Cohere R+*":
                co = cohere.Client(cohere_api_key)
                response = co.chat(
                    message = prompt_message
                    )
                print(response)
                st.write(response)
            case _:
                print("invalid option!")
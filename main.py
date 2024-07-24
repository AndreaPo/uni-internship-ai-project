import streamlit as st
import cohere
import show_api_message
import anthropic
import json
import re
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
   with st.chat_message("User"):
       prompt_message = st.text_area(
           "*User*",
           "Ask me everything",
           max_chars= 1000,
           placeholder="e.g. Explain the Bayes Theorem"
        )

   submit_button = st.form_submit_button(label='Submit')
   st.divider()

   if submit_button:
        with st.chat_message("Assistant"):
            st.write("Model language selected: ", ml_selected)
            st.write("Prompt message : ", prompt_message)

        #Select Language model to use
        match ml_selected:
            #Anthropic Claude 3.5 Sonnet
            case "*Claude 3.5 Sonnet*":
                try:
                    client = anthropic.Anthropic(api_key=anthropic_api_key)
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20240620",
                        max_tokens=300,
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

                    show_api_message.show_Sonnet_message(message)

                    with st.chat_message("Assistant"):
                        #Message un oggetto che contiene come attributo content(tipo lista) e ogni elemento della lista contiene un blocco testo(text)
                        for block_text in message.content:
                            st.write(block_text.text)    

                except anthropic.AuthenticationError as e:
                    print(f"Si è verificato un errore : {e}") 
                    st.write(f"Si è verificato un errore : {e}")                    
                
            #Cohere R+
            case "*Cohere R+*":
                try:
                    co = cohere.Client(cohere_api_key)
                    response = co.chat(
                        message = prompt_message
                    )
                    show_api_message.show_command_r_message(response)
                    with st.chat_message("Assistant"):
                        st.write(response.text) 

                    regex =r'(\{.*\})'
                    match_result =re.search(regex, response.text, re.DOTALL)
                    
                    string_to_convert = match_result.group()
                    print(string_to_convert)

                    if match_result:
                        print("Json trovato!")
                        string_to_convert = match_result.group()
                        json_response = json.loads(string_to_convert)
                        print(json_response["traccia"])
                        print(json_response["ragionamento"])
                        print(json_response["formula"])
                        print(json_response["soluzione"])
                    else:
                        print("json non trovato")
 
                except Exception as e:
                    print(f"Si è verificato un errore: {e}")
                    st.write(f"Si è verificato un errore : {e}")  
            case _:
                print("invalid option!")
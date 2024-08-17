import streamlit as st
import cohere
import show_api_message
import anthropic
import os
from dotenv import load_dotenv
from claude_sonnet import *
from command_r_plus import *
from create_json_response import *

#Retrive all API KEYS
load_dotenv()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
cohere_api_key = os.getenv('COHERE_APY_KEY')

response_names = ["PROBLEM","REASONING", "FORMULA", "SOLUTION"]

if 'response_values' not in st.session_state:
    st.session_state['response_values'] = [None, None, None, None]

prompt_description = ", crea JSON solo 4 attributi( traccia: traccia problema, ragionamento: ragionamento arrivare formula, formula: formula usare(no descrizioni), soluzione: soluzione con formula) no ulteriori descrizioni, no sottoattributi innestati"

#Set Streamlit Objects
st.title("*UNIVERSITY INTERN PROJECT*")

#form to prompts
with st.form("Main form"):
   
   ml_selected = st.radio(
    "**Select one of the language model**",
    ["*Claude 3.5 Sonnet*",  "*Command R+*"],
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

        full_prompt = prompt_message + prompt_description
        
        #Select Language model to use
        match ml_selected:
            #Anthropic Claude 3.5 Sonnet
            case "*Claude 3.5 Sonnet*":
                try:
                    claude_sonnet = ClaudeSonnet(api_key=anthropic_api_key)

                    connection_client = claude_sonnet.get_connection_client()

                    response = claude_sonnet.txt_message_create(my_connection_client=connection_client, my_prompt=full_prompt)

                    show_api_message.show_Sonnet_message(response)

                    response_txt = ""

                    #Response.content (type = list) every list element has a block text
                    for block_text in response.content:
                        response_txt += block_text.text

                    extract_json(my_response_txt=response_txt)

                except anthropic.AuthenticationError as e:
                    print(f"Si è verificato un errore : {e}") 
                    st.write(f"Si è verificato un errore : {e}")                    
                
            #Cohere R+
            case "*Command R+*":
                try:
                    command_r_plus = Command_r_plus(cohere_api_key)

                    command_r_plus_conncection = command_r_plus.get_connection()

                    response = command_r_plus.txt_message_chat(my_connection_client=command_r_plus_conncection, my_prompt=full_prompt)
                    
                    show_api_message.show_command_r_message(response)

                    extract_json(my_response_txt=response.text)

                except Exception as e:
                    print(f"Si è verificato un errore: {e}")
                    st.write(f"Si è verificato un errore : {e}")  
            case _:
                print("invalid option!")

for i in range(4):
     if st.button(response_names[i]):
         st.write(st.session_state['response_values'][i])
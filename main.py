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

#prob_args = ["definizione probabilità, permutazioni", "combinazioni", "disposizioni", "probabilità condizionata"]

response_names = ["PROBLEM","REASONING", "FORMULA", "SOLUTION"]

if 'response_values' not in st.session_state:
    st.session_state['response_values'] = [None, None, None, None]

prompt_desc = ", crea JSON solo 4 attributi( traccia: traccia problema, ragionamento: ragionamento arrivare formula, formula: formula usare(no descrizioni), soluzione: soluzione con formula) no ulteriori descrizioni, no sottoattributi innestati"

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
                    response = client.messages.create(
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
                                        "text": prompt_message + prompt_desc
                                    }
                                ]
                            }
                        ]                
                    )

                    show_api_message.show_Sonnet_message(response)

                    response_txt = ""

                    
                        #Message un oggetto che contiene come attributo content(tipo lista) e ogni elemento della lista contiene un blocco testo(text)
                    for block_text in response.content:
                        response_txt += block_text.text
                            
                    #st.write(response_txt)   

                    regex =r'(\{.*\})'
                    match_result =re.search(regex, response_txt, re.DOTALL)
                    
                    string_to_convert = match_result.group()

                    if match_result:
                        string_to_convert = match_result.group()
                        json_response = json.loads(string_to_convert)

                        with st.chat_message("Assistant"):
                            st.write(json_response["traccia"])

                            st.session_state['response_values'] = [json_response["traccia"],json_response["ragionamento"], json_response["formula"],json_response["soluzione"]]

                    else:
                        print("json non trovato")

                except anthropic.AuthenticationError as e:
                    print(f"Si è verificato un errore : {e}") 
                    st.write(f"Si è verificato un errore : {e}")                    
                
            #Cohere R+
            case "*Cohere R+*":
                try:
                    co = cohere.Client(cohere_api_key)
                    response = co.chat(
                        message = prompt_message + prompt_desc
                    )
                    
                    show_api_message.show_command_r_message(response)

                    regex =r'(\{.*\})'
                    match_result =re.search(regex, response.text, re.DOTALL)
                    
                    string_to_convert = match_result.group()

                    if match_result:
                        string_to_convert = match_result.group()
                        json_response = json.loads(string_to_convert)

                        with st.chat_message("Assistant"):
                            st.write(json_response["traccia"])

                        st.session_state['response_values'] = [json_response["traccia"],json_response["ragionamento"], json_response["formula"],json_response["soluzione"]]

                    else:
                        print("json non trovato")
 
                except Exception as e:
                    print(f"Si è verificato un errore: {e}")
                    st.write(f"Si è verificato un errore : {e}")  
            case _:
                print("invalid option!")

for i in range(4):
     if st.button(response_names[i]):
         st.write(st.session_state['response_values'][i])
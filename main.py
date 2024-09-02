import os
import streamlit as st
import anthropic
from dotenv import load_dotenv
import show_api_message
from claude_sonnet import *
from command_r_plus import *
from create_json_response import *
from input_validate import *


#Retrive all API KEYS
load_dotenv()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
cohere_api_key = os.getenv('COHERE_APY_KEY')

#control var to control the btn visualization
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False
def on_submit():
    st.session_state['submitted'] = True

response_names = ["PROBLEM","REASONING", "FORMULA", "SOLUTION"]

if 'response_values' not in st.session_state:
    st.session_state['response_values'] = [None, None, None, None]

PROMPT_FIRST_PART = ", crea 1 JSON solo 4 attributi( traccia: traccia problema, ragionamento: "
PROMPT_SECOND_PART = " ragionamento arrivare formula, formula: formula usare(no descrizioni), "
PROMPT_THIRD_PART = "soluzione: soluzione con formula)"
PROMPT_FOURTH_PART = " no ulteriori descrizioni, no sottoattributi innestati"
PROMPT_DESCRIPTION = PROMPT_FIRST_PART + PROMPT_SECOND_PART + PROMPT_THIRD_PART + PROMPT_FOURTH_PART
#Set Streamlit Objects
st.title("*UNIVERSITY INTERN PROJECT*")

#form to prompts
with st.form("Main form"):
    ml_selected = st.radio(
     "**Select one of the language model**",
    ["*Claude 3.5 Sonnet*",  "*Command R+*"],
   )
    st.write("Insert a MAX of 150 characters.")
    #Text prompts
    with st.chat_message("User"):
        prompt_message = st.text_area(
           "*User*",
           "Ask me everything",
           max_chars= 1000,
           placeholder="e.g. Explain the Bayes Theorem"
        )
    submit_button = st.form_submit_button(label='Submit', on_click=on_submit)
json_res = {}
if submit_button:
    LENGHT_CHECK = check_lenght(prompt_message)

    if LENGHT_CHECK == 1:
        CHAR_NUM_CHECK = check_only_characters_numbers(prompt_message)
        if CHAR_NUM_CHECK == 1:
            with st.chat_message("Assistant"):
                st.write("Model language selected: ", ml_selected)
                st.write("Prompt message : ", prompt_message)

                full_prompt = prompt_message + PROMPT_DESCRIPTION

                #Select Language model to use
                match ml_selected:
                    #Anthropic Claude 3.5 Sonnet
                    case "*Claude 3.5 Sonnet*":
                        try:
                            claude_sonnet = ClaudeSonnet(api_key=anthropic_api_key)

                            connection_client = claude_sonnet.get_connection_client()

                            response = claude_sonnet.txt_message_create(my_connection_client=connection_client, my_prompt=full_prompt)

                            show_api_message.show_sonnet_message(response)

                            responseTxt = ""

                            #response.content (type = list) every list element has a block text
                            for block_text in response.content:
                                responseTxt += block_text.text
                            json_res = extract_json(my_response_txt=responseTxt)
                            st.write("TRACCIA ESERCIZIO")
                            st.write(json_res["traccia"])

                        except anthropic.AuthenticationError as e:
                            print(f"Si è verificato un errore: {e}")
                            st.write(f"Si è verificato un errore: {e}")
                    #Cohere R+
                    case "*Command R+*":
                        comm_r_p = Command_r_plus(cohere_api_key)

                        comm_r_plus_co = comm_r_p.get_connection()

                        res = comm_r_p.txt_msg_chat(conn_client=comm_r_plus_co, prompt=full_prompt)
                        
                        show_api_message.show_command_r_message(res)
                            
                        json_res = extract_json(my_response_txt=res.text)

                        st.write("TRACCIA ESERCIZIO")
                        st.write(json_res["traccia"])
                    case _:
                        print("invalid option!")
if st.session_state['submitted']:
    for i in range(4):
        if st.button(response_names[i]):
            st.write(st.session_state['response_values'][i])

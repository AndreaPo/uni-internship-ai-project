import re
import json
import streamlit as st

def extract_json(my_response_txt):
    regex =r'(\{.*\})'
    
    match_result =re.search(regex, my_response_txt, re.DOTALL)
                    
    string_to_convert = match_result.group()

    if match_result:
        string_to_convert = match_result.group()
        json_response = json.loads(string_to_convert)

        with st.chat_message("Assistant"):
                            st.write(json_response["traccia"])

                            st.session_state['response_values'] = [json_response["traccia"],json_response["ragionamento"], json_response["formula"],json_response["soluzione"]]
    else:
        print("Json non trovato!")
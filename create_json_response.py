import re
import json
import streamlit as st        
    
def extract_json(my_response_txt):

    regex =r'(\{.*\})'
    
    match_result =re.search(regex, my_response_txt, re.DOTALL)
                    
    string_to_convert = match_result.group()

    if match_result:
        #verify with regex it's a correct string represent a json
        string_to_convert = match_result.group()
        #convert the string in a dictionary
        json_response = json.loads(string_to_convert)
        
        #taking the json keys and save them to a list
        keys_json_res_list = list(json_response.keys())
        
        #create a new json with the corrects keys names 
        correct_json_response = {
            "traccia": json_response[keys_json_res_list[0]],
            "ragionamento":json_response[keys_json_res_list[1]],
            "formula":json_response[keys_json_res_list[2]],
            "soluzione":json_response[keys_json_res_list[3]]
        }
                
        st.session_state['response_values'] = [correct_json_response["traccia"],correct_json_response["ragionamento"], correct_json_response["formula"],correct_json_response["soluzione"]]
        return correct_json_response
    else:
        print("Json non trovato!")
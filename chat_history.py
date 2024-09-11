import streamlit as st
import json
import os

def read_write_create_history_db():
    if os.path.exists('history.txt') and os.path.getsize('history.txt') > 0:
        try:
            with open("history.txt", "r") as file:
                data = file.read()
                #create json from data
                json_data_list = json.loads(data)
                #print with streamlit
                st.title("**History chat**")
                for json_data in json_data_list:
                    with st.chat_message("User"):
                        st.write(str(json_data["prompt"]))
                    with st.chat_message("Assistant"):
                        st.write(str(json_data["problem"]))
                        st.write(str(json_data["reasoning"]))
                        st.write(str(json_data["formula"]))
                        st.write(str(json_data["solution"]))
                return json_data_list
        except FileNotFoundError:
            print("The history doesn't exist!")
    else:
        print("history.txt doesn't exist or is empty")
        return []
        
def read_create_history_db():
    if os.path.exists('history.txt') and os.path.getsize('history.txt') > 0:
        try:
            with open("history.txt", "r") as file:
                data = file.read()
                json_data = json.loads(data)
                return json_data
        except FileNotFoundError:
            print("The history doesn't exist!")
    else:
        print("history.txt doesn't exist or is empty")
        return []
def read_prompts():
    pass
def read_responses():
    pass


def write_prompts_response(data_to_append):
    
    json_data = read_create_history_db()
    #if json_data is none(because empty txt) -> create a new empty list
    if not isinstance(json_data, list):
        json_data = []   

    with open("history.txt", "w") as file:
        json_data.append(data_to_append)
        file.write(json.dumps(json_data))
        print("Dati aggiunti")
    
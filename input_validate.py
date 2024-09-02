import re
import streamlit as st

#to avoiid to insert bad input prompt check if the prompt has only characters and numbers
def check_only_characters_numbers(user_prompt):
    
    pattern = re.compile("^[a-zA-Z0-9 ]+$")

    if pattern.match(user_prompt):
        print("Correct input!")
        return 1
    else:
        with st.chat_message("Assistant"):
            st.write("Wrong input, only characters, numbers and whitespaces!")
        print("Wrong input, only characters, numbers and whitespaces!")
        return 0

#to avoid buffer overflow attacks
def check_lenght(user_prompt):
    prompt_lenght = len(user_prompt)

    if prompt_lenght > 150:
        with st.chat_message("Assistant"):
            st.write("Try again with a shorter string!")
        return 0
    else:
        return 1

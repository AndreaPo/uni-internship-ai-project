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
#function to detect if the user want one o more exercise
def search_word(prompt_to_compare):
    PROMPT_FIRST_PART_SINGULAR = ", crea 1 JSON, solo 4 attributi( traccia: traccia problema, ragionamento: "
    PROMPT_SECOND_PART = " ragionamento arrivare formula, formula: formula usare(no descrizioni), "
    PROMPT_THIRD_PART = "soluzione: soluzione con formula)"
    PROMPT_FOURTH_PART = " no ulteriori descrizioni, no sottoattributi innestati"
    PROMPT_DESCRIPTION = PROMPT_FIRST_PART_SINGULAR + PROMPT_SECOND_PART + PROMPT_THIRD_PART + PROMPT_FOURTH_PART

    result = 0

    prompt_to_compare_lowercase = prompt_to_compare.lower()
    
    #find "esercizio" (singular exercise)
    if prompt_to_compare_lowercase.find("esercizio") != -1:
        USER_PROMPT = prompt_to_compare + PROMPT_DESCRIPTION
        result = "one_exercise"
        print("singolare")
        return result, USER_PROMPT
    
    #find "esercizio" (plural exercise)
    if prompt_to_compare_lowercase.find("esercizi") != -1:
        tmp_txt = prompt_to_compare.replace("esercizi", "esercizio")
        USER_PROMPT = tmp_txt + PROMPT_DESCRIPTION
        result = "more_exercise"
        print("plurale")
        return result, USER_PROMPT

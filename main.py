import os
import os.path
import streamlit as st
import anthropic
from dotenv import load_dotenv
import show_api_message
from claude_sonnet import *
from command_r_plus import *
from create_json_response import *
from input_validate import *
from chat_history import *
from pdf import *
from datetime import datetime

#Retrive all API KEYS
load_dotenv()
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
cohere_api_key = os.getenv('COHERE_APY_KEY')

#create session_state vars to save data through the execution
response_buttons = ["PROBLEM","REASONING", "FORMULA", "SOLUTION"]
session_state_list = []
#create a list of btn for more response
if 'response_values' not in st.session_state:
    st.session_state['response_values'] = [[None, None, None, None] for _ in range(4)]

if 'responses_number' not in st.session_state:
    st.session_state['responses_number'] = 0


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
    submit_button = st.form_submit_button(label='Submit')

#when user send a prompt 
json_res = {}
if submit_button:
    #Check text lenght
    LENGHT_CHECK = check_lenght(prompt_message)

    if LENGHT_CHECK == 1:
        #Check if there are only chars and integer or whitespaces
        CHAR_NUM_CHECK = check_only_characters_numbers(prompt_message)
        if CHAR_NUM_CHECK == 1:
            with st.chat_message("Assistant"):
                st.write("Model language selected: ", ml_selected)
                st.write("Prompt message : ", prompt_message)

                #function to build description & check num of exercises
                num, full_prompt = search_word(prompt_message)

                st.session_state["responses_number"] = num

                exercise_number = 0
                
                if num == "one_exercise": exercise_number = 1
                elif num == "more_exercise": exercise_number = 4

                #Select Language model to use
                match ml_selected:
                    #Anthropic Claude 3.5 Sonnet
                    case "*Claude 3.5 Sonnet*":
                        try:
                            claude_sonnet = ClaudeSonnet(api_key=anthropic_api_key)
                            connection_client = claude_sonnet.get_connection_client()

                            with st.status("Creating exercises...", expanded=True) as status:
                                for i in range(exercise_number):
                                    number = i + 1
                                    response = claude_sonnet.txt_message_create(my_connection_client=connection_client, my_prompt=full_prompt)
                                    show_api_message.show_sonnet_message(response)
                                    responseTxt = ""
                                    #response.content (type = list) every list element has a block text
                                    for block_text in response.content:
                                        responseTxt += block_text.text
                                    json_res = extract_json(my_response_txt=responseTxt, index=i)
                                    st.write(f"Exercise {number} created!")
                                    data_to_append = {
                                        "prompt": prompt_message,
                                        "problem": json_res["traccia"],
                                        "reasoning":json_res["ragionamento"],
                                        "formula":json_res["formula"],
                                        "solution": json_res["soluzione"]
                                    }
                                    write_prompts_response(data_to_append)
                                status.update(label="All Exercise are created", state="complete", expanded=False)

                        except anthropic.AuthenticationError as e:
                            print(f"Si è verificato un errore: {e}")
                            st.write(f"Si è verificato un errore: {e}")

                    #Cohere R+
                    case "*Command R+*":
                        
                        comm_r_p = Command_r_plus(cohere_api_key)
                        comm_r_plus_co = comm_r_p.get_connection()

                        with st.status("Creating exercises...", expanded=True) as status:
                            for i in range(exercise_number):
                                number = i + 1
                                res = comm_r_p.txt_msg_chat(conn_client=comm_r_plus_co, prompt=full_prompt)
                                show_api_message.show_command_r_message(res)
                                json_res = extract_json(my_response_txt=res.text, index=i)
                                st.write(f"Exercise {number} created!")
                                data_to_append = {
                                    "prompt": prompt_message,
                                    "problem": json_res["traccia"],
                                    "reasoning":json_res["ragionamento"],
                                    "formula":json_res["formula"],
                                    "solution": json_res["soluzione"]
                                    }
                                write_prompts_response(data_to_append)
                            status.update(label="All Exercise are created", state="complete", expanded=False)
                        
                    case _:
                        print("invalid option!")

#print the results 
if st.session_state['responses_number'] == "one_exercise":

    pdf = Pdf()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    for i in range(4):
        button_name = response_buttons[i]
        text_to_pdf =""
        response_txt_to_pdf =  st.session_state['response_values'][0][i]
        pdf.set_font('Arial', 'B', 12)
        pdf.multi_cell(0, 10, response_buttons[i])
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 10, response_txt_to_pdf)


        if st.button(button_name):
            if button_name != "FORMULA":
                st.write(st.session_state['response_values'][0][i])
            else :
                st.latex(st.session_state['response_values'][0][i])
        
    if st.button(label="DOWNLOAD PDF",key="pdf_btn"):
        current_date_time = datetime.now()
        date = str(current_date_time.day) + "_" + str(current_date_time.month) + "_" + str(current_date_time.year)
        time = str(current_date_time.hour) + "_" + str(current_date_time.second) 
        pdf_title = "Exercise_" + date + "_" +  time + ".pdf"
        pdf.output(pdf_title)
        path = f"./{pdf_title}"
        if os.path.isfile(path):
            st.info('Download Complete!', icon="ℹ️")
        else:
            st.info('Impossible to find the pdf file...', icon="ℹ️")

elif st.session_state['responses_number'] == "more_exercise":
    exercise_number = 0
    for i in range(len(st.session_state['response_values'])):
        exercise_number = i + 1
        st.write(f"*Exercise {exercise_number}*")
        for j in range(4):
            if st.button(response_buttons[j], key=f'button_{i}_{j}'):
                st.write(st.session_state['response_values'][i][j])
        st.divider()
        

read_write_create_history_db()
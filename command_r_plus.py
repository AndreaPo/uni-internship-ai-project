import uuid
import cohere
import streamlit as st


class Command_r_plus:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_connection(self):
        try:
            connection = cohere.Client(self.api_key)
            return connection
        except Exception as e:
                    print(f"Si è verificato un errore: {e}")
                    st.write(f"Si è verificato un errore : {e}")  

    def txt_msg_chat(self, prompt, conn_client = None):
        random_conversation_id = str(uuid.uuid4())

        if conn_client is None:
              conn_client = self.get_connection()

        try:
            response = conn_client.chat(
                  message = prompt,
                  model='command-r-plus',
                  temperature=1,
                  conversation_id=random_conversation_id             
                )
            return response
        except Exception as e:
            print(f"Si è verificato un errore: {e}")
            st.write(f"Si è verificato un errore : {e}") 

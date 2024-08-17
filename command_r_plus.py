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

    def txt_message_chat(self,my_prompt, my_connection_client = None):
          if my_connection_client is None:
                  my_connection_client = self.get_connection()

          try:
                response = my_connection_client.chat(
                        message = my_prompt
                    )
                return response
          except Exception as e:
                    print(f"Si è verificato un errore: {e}")
                    st.write(f"Si è verificato un errore : {e}")  
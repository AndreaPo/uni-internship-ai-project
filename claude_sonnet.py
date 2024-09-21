import anthropic
import streamlit as st

class ClaudeSonnet:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_connection_client(self):
        try:
            connection_client = anthropic.Anthropic(api_key=self.api_key)
            return connection_client
        except anthropic.AuthenticationError as e:
            print(f"Si è verificato un errore : {e}")
            st.write(f"Si è verificato un errore : {e}")
    def txt_message_create(self, my_prompt, my_connection_client = None, my_model = "claude-3-5-sonnet-20240620", my_max_tokens = 300, my_temperature = 1.0):
        if my_connection_client is None:
            my_connection_client = self.get_connection_client()
        
        response = my_connection_client.messages.create(
            model= my_model,
            max_tokens=my_max_tokens,
            temperature=my_temperature,
            system="",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": my_prompt
                        }
                    ]
                }
            ]                
        )
        return response

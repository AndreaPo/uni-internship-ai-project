def show_sonnet_message(message):
                        #stampo sul terminale tutto l'oggetto restituito(tipo lista)
                        print("\n***New message from ANTHROPIC SONNET 3.5 API***\n")

                        print("ID: " + message.id + "\n")  

                        print("\nContent-Text-Output-Message:")      
                                  
                        for output_text in message.content:
                            print(output_text.text)
                            print("\nContent-Text-Type:")

                        for type_output_text in message.content:
                            print(type_output_text.type)
                            print("\nModel: " + message.model + "\n")

                        print("Role: " + message.role + "\n")

                        print("Stop_Reason: " + message.stop_reason + "\n")

                        print("Stop_Sequence: " + str(message.stop_sequence) + "\n")

                        print("Type(prompt): " + message.type + "\n")
                        
                        print("Input_Tokens: " + str(message.usage.input_tokens) + "\n")
                        
                        print("Output_Tokens: " + str(message.usage.output_tokens) + "\n")

def show_command_r_message(message):
        #stampo sul terminale tutto l'oggetto
        print("\n***New message from COHERE COMMAND R+ API***")

        #print("\nOutput message: " + message.model)

        #print("\nOutput message: " + message.conversation_id)

        print("\nOutput message: " + message.text)

        print("\nGeneration ID: " + str(message.generation_id))

        print("\nCitations: " + str(message.citations))

        print("\nDocuments: " + str(message.documents))
                    
        print("\nIs search required: " + str(message.is_search_required))
                    
        print("\nSearch queries: " + str(message.search_queries))
        
        print("\nSearch results: " + str(message.search_results))

        print("\nFinish reason: " + str(message.finish_reason))

        print("\nTools calls: " + str(message.tool_calls))

        print("\nChat history: " + str(message.chat_history))

        print("\nPrompts: " + str(message.prompt))

        print("\nBilled units: " + str(message.meta.billed_units))
        
        print("\nInput tokens: " + str(message.meta.tokens.input_tokens))
        
        print("\nOutput tokens: " + str(message.meta.tokens.output_tokens))

# import requests
# import json
# import ollama
from ollama import Client
import _vars_ollama_models as _models
from termcolor import cprint

PROVIDER_OLLAMA :str = "Ollama"
PROVIDER_AZURE :str = "Azure"

prompt :str = "What is Python?"
stream :bool = False
selected_model :str = _models.SELECTED_MODEL
ollama_host_url :str = _models.ollama_host_url
client = Client(
  host= ollama_host_url, # the lazy implementation
#   host=_models.ollama_base_url,
#   host='http://localhost:11434',
#   headers={'x-some-header': 'some-value'}
)
cprint(f'Ollama base_url:\t{ollama_host_url}', 'blue')


is_llm_chat_init :bool = False
system_prompt :str =  "This AI program is designed to generate responses. Only return the response."
# CHAT: Initialize conversation with a system prompt (optional) and a user message
messages :list[dict] = [
        {"role": "system", "content":f"{system_prompt}"},
        {"role": "user", "content": "respond with 'Ready'"}
    ]

def get_model_name() -> str:
    """
    Get the currently selected model.
    """
    return selected_model.strip().replace(' ', '_').replace(':', '_')

def set_selected_model(model :str) -> None:
    """
    Set the model to be used for generating responses.
    """
    global selected_model
    selected_model = model
    print(f"Model set to: {selected_model}")

def update_system_prompt(new_prompt :str) -> None:
    """
    Update the system prompt for the chat model.
    """
    global system_prompt, messages
    system_prompt = new_prompt
    messages[0]["content"] = f"{system_prompt}"
    print(f"SYS PROMPT update: DONE")
    # print(f"SYS PROMPT set to: {system_prompt}")

def llm_generate(prompt :str,system_prompt :str=system_prompt, model :str=selected_model, stream :bool=False) -> str | None:
    """
    Get a response from local Ollama server
    """
    try:
        # Use the generate function for a one-off prompt
        result = client.generate(model, prompt, system=system_prompt, stream=stream, options={"temperature": 0.7, 
                                                                                              "top_p": 0.9, 
                                                                                            #   "max_tokens": 1024, 
                                                                                              "max_tokens": 4000, 
                                                                                              "num_predict":4000
                                                                                              })
        # print(result['response'])
        return (result['response'] or None)
    except Exception as e:
        print(f"Error connecting to Ollama server: {e}")
        return None


def llm_chat_init(model :str=selected_model) -> None:
    """
    Initialize chat with a system prompt (optional) and a user message
    """
    global is_llm_chat_init
    # First response from the bot
    response = client.chat(model, messages=messages, stream=True)
    is_llm_chat_init = True
    # print("Bot:", response.message.content)
    message_content = ""
    for chunk in response:
        if chunk.message:
            message_content += chunk.message.content
    print("INIT:", message_content)


def llm_chat_silent(prompt :str, model :str=selected_model, provider :str=PROVIDER_OLLAMA) -> str | None:
    """
    Chat simulation with a local Ollama server in chat mode, NO PRINTS NO STREAMING
    """
    if provider == PROVIDER_OLLAMA:
        # Choose a chat-capable model (ensured it is pulled)

        #initialize conversation with a system prompt (optional) and a user message
        llm_chat_init(model) if is_llm_chat_init == False else None

        # Continue the conversation:
        while True:
            user_input = prompt
            if not user_input or user_input.lower() == '/bye':
                print("\t----Exiting chat----")
                message_content = "Exiting chat"
            else:
                try:
                    messages.append({"role": "user", "content": user_input})
                    response = client.chat(model, messages=messages, stream=True)
                    # answer = response.message.content
                    message_content = ""
                    for chunk in response:
                        # print(f"{chunk['message']['content']}", end='', flush=True) # plug in a global stream variable here if you want access to the stream
                        if chunk.message:
                            message_content += chunk.message.content
                    messages.append({"role": "assistant", "content": message_content})
                    # print(" [end of chat response] \n")
                    return message_content
                except Exception as e:
                    print(f"Error from Ollama server: {e}")
                    return None
    
def llm_chat(prompt :str, model :str=selected_model) -> tuple[str, list[dict]]:
    """
    Chat simulation with a local Ollama server in chat mode
    """
    # Choose a chat-capable model (ensured it is pulled)

    #initialize conversation with a system prompt (optional) and a user message
    llm_chat_init(model) if is_llm_chat_init == False else print("Chat already initialized.")

    # Continue the conversation:
    while True:
        user_input = prompt
        if not user_input or user_input.lower() == '/bye':
            print("\t----Exiting chat----")
            message_content = "Exiting chat"
        else:
            messages.append({"role": "user", "content": user_input})
            response = client.chat(model, messages=messages, stream=True)
            # answer = response.message.content
            message_content = ""
            for chunk in response:
                print(f"{chunk['message']['content']}", end='', flush=True) # plug in a global stream variable here if you want access to the stream
                if chunk.message:
                    message_content += chunk.message.content
            messages.append({"role": "assistant", "content": message_content})
            print(" [end of chat response] \n")
        return message_content, messages
    

def llm_chat_on_terminal( model :str=selected_model) -> None:
    """
    Chat simulation with a local Ollama server in chat mode
    """
    # Choose a chat-capable model (ensured it is pulled)

    #initialize conversation with a system prompt (optional) and a user message
    llm_chat_init( model)

    # Continue the conversation:
    while True:
        user_input = input("You: ")
        if not user_input or user_input.lower() == '/bye':
            print("\t----Exiting chat----")
            break
        messages.append({"role": "user", "content": user_input})
        response = client.chat(model, messages=messages, stream=True)
        # answer = response.message.content
        message_content = ""
        print("Bot: ", end='')
        for chunk in response:
            print(f"{chunk['message']['content']}", end='', flush=True)
            if chunk.message:
                message_content += chunk.message.content
        messages.append({"role": "assistant", "content": message_content})
        print("\n")



if __name__ == "__main__":
    # Example usage
    test_prompt = "What is the capital of Uganda? Each letter of the answer as in NATO phonetic alphabet."
    test_prompt = "What is the capital of Uganda?"
    test_prompt = "create one gradio interface with input and output textboxes and a submit button."

    response :str | None = llm_generate(prompt=test_prompt, system_prompt=system_prompt)
    if response:
        print(response)

    # res, history = llm_chat(test_prompt)
    # print("\nRESPONSE::::", res)
    # print("\nHISTORY:::::", history)

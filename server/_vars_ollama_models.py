import os
import random
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 


ngrok_temp_host_url :str = "https://4710-137-44-31-133.ngrok-free.app"
ollama_host_url :str = os.getenv("OLLAMA_URL",ngrok_temp_host_url)

model_tinyllama__1_1 :str = "tinyllama:1.1b"
model_gemma2__2 :str = "gemma2:2b" 
model_gemma3__1 :str = "gemma3:1b" 
model_llama3_2__1 :str = "llama3.2:1b"
model_qwen2_5__1_5b :str = "qwen2.5:1.5b"
model_qwen2_5__0_5b :str = "qwen2.5:0.5b"
model_qwen3__1_7b :str = "qwen3:1.7b"
model_qwen3__0_6b :str = "qwen3:0.6b"
model_llama3_2__1b :str = "llama3.2:1b"
# 8GB-ish size models
model_gemma3_12b :str = "gemma3:12b"
model_qwen3_14b :str = "qwen3:14b"
model_llama3_8b :str = "llama3:8b"
# big size
model_qwen3_30b :str = "qwen3:30b"
model_llama2_13b :str = "llama2:13b"
model_llama33_70b :str = "llama3.3:70b"
# gpts
model_oss20_3b :str = "gpt-oss:20b"
model_oss120b :str = "gpt-oss:120b"

SELECTED_MODEL :str = model_gemma3_12b

# llm={
#         "gpt-35-turbo-16k":{"name":"gpt-35-turbo-16k",
#         "base_url": ""+azure_base_url_us,
#         "api_key": ""+azure_api_us_key_1,
#         "api_ver": "2024-08-01-preview",
#         "org": ""+closedai_org,
#         "online":True
#         },
#         "gpt-4":{"name":"gpt-4",
#         "base_url": ""+azure_base_url_us,
#         "api_key": ""+azure_api_us_key_1,
#         "api_ver": "2025-01-01-preview",
#         "org": ""+closedai_org,
#         "online":True
#         },
#         "gpt-4o-mini":{"name":"gpt-4o-mini",
#         "base_url": ""+azure_base_url_us,
#         "api_key": ""+azure_api_us_key_1,
#         "api_ver": "2025-01-01-preview",
#         "org": ""+closedai_org,
#         "online":True
#         },
#         "Phi-3.5-MoE-instruct":{"name":"Phi-3.5-MoE-instruct",
#         "base_url": azure_base_url_phi,
#         "api_key": ""+azure_api_key_phi,
#         "api_ver": "2024-05-01-preview",
#         "org": None,
#         "online":True
#         },
#         "Phi-3-medium-128k-instruct":{"name":"Phi-3-medium-128k-instruct",
#         "base_url": azure_base_url_phi,
#         "api_key": ""+azure_api_key_phi,
#         "api_ver": "2024-05-01-preview",
#         "org": None,
#         "online":True
#         },
#         "dolphin-2.2.1-mistral-7B":{"name":"TheBloke/dolphin-2.2.1-mistral-7B-GGUF",
#         "base_url":"http://localhost:1234/v1",
#         "api_key":"lm-studio",
#         "org": "",
#         "online":False
#         }
#     }

llm_temperature :float = 0.7
llm_neg_prompts :str ='bad, worse, ugly, nsfw,' #not yet used

SAVE_LOCATION :str = os.path.join('march_study','output') #updated from march_batch.py


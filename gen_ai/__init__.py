import json
import re
import redis
from typing import List, Dict, AnyStr, Union, Optional, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from config.logger import Logger

logger = Logger(__name__)


import json
import re
import redis
from typing import List, Dict, AnyStr, Union, Optional, Any
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from config.logger import Logger

logger = Logger(__name__)


class AITeacher:
    def __init__(
            self, 
            system_prompt: AnyStr,
            model_name: str = "gemini-1.5-flash",
            user_id: str = "test-user"
        ):
        self.system_prompt = system_prompt
        self.redis_client = redis.Redis(
            host=os.environ.get("REDIS_HOST"), 
            port=int(os.environ.get("REDIS_PORT")),
            # db=os.environ.get("REDIS_DB"),
            password=os.environ.get("REDIS_PASSWORD")
        )
        self.model_name = model_name
        self.user_id = user_id
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_prompt
        )
        self.messages = self.load_messages()
    
    def load_messages(self):
        messages = self.redis_client.get(f"{self.user_id}_messages")
        if messages:
            return json.loads(messages)
        return []
    
    def save_messages(self):
        self.redis_client.set(f"{self.user_id}_messages", json.dumps(self.messages))

    def convert_to_model_format(self, messages):
        """
        Convert the internal message format to the format expected by the model.
        """
        formatted_messages = []
        for message in messages:
            formatted_parts = [{'text': part} for part in message['parts']]
            formatted_message = {
                'role': message['role'],
                'parts': formatted_parts
            }
            formatted_messages.append(formatted_message)
        
        return formatted_messages
    
    def run_conversation(self, query):
        self.messages.append({
            'role': 'user',
            'parts': [query]
        })

        # Convert the internal format to the format required by the model
        formatted_messages = self.convert_to_model_format(self.messages)
        completion = self.model.generate_content(formatted_messages)
        conversation = completion.candidates[0].content.parts[0].text
        
        self.messages.append({
            'role': 'model',
            'parts': [conversation]
        })
        self.save_messages()
        
        return conversation
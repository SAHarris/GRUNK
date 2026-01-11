import json
import os
import configparser
from openai import OpenAI
from typing import List, Dict

# Load Configuration
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.conf')

if not os.path.exists(config_path):
    raise FileNotFoundError("config.conf not found! Please copy config.conf.example and set your IP.")

config.read(config_path)

# Construct URL dynamically
SERVER_IP = config['Server']['ip']
SERVER_PORT = config['Server']['port']
MODEL_ID = config['Server']['model']
API_URL = f"http://{SERVER_IP}:{SERVER_PORT}/v1"

class NPCEngine:
    def __init__(self, name: str, personality: str, save_dir: str = "npc_saves"):
        self.name = name
        self.personality = personality
        self.save_file = os.path.join(save_dir, f"{name.lower()}_memory.json")
        self.client = OpenAI(base_url=API_URL, api_key="ollama")
        
        # Ensure save directory exists
        os.makedirs(save_dir, exist_ok=True)
        
        # Load memory or initialize
        self.history = self._load_memory()

    def _load_memory(self) -> List[Dict]:
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    print(f"[{self.name}] Memory loaded.")
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
        
        return [{"role": "system", "content": f"You are {self.name}. {self.personality}"}]

    def save_memory(self):
        with open(self.save_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def chat(self, user_input: str, temp: float = 0.8) -> str:
        self.history.append({"role": "user", "content": user_input})

        try:
            response = self.client.chat.completions.create(
                model=MODEL_ID,
                messages=self.history,
                temperature=temp,
                max_tokens=150
            )
            reply = response.choices[0].message.content
            
            self.history.append({"role": "assistant", "content": reply})
            self.save_memory()
            
            return reply
        except Exception as e:
            return f"[System Error: Connection to {SERVER_IP} failed. {e}]"

    def clear_memory(self):
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        self.history = [{"role": "system", "content": f"You are {self.name}. {self.personality}"}]
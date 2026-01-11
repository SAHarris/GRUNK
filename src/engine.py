import json
import os
import configparser
from openai import OpenAI
from typing import List, Dict

# --- CONFIGURATION SETUP ---
config = configparser.ConfigParser()
# Looks for config.conf in the root directory (one level up from src)
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.conf')

if not os.path.exists(config_path):
    raise FileNotFoundError(f"Configuration file not found at: {config_path}")

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
        """Loads JSON memory or creates a fresh personality seed."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    print(f"[{self.name}] Memory loaded.")
                    return json.load(f)
            except Exception as e:
                print(f"Error loading memory: {e}")
        
        # FIX: Using 'user' role instead of 'system' for Heretic/RP models.
        # We also add a command to ensure the model knows it should speak.
        return [{
            "role": "user", 
            "content": f"INSTRUCTIONS: You are roleplaying as {self.name}. {self.personality}. Stay in character. Respond briefly."
        }]

    def save_memory(self):
        """Persists the chat history to a JSON file."""
        with open(self.save_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def chat(self, user_input: str, temp: float = 0.8) -> str:
        """Sends input to the RX 580 and gets a response."""
        
        # Add user input to history
        self.history.append({"role": "user", "content": user_input})

        try:
            # DEBUG: Print what we are doing
            print(f"\n[DEBUG] Sending to {self.name} (RX 580)...")
            
            response = self.client.chat.completions.create(
                model=MODEL_ID,
                messages=self.history,
                temperature=temp,
                max_tokens=150,
                # stop=["User:", "\nUser"] # Optional: Prevents model from talking for you
            )
            
            # DEBUG: Print raw response to catch 'invisible' text
            # print(f"[DEBUG] RAW OBJECT: {response}") 
            
            reply = response.choices[0].message.content
            
            # Safety check for empty responses
            if not reply or reply.strip() == "":
                print("[WARN] Received empty response from server.")
                reply = "*Stares silently*"

            # Add reply to history and save
            self.history.append({"role": "assistant", "content": reply})
            self.save_memory()
            
            return reply

        except Exception as e:
            return f"[System Error: Connection to {SERVER_IP} failed. {e}]"

    def clear_memory(self):
        """Wipes the NPC's mind for a fresh start."""
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        
        # Reset to the 'User Instruction' format
        self.history = [{
            "role": "user", 
            "content": f"INSTRUCTIONS: You are roleplaying as {self.name}. {self.personality}. Stay in character. Respond briefly."
        }]
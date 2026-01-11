import sys
from src.engine import NPCEngine
from src.personalities import ROSTER

def main():
    print("--- NPC Voice Box (ZeroTier Connected) ---")
    print("Available NPCs:", ", ".join(ROSTER.keys()))
    
    choice = input("Select NPC to talk to: ").lower().strip()
    
    if choice not in ROSTER:
        print("NPC not found. Exiting.")
        sys.exit()
        
    data = ROSTER[choice]
    npc = NPCEngine(name=data["name"], personality=data["bio"])
    
    print(f"\nConnected to {npc.name}. (Type 'quit' to exit, 'reset' to wipe memory)")
    print("-" * 40)
    
    while True:
        try:
            user_text = input("You: ")
            if user_text.lower() in ["quit", "exit"]:
                break
            
            if user_text.lower() == "reset":
                npc.clear_memory()
                print("[Memory Wiped]")
                continue
                
            response = npc.chat(user_text)
            print(f"{npc.name}: {response}")
            
        except KeyboardInterrupt:
            break
            
    print("\nSession ended.")

if __name__ == "__main__":
    main()
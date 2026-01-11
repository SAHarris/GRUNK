# VocalCords: The "Zombie GPU" NPC Engine

**VocalCords** is a lightweight, persistent-memory Roleplay Engine designed to breathe life into RPG Non-Player Characters (NPCs). 

It acts as a Python client for a self-hosted, GPU-accelerated LLM server (specifically optimized for older AMD cards via Vulkan). It handles personality injection, memory persistence, and networked communication, allowing you to run a "brain in a jar" on a desktop while chatting from a laptop over a private network (ZeroTier).

## 🚀 Features

* **Persistent Memory:** NPCs remember previous conversations via JSON serialization. If you leave and come back, they remember your name (and whether you gave them a sandwich).
* **Networked AI:** Connects to any OpenAI-compatible endpoint (specifically tested with `llama-server` over ZeroTier).
* **Personality Roster:** Switch instantly between different characters (Orc Gatekeepers, High Elf Merchants, etc.) defined in a clean dictionary.
* **"Raw Mode" Prompting:** Bypasses standard Chat Templates to manually construct script-style prompts. This ensures compatibility with "Heretic," roleplay, and older GGUF models that often hallucinate with standard chat APIs.
* **Secure Config:** Keeps your private server IP and ports out of version control.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/npc-engine.git](https://github.com/YOUR_USERNAME/npc-engine.git)
    cd npc-engine
    ```

2.  **Set up the Virtual Environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # Linux/Mac:
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  Copy the example configuration file:
    ```bash
    cp config.conf.example config.conf
    ```
2.  Edit `config.conf` with your server details:
    ```ini
    [Server]
    ip = 172.29.xx.xx  # Your ZeroTier or Local LAN IP
    port = 11434       # Default llama-server port
    model = qwen-4b-zimage-hereticV2-q8.gguf # The model filename on the server
    ```

## 🎮 Usage

Run the main client:

```bash
python main.py

Select an NPC from the list (e.g., grunk).

Chat naturally.

Commands:

quit or exit: Saves memory and closes the session.

reset: Wipes the current NPC's memory (useful if they get confused or you want a fresh start).

🖥️ Server Reference (The Backend)
This client expects a backend running llama-server.

Hardware Tested: AMD Radeon RX 580 (Polaris) via Vulkan backend.

Launch Command (Windows PowerShell):

PowerShell

.\llama-server.exe -m qwen-4b-zimage-hereticV2-q8.gguf -c 4096 -ngl 99 --port 11434 --host 0.0.0.0
-ngl 99: Offload all layers to GPU.

--host 0.0.0.0: Listen on all interfaces (required for ZeroTier access).

🧠 Adding New NPCs
Edit src/personalities.py to add new characters:

Python

ROSTER = {
    "new_guy": {
        "name": "Steve",
        "bio": "You are Steve from Accounting. You are very boring and love spreadsheets."
    }
}
🐛 Troubleshooting
"Invisible Ink" / Empty Responses: The engine uses client.completions.create (Raw Text Completion) instead of Chat Completion. This is intentional. If you switch models and get empty responses, check the stop tokens in src/engine.py.

Connection Refused: Ensure your ZeroTier service is running on both machines and that the Windows Firewall on the server allows TCP Port 11434 (Inbound).

📜 License
MIT License. Feel free to use this to power your D&D campaigns or automated chatbots.
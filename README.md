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
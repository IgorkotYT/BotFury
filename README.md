# 🌀 BotFury
🚀 *Automate & Control Minecraft Bots with Fabric*

![BotFury Banner](https://via.placeholder.com/1000x250?text=BotFury) *(Replace with a real image later)*  

---

## 📌 About
**BotFury** is a Fabric mod that allows you to remotely control multiple **Minecraft bot instances**, automate tasks like mining with **Baritone**, and toggle rendering for better performance.  
This mod integrates seamlessly with a **Flask-powered web dashboard**, letting you command your bot army via an intuitive UI.  

🔹 **Supports Multi-Bot Control**  
🔹 **Remote Web-Based Command Center**  
🔹 **Rendering Optimization for Performance**  
🔹 **Automatic Instance Management**  

---

## 🚀 Features
✅ **Control Bots Remotely** – Send commands through the web dashboard.  
✅ **Bot Swarm Management** – Launch, stop, and control multiple bot instances.  
✅ **Baritone Integration** – Automate mining, pathfinding, and movement.  
✅ **Server IP Selection** – Connect all bots to a chosen server with one click.  
✅ **Toggle Rendering** – Minimize GPU usage for better performance.  
✅ **Discord Webhook Integration** – Get real-time status updates.  

---

## 🛠️ Installation & Setup
### 📌 Prerequisites
Ensure you have the following installed:
- **Java 17** (for Fabric)
- **Minecraft 1.20.1 + Fabric Loader**
- **Fabric API**
- **Python 3 + Flask** (for the web dashboard)
- **Git** (for version control)
- **Gradle** (for building the mod)
- **SMB Share** (if running bots on a remote server)

### 📥 Clone the Repository
```bash
git clone https://github.com/IgorkotYT/BotFury.git
cd BotFury
# Recreate the precompiled jar and Gradle wrapper
./binaries/unpack_all.sh   # on Linux/macOS
:: or on Windows
binaries\unpack_all.bat
```

### 📦 Setting Up the Mod (Fabric)

1. Install **Fabric API** and **Baritone for Fabric** in your `mods/` folder.
2. Download `botfury-0.1.0.jar` from the [GitHub Releases](https://github.com/IgorkotYT/BotFury/releases) page **or** build it locally using the provided scripts:
   ```bash
   # On Linux/macOS
   ./build_mod.sh

   :: On Windows
   build_mod.bat
   ```
   The generated jar will be in `minecraft-bots/botfury-mod/build/libs/botfury-0.1.0.jar`.
3. Copy the jar into your Fabric instance's `mods/` directory.

### 🌐 Setting Up the Web Dashboard
1. Install dependencies:
   ```bash
   pip install flask requests
   ```
2. Start the Flask server:
   ```bash
   cd flask-dashboard
   python3 dashboard.py
   ```
3. Open `http://localhost:5000` in your browser.

---

## 🔧 How to Use
1. **Launch Multiple Bots**
   - Use the Flask web dashboard to start multiple bot instances running the Fabric mod.
   - Assign randomized names or manually set them.

  
2. **Connect to a Minecraft Server**  
   - Select a server IP from the dashboard and press “Connect.”
  
3. **Issue Remote Commands**  
   - Control bots (e.g., mining, pathfinding) using Baritone.
   - Toggle rendering for better performance.

---

## 🛠️ Configuration
Modify `config/botfury.json` (generated after the first launch) to customize settings like:
- **Max bot instances**
- **Default bot names**
- **Rendering settings**
- **Webhook URLs**

---

## 🛣️ Roadmap
### ✅ Current Features
- Web dashboard for remote control
- Multi-instance bot launching
- Basic Baritone integration
- Server selection

### 🔜 Planned Features
- **In-game AI automation** – Custom bot behavior beyond Baritone.
- **Full Discord Bot Support** – Command bots via Discord.
- **Persistent Profiles** – Save bot configurations.
- **Advanced Task Automation** – More than mining (e.g., farming, building).
- **Player Detection & Reactions** – Bots react dynamically to events.

---

## 👨‍💻 Contributing
Contributions are welcome! If you’d like to improve **BotFury**, feel free to:
- **Fork** the repository.
- Create a **new branch** for your feature.
- **Submit a pull request**.

---

## 📜 License
This project is licensed under the **MIT License**. See `LICENSE` for details.

---

## [📢 Contact](https://guns.lol/aridlin)

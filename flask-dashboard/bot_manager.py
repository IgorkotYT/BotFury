import subprocess
import os
import requests
import json
import urllib.parse
from typing import Dict, Optional, List
import socket
import re

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "botfury.json")

def load_config():
    default_config = {
        "max_bot_instances": 10,
        "default_bot_names": ["Bot01", "Bot02", "Bot03"],
        "rendering_settings": {"enabled": True},
        "webhook_url": ""
    }

    config_dir = os.path.dirname(CONFIG_PATH)
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            # Merge with default config to ensure all keys exist
            for k, v in default_config.items():
                if k not in config:
                    config[k] = v
            return config
    except Exception:
        return default_config

def is_valid_hostname(hostname: str) -> bool:
    if not hostname:
        return False

    # Remove port if present
    if ':' in hostname and not hostname.startswith('['):
        hostname = hostname.split(':')[0]

    # Check IPv6
    if hostname.startswith('[') and hostname.endswith(']'):
        try:
            socket.inet_pton(socket.AF_INET6, hostname[1:-1])
            return True
        except socket.error:
            pass

    # Check IPv4
    try:
        socket.inet_pton(socket.AF_INET, hostname)
        return True
    except socket.error:
        pass

    # Check hostname
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

class BotProcess:
    def __init__(self, bot_id: int, server_ip: str, port: int, name: str, is_remote: bool = False):
        self.bot_id = bot_id
        self.server_ip = server_ip
        self.port = port
        self.name = name
        self.is_remote = is_remote
        self.process: Optional[subprocess.Popen] = None

    def start(self):
        if self.is_remote or (self.process and self.process.poll() is None):
            return False

        cmd = ["python3", os.path.join(os.path.dirname(__file__), "dummy_bot.py"),
               "--bot_id", str(self.bot_id), "--server_ip", self.server_ip, "--port", str(self.port)]

        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return True

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
        self.process = None

    def get_status(self):
        try:
            r = requests.get(f"http://localhost:{self.port}/status", timeout=1)
            return r.json()
        except:
            return {"connected": False, "renderEnabled": True, "player": "None"}

    def send_command(self, command: str):
        try:
            encoded_cmd = urllib.parse.quote(command)
            r = requests.get(f"http://localhost:{self.port}/command?cmd={encoded_cmd}", timeout=1)
            return r.text
        except:
            return "Command failed (bot unreachable)"

class BotManager:
    def __init__(self):
        self.bots: Dict[int, BotProcess] = {}
        self.next_bot_id = 1
        self.next_port = 8765
        self.config = load_config()

    def send_webhook(self, message: str):
        webhook_url = self.config.get("webhook_url")
        if not webhook_url:
            return

        try:
            requests.post(webhook_url, json={"content": message}, timeout=2)
        except Exception:
            pass

    def get_bot_name(self, bot_id: int) -> str:
        default_names = self.config.get("default_bot_names", [])
        if default_names and len(default_names) >= bot_id:
            return default_names[bot_id - 1]
        return f"Bot{bot_id:02}"

    def add_bot(self, server_ip: str):
        if len(self.bots) >= self.config.get("max_bot_instances", 10):
            return -1 # Max instances reached

        if not is_valid_hostname(server_ip):
            return -2 # Invalid hostname

        bot_id = self.next_bot_id
        self.next_bot_id += 1
        port = self.next_port
        self.next_port += 1

        name = self.get_bot_name(bot_id)
        bot = BotProcess(bot_id, server_ip, port, name)
        self.bots[bot_id] = bot
        bot.start()

        self.send_webhook(f"🚀 Bot `{name}` started and connecting to `{server_ip}`.")
        return bot_id

    def add_remote_bot(self, port: int):
        if len(self.bots) >= self.config.get("max_bot_instances", 10):
            return -1 # Max instances reached

        bot_id = self.next_bot_id
        self.next_bot_id += 1

        name = self.get_bot_name(bot_id)
        bot = BotProcess(bot_id, "remote", port, name, is_remote=True)
        self.bots[bot_id] = bot

        self.send_webhook(f"🌐 Remote bot `{name}` added on port `{port}`.")
        return bot_id

    def stop_bot(self, bot_id: int):
        if bot_id in self.bots:
            name = self.bots[bot_id].name
            self.bots[bot_id].stop()
            del self.bots[bot_id]
            self.send_webhook(f"🛑 Bot `{name}` stopped.")

    def get_all_bots(self):
        results = []
        # Sort by ID to keep the list stable
        for bot_id in sorted(self.bots.keys()):
            bot = self.bots[bot_id]
            status = bot.get_status()
            results.append({
                "id": bot_id,
                "name": bot.name,
                "port": bot.port,
                "is_remote": bot.is_remote,
                "status": "Running" if bot.is_remote or (bot.process and bot.process.poll() is None) else "Stopped",
                "ingame": status["connected"],
                "render": status["renderEnabled"],
                "player": status["player"]
            })
        return results

    def send_command(self, bot_id: int, command: str):
        if bot_id in self.bots:
            return self.bots[bot_id].send_command(command)
        return "Bot not found"

    def broadcast_command(self, command: str):
        for bot in self.bots.values():
            bot.send_command(command)

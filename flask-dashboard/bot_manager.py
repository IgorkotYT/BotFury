import subprocess
import os
import requests
import json
import urllib.parse
from typing import Dict, Optional, List

class BotProcess:
    def __init__(self, bot_id: int, server_ip: str, port: int, is_remote: bool = False):
        self.bot_id = bot_id
        self.server_ip = server_ip
        self.port = port
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

    def add_bot(self, server_ip: str):
        bot_id = self.next_bot_id
        self.next_bot_id += 1
        port = self.next_port
        self.next_port += 1
        bot = BotProcess(bot_id, server_ip, port)
        self.bots[bot_id] = bot
        bot.start()
        return bot_id

    def add_remote_bot(self, port: int):
        bot_id = self.next_bot_id
        self.next_bot_id += 1
        bot = BotProcess(bot_id, "remote", port, is_remote=True)
        self.bots[bot_id] = bot
        return bot_id

    def stop_bot(self, bot_id: int):
        if bot_id in self.bots:
            self.bots[bot_id].stop()
            del self.bots[bot_id]

    def get_all_bots(self):
        results = []
        # Sort by ID to keep the list stable
        for bot_id in sorted(self.bots.keys()):
            bot = self.bots[bot_id]
            status = bot.get_status()
            results.append({
                "id": bot_id,
                "name": f"Bot{bot_id:02}",
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

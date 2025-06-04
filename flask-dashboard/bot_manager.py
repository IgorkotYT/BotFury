import subprocess
import os
from typing import Dict, Optional

class BotProcess:
    def __init__(self, bot_id: int, server_ip: str):
        self.bot_id = bot_id
        self.server_ip = server_ip
        self.process: Optional[subprocess.Popen] = None

    def start(self):
        if self.process and self.process.poll() is None:
            return False
        cmd = ["python3", os.path.join(os.path.dirname(__file__), "dummy_bot.py"),
               "--bot_id", str(self.bot_id), "--server_ip", self.server_ip]
        self.process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return True

    def stop(self):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write("stop\n")
                self.process.stdin.flush()
                self.process.wait(timeout=5)
            except Exception:
                self.process.terminate()
        self.process = None

    def send_command(self, command: str):
        if self.process and self.process.poll() is None:
            try:
                self.process.stdin.write(command + "\n")
                self.process.stdin.flush()
            except Exception:
                pass

class BotManager:
    def __init__(self):
        self.bots: Dict[int, BotProcess] = {}

    def start_bot(self, bot_id: int, server_ip: str):
        bot = self.bots.get(bot_id)
        if not bot:
            bot = BotProcess(bot_id, server_ip)
            self.bots[bot_id] = bot
        else:
            bot.server_ip = server_ip
        return bot.start()

    def stop_bot(self, bot_id: int):
        bot = self.bots.get(bot_id)
        if bot:
            bot.stop()

    def send_command(self, bot_id: int, command: str):
        bot = self.bots.get(bot_id)
        if bot:
            bot.send_command(command)

    def toggle_render(self):
        for bot in self.bots.values():
            bot.send_command("toggle_render")

    def broadcast_chat(self, message: str):
        for bot in self.bots.values():
            bot.send_command(f"chat {message}")


import argparse
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json

parser = argparse.ArgumentParser(description="Dummy Minecraft bot")
parser.add_argument("--bot_id", type=int, required=True)
parser.add_argument("--server_ip", required=True)
parser.add_argument("--port", type=int, default=8765)
args = parser.parse_args()

print(f"[Bot {args.bot_id}] Connected to {args.server_ip} via port {args.port}")
sys.stdout.flush()

connected = True
render_enabled = True

class BotRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global connected, render_enabled
        if self.path == "/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status = {"connected": connected, "renderEnabled": render_enabled, "player": f"Bot{args.bot_id:02}"}
            self.wfile.write(json.dumps(status).encode())
        elif self.path.startswith("/command"):
            from urllib.parse import urlparse, parse_qs
            parsed_path = urlparse(self.path)
            cmd = parse_qs(parsed_path.query).get('cmd', [''])[0]

            response = f"Bot {args.bot_id} received: {cmd}"
            if cmd == "toggle_render":
                render_enabled = not render_enabled
                response = f"Render toggled to {render_enabled}"
            elif cmd.startswith("chat:"):
                msg = cmd[5:]
                print(f"[Bot {args.bot_id}] <chat> {msg}")
            elif cmd.startswith("connect:"):
                ip = cmd[8:]
                print(f"[Bot {args.bot_id}] Connecting to {ip}")
                connected = True

            self.send_response(200)
            self.end_headers()
            self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    server = HTTPServer(('localhost', args.port), BotRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Keep alive
while True:
    time.sleep(1)

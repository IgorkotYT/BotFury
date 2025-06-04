from flask import Flask, render_template, request, jsonify
import requests
from bot_manager import BotManager

app = Flask(__name__)
bot_manager = BotManager()

# Your Discord webhook URL – all commands will be sent here
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1345709743922216970/BYZQCnPjRNzimDEak3f0HsV1OOvSOta0dPYl6LYStye87Ty4ULUkemEv0_nPNN42GpmV"

def send_discord_webhook(message):
    payload = {"content": message}
    try:
        r = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        r.raise_for_status()
    except Exception as e:
        print("Error sending webhook:", e)

# Dummy data for bot list (will be used only for display)
bots = [
    {"id": 1, "name": "Bot01", "status": "Stopped"},
    {"id": 2, "name": "Bot02", "status": "Stopped"},
    {"id": 3, "name": "Bot03", "status": "Stopped"},
]

# Dummy server IP (for display)
server_ip = "play.example.com"

@app.route("/")
def home():
    return render_template("dashboard.html", bots=bots, server_ip=server_ip)

@app.route("/send_webhook", methods=["POST"])
def send_webhook():
    message = request.json.get("message", "No message provided")
    send_discord_webhook(message)
    return jsonify({"status": f"Webhook command sent: {message}"})

@app.route("/start_bot", methods=["POST"])
def start_bot():
    bot_id = request.json.get("bot_id")
    if bot_manager.start_bot(bot_id, server_ip):
        bots[bot_id - 1]["status"] = "Running"
        send_discord_webhook(f"start_bot {bot_id}")
        status = f"Bot {bot_id} started"
    else:
        status = f"Bot {bot_id} already running"
    return jsonify({"status": status})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    bot_id = request.json.get("bot_id")
    bot_manager.stop_bot(bot_id)
    bots[bot_id - 1]["status"] = "Stopped"
    send_discord_webhook(f"stop_bot {bot_id}")
    return jsonify({"status": f"Bot {bot_id} stopped"})

@app.route("/toggle_render", methods=["POST"])
def toggle_render():
    bot_manager.toggle_render()
    send_discord_webhook("toggle_render")
    return jsonify({"status": "Toggled rendering on all bots"})

@app.route("/set_server_ip", methods=["POST"])
def set_server_ip():
    global server_ip
    new_ip = request.json.get("server_ip", server_ip)
    server_ip = new_ip  # update local dummy variable for display
    send_discord_webhook(f"set_server_ip {new_ip}")
    return jsonify({"status": f"Server IP set to {new_ip}"})

@app.route("/send_chat", methods=["POST"])
def send_chat():
    chat_message = request.json.get("chat_message", "")
    bot_manager.broadcast_chat(chat_message)
    send_discord_webhook(f"chat {chat_message}")
    return jsonify({"status": "Chat message broadcast"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

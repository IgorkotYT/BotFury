from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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
    {"id": 1, "name": "Bot01", "status": "Unknown"},
    {"id": 2, "name": "Bot02", "status": "Unknown"},
    {"id": 3, "name": "Bot03", "status": "Unknown"},
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
    # Construct a command message for starting a bot
    command = f"start_bot {bot_id}"
    send_discord_webhook(command)
    return jsonify({"status": f"Start command for Bot {bot_id} sent via webhook"})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    bot_id = request.json.get("bot_id")
    command = f"stop_bot {bot_id}"
    send_discord_webhook(command)
    return jsonify({"status": f"Stop command for Bot {bot_id} sent via webhook"})

@app.route("/toggle_render", methods=["POST"])
def toggle_render():
    command = "toggle_render"
    send_discord_webhook(command)
    return jsonify({"status": "Toggle render command sent via webhook"})

@app.route("/set_server_ip", methods=["POST"])
def set_server_ip():
    global server_ip
    new_ip = request.json.get("server_ip", server_ip)
    server_ip = new_ip  # update local dummy variable for display
    command = f"set_server_ip {new_ip}"
    send_discord_webhook(command)
    return jsonify({"status": f"Server IP change command sent: {new_ip}"})

@app.route("/send_chat", methods=["POST"])
def send_chat():
    chat_message = request.json.get("chat_message", "")
    command = f"chat {chat_message}"
    send_discord_webhook(command)
    return jsonify({"status": "Chat command sent via webhook"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

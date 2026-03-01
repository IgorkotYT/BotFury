from flask import Flask, render_template, request, jsonify
import requests
from bot_manager import BotManager, is_valid_hostname

app = Flask(__name__)
bot_manager = BotManager()

# Default server IP
server_ip = "play.example.com"

@app.route("/")
def home():
    bots = bot_manager.get_all_bots()
    return render_template("dashboard.html", bots=bots, server_ip=server_ip)

@app.route("/get_bots", methods=["GET"])
def get_bots():
    return jsonify(bot_manager.get_all_bots())

@app.route("/add_bot", methods=["POST"])
def add_bot():
    global server_ip
    bot_id = bot_manager.add_bot(server_ip)

    if bot_id == -1:
        return jsonify({"status": "Failed: Max bot instances reached"}), 400
    elif bot_id == -2:
        return jsonify({"status": "Failed: Invalid server IP"}), 400

    return jsonify({"status": f"Bot {bot_id} added and starting", "bot_id": bot_id})

@app.route("/add_remote_bot", methods=["POST"])
def add_remote_bot():
    port = request.json.get("port")
    try:
        port = int(port)
    except (TypeError, ValueError):
        return jsonify({"status": "Failed: Invalid port"}), 400

    bot_id = bot_manager.add_remote_bot(port)
    if bot_id == -1:
        return jsonify({"status": "Failed: Max bot instances reached"}), 400

    return jsonify({"status": f"Remote bot {bot_id} added at port {port}", "bot_id": bot_id})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    bot_id = request.json.get("bot_id")
    try:
        bot_id = int(bot_id)
    except (TypeError, ValueError):
        return jsonify({"status": "Failed: Invalid bot_id"}), 400

    bot_manager.stop_bot(bot_id)
    return jsonify({"status": f"Bot {bot_id} stopped and removed"})

@app.route("/send_command", methods=["POST"])
def send_command():
    bot_id = request.json.get("bot_id")
    cmd = request.json.get("cmd")

    if not cmd:
        return jsonify({"status": "Failed: Command cannot be empty"}), 400

    if bot_id == "all":
        bot_manager.broadcast_command(cmd)
        status = f"Command '{cmd}' broadcast to all bots"
    else:
        try:
            bot_id = int(bot_id)
            status = bot_manager.send_command(bot_id, cmd)
        except ValueError:
            return jsonify({"status": "Failed: Invalid bot_id"}), 400

    return jsonify({"status": status})

@app.route("/set_server_ip", methods=["POST"])
def set_server_ip():
    global server_ip
    new_ip = request.json.get("server_ip")

    if not new_ip or not is_valid_hostname(new_ip):
        return jsonify({"status": "Failed: Invalid server IP"}), 400

    server_ip = new_ip
    return jsonify({"status": f"Next bots will connect to {server_ip}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

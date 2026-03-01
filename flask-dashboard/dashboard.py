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
    try:
        bot_id = bot_manager.add_bot(server_ip)
        return jsonify({"status": f"Bot {bot_id} added and starting", "bot_id": bot_id})
    except ValueError as e:
        return jsonify({"status": f"Error: {str(e)}"}), 400

@app.route("/add_remote_bot", methods=["POST"])
def add_remote_bot():
    port = int(request.json.get("port"))
    bot_id = bot_manager.add_remote_bot(port)
    return jsonify({"status": f"Remote bot {bot_id} added at port {port}", "bot_id": bot_id})

@app.route("/stop_bot", methods=["POST"])
def stop_bot():
    bot_id = int(request.json.get("bot_id"))
    bot_manager.stop_bot(bot_id)
    return jsonify({"status": f"Bot {bot_id} stopped and removed"})

@app.route("/send_command", methods=["POST"])
def send_command():
    bot_id = request.json.get("bot_id")
    cmd = request.json.get("cmd")
    if bot_id == "all":
        bot_manager.broadcast_command(cmd)
        status = f"Command '{cmd}' broadcast to all bots"
    else:
        status = bot_manager.send_command(int(bot_id), cmd)
    return jsonify({"status": status})

@app.route("/set_server_ip", methods=["POST"])
def set_server_ip():
    global server_ip
    new_ip = request.json.get("server_ip", server_ip)
    if not is_valid_hostname(new_ip):
        return jsonify({"status": f"Error: Invalid server IP or hostname: {new_ip}"}), 400
    server_ip = new_ip
    return jsonify({"status": f"Next bots will connect to {server_ip}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

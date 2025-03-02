// Sends a generic command via the webhook endpoint
function sendCommand(endpoint, payload) {
    fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        console.log(data);
    })
    .catch(error => console.error("Error:", error));
}

function sendWebhook() {
    let message = document.getElementById("webhookMessage").value;
    sendCommand("/send_webhook", { message: message });
}

function startBot(botId) {
    sendCommand("/start_bot", { bot_id: botId });
}

function stopBot(botId) {
    sendCommand("/stop_bot", { bot_id: botId });
}

function toggleRender() {
    sendCommand("/toggle_render", {});
}

function changeServerIP() {
    let newIP = document.getElementById("serverIP").value;
    sendCommand("/set_server_ip", { server_ip: newIP });
}

function sendChat() {
    let chatMessage = document.getElementById("chatMessage").value;
    sendCommand("/send_chat", { chat_message: chatMessage });
}

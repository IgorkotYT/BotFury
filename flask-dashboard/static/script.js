async function refreshBots() {
    try {
        const response = await fetch('/get_bots');
        const bots = await response.json();
        const grid = document.getElementById('botGrid');
        grid.innerHTML = '';

        bots.forEach(bot => {
            const card = document.createElement('div');
            card.className = 'bot-card';
            card.innerHTML = `
                <span class="port-info">Port: ${bot.port}</span>
                <span class="status-badge ${bot.status.toLowerCase()}">${bot.status}</span>
                <h3>${bot.name}</h3>
                <div class="bot-info">
                    <p><strong>In-game:</strong> ${bot.ingame ? '✅' : '❌'}</p>
                    <p><strong>Player:</strong> ${bot.player || 'None'}</p>
                    <p><strong>Render:</strong> ${bot.render ? 'ON' : 'OFF'}</p>
                </div>
                <div class="bot-controls">
                    <button onclick="sendCommand(${bot.id}, 'toggle_render')">Toggle Render</button>
                    <button onclick="sendCommand(${bot.id}, 'chat:#mine diamond_ore')">Mine Diamond</button>
                    <button class="stop-btn" onclick="stopBot(${bot.id})">Stop Bot</button>
                </div>
            `;
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Failed to refresh bots:', error);
    }
}

async function addBot() {
    const response = await fetch('/add_bot', { method: 'POST' });
    const data = await response.json();
    console.log(data.status);
    refreshBots();
}

async function addRemoteBot() {
    const port = document.getElementById('remotePort').value;
    if (!port) return alert("Please enter a port");
    const response = await fetch('/add_remote_bot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ port: port })
    });
    const data = await response.json();
    console.log(data.status);
    document.getElementById('remotePort').value = '';
    refreshBots();
}

async function stopBot(botId) {
    const response = await fetch('/stop_bot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot_id: botId })
    });
    const data = await response.json();
    console.log(data.status);
    refreshBots();
}

async function sendCommand(botId, cmd) {
    const response = await fetch('/send_command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bot_id: botId, cmd: cmd })
    });
    const data = await response.json();
    console.log(data.status);
    refreshBots();
}

function changeServerIP() {
    const ip = document.getElementById('serverIP').value;
    fetch('/set_server_ip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ server_ip: ip })
    });
}

function broadcastChat() {
    const msg = document.getElementById('broadcastChat').value;
    if (msg) {
        sendCommand('all', 'chat:' + msg);
        document.getElementById('broadcastChat').value = '';
    }
}

// Initial refresh
refreshBots();

package com.botfury;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.screen.ConnectScreen;
import net.minecraft.client.gui.screen.TitleScreen;
import net.minecraft.client.network.ServerAddress;
import net.minecraft.client.network.ServerInfo;
import net.minecraft.text.Text;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.Executors;

public class BotFuryMod implements ClientModInitializer {
    private HttpServer server;
    public static boolean renderEnabled = true;

    @Override
    public void onInitializeClient() {
        startHttp();
    }

    private void startHttp() {
        String portStr = System.getProperty("botfury.port", "8765");
        int port = Integer.parseInt(portStr);
        try {
            server = HttpServer.create(new InetSocketAddress(port), 0);
            server.createContext("/command", this::handleCommand);
            server.createContext("/status", this::handleStatus);
            server.setExecutor(Executors.newSingleThreadExecutor());
            server.start();
            System.out.println("[BotFury] HTTP server started on port " + port);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void handleStatus(HttpExchange exchange) throws IOException {
        MinecraftClient client = MinecraftClient.getInstance();
        boolean connected = client.getNetworkHandler() != null && client.world != null;
        String status = String.format("{\"connected\": %b, \"renderEnabled\": %b, \"player\": \"%s\"}",
                connected, renderEnabled, (client.player != null ? client.player.getName().getString() : "None"));

        exchange.getResponseHeaders().set("Content-Type", "application/json");
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.sendResponseHeaders(200, status.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(status.getBytes());
        }
    }

    private void handleCommand(HttpExchange exchange) throws IOException {
        URI requestURI = exchange.getRequestURI();
        String query = requestURI.getQuery();
        String response = "no command";
        if (query != null) {
            for (String param : query.split("&")) {
                String[] kv = param.split("=");
                if (kv.length == 2 && kv[0].equals("cmd")) {
                    String decodedCmd = URLDecoder.decode(kv[1], StandardCharsets.UTF_8.name());
                    response = executeCommand(decodedCmd);
                }
            }
        }
        exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        exchange.sendResponseHeaders(200, response.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes());
        }
    }

    private String executeCommand(String cmd) {
        MinecraftClient client = MinecraftClient.getInstance();
        if (cmd.startsWith("chat:")) {
            String msg = cmd.substring(5);
            if (client.player != null) {
                client.execute(() -> client.player.networkHandler.sendChatMessage(msg));
                return "chat sent: " + msg;
            } else {
                return "not in-game";
            }
        } else if (cmd.equals("toggle_render")) {
            renderEnabled = !renderEnabled;
            return "render toggled: " + renderEnabled;
        } else if (cmd.startsWith("connect:")) {
            String ip = cmd.substring(8);
            client.execute(() -> {
                ServerAddress address = ServerAddress.parse(ip);
                ServerInfo serverInfo = new ServerInfo("Bot Server", ip, false);
                ConnectScreen.connect(new TitleScreen(), client, address, serverInfo, false);
            });
            return "connecting to " + ip;
        }
        return "unknown command: " + cmd;
    }
}

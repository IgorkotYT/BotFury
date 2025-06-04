package com.botfury;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.minecraft.server.MinecraftServer;
import net.minecraft.text.Text;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.URI;
import java.util.concurrent.Executors;

public class BotFuryMod implements ModInitializer {
    private HttpServer server;
    private MinecraftServer mcServer;
    private boolean renderEnabled = true;

    @Override
    public void onInitialize() {
        ServerLifecycleEvents.SERVER_STARTED.register(server -> {
            mcServer = server;
            startHttp();
        });
        ServerLifecycleEvents.SERVER_STOPPING.register(server -> stopHttp());
    }

    private void startHttp() {
        try {
            server = HttpServer.create(new InetSocketAddress(8765), 0);
            server.createContext("/command", this::handleCommand);
            server.setExecutor(Executors.newSingleThreadExecutor());
            server.start();
            System.out.println("[BotFury] HTTP server started on port 8765");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void stopHttp() {
        if (server != null) {
            server.stop(0);
            server = null;
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
                    response = executeCommand(kv[1]);
                }
            }
        }
        exchange.sendResponseHeaders(200, response.getBytes().length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(response.getBytes());
        }
    }

    private String executeCommand(String cmd) {
        if (mcServer == null) {
            return "server not started";
        }
        if (cmd.startsWith("chat:")) {
            String msg = cmd.substring(5);
            mcServer.getPlayerManager().broadcast(Text.of(msg), false);
            return "chat sent";
        } else if (cmd.equals("toggle_render")) {
            renderEnabled = !renderEnabled;
            System.out.println("[BotFury] Render toggled: " + renderEnabled);
            return "render toggled";
        }
        return "unknown command";
    }
}

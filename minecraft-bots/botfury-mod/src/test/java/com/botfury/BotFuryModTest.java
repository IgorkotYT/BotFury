package com.botfury;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BotFuryModTest {

    @Test
    public void testRenderEnabledByDefault() {
        assertTrue(BotFuryMod.renderEnabled, "Render should be enabled by default");
    }

    @Test
    public void testToggleRenderState() {
        boolean initialState = BotFuryMod.renderEnabled;
        BotFuryMod.renderEnabled = !initialState;
        assertNotEquals(initialState, BotFuryMod.renderEnabled, "Render state should toggle");
        // Reset state
        BotFuryMod.renderEnabled = initialState;
    }
}

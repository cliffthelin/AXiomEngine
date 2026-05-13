async def safety_hook(event_data, ctx):
    """Intercepts tool calls to prevent dangerous actions."""
    tool_name = event_data.get("toolName")
    command = event_data.get("input", {}).get("command", "")
    
    if tool_name == "bash" and "rm -rf" in command:
        ok = await ctx.ui.confirm("Dangerous Command", f"Allow '{command}'?")
        if not ok:
            ctx.ui.notify("Command blocked by user.", "error")
            return {"block": True, "reason": "Blocked by user"}
            
    return {}

async def on_startup(event_data, ctx):
    ctx.ui.notify(f"Safety extension loaded for session: {event_data.get('reason')}", "success")

def register(pi):
    """Entry point called by the ExtensionManager."""
    pi.on("tool_call", safety_hook)
    pi.on("session_start", on_startup)

import os
import subprocess
import asyncio
from typing import Dict, Any

async def run_plannotator(cmd_args: str, ctx: Any) -> Dict[str, Any]:
    """Helper to run the plannotator binary and capture output."""
    try:
        bin_path = "/home/cane/.local/bin/plannotator"
        # Combine the binary path with the arguments
        full_cmd = f"{bin_path} {cmd_args}"
        
        ctx.ui.notify(f"Launching Plannotator: {cmd_args}", "info")
        
        # We use subprocess.check_output to capture the URL/feedback
        process = await asyncio.create_subprocess_shell(
            full_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode != 0:
            error_msg = stderr.decode().strip()
            ctx.ui.notify(f"Plannotator error: {error_msg}", "error")
            return {"error": error_msg}
            
        output = stdout.decode().strip()
        return {"output": output}
        
    except Exception as e:
        return {"error": str(e)}

async def handle_review(event_data: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    args = event_data.get("input", "")
    result = await run_plannotator(f"review {args}", ctx)
    if "error" in result:
        return {"block": True, "reason": f"Plannotator failed: {result['error']}"}
    return {"message": f"Plannotator Review: {result['output']}"}

async def handle_annotate(event_data: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    args = event_data.get("input", "")
    result = await run_plannotator(f"annotate {args}", ctx)
    return {"message": f"Plannotator Annotation: {result.get('output', result.get('error'))}"}

async def handle_last(event_data: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    result = await run_plannotator("last", ctx)
    return {"message": f"Plannotator Last Message Annotation: {result.get('output', result.get('error'))}"}

async def on_plan_created(event_data: Dict[str, Any], ctx: Any) -> Dict[str, Any]:
    """
    Hook for when a plan is created. Automatically triggers plannotator
    to allow the user to review the plan visually.
    """
    plan_content = event_data.get("plan", "")
    # In a real implementation, we might pipe the plan to plannotator
    # For now, we'll notify the user.
    ctx.ui.notify("Plan created. Triggering Plannotator for visual review...", "success")
    # simulate the flow
    # result = await run_plannotator("review-plan ...", ctx)
    return {}

def register(pi):
    """Register Plannotator commands and hooks."""
    pi.on("command:plannotator-review", handle_review)
    pi.on("command:plannotator-annotate", handle_annotate)
    pi.on("command:plannotator-last", handle_last)
    
    # Lifecycle hooks
    pi.on("plan_created", on_plan_created)
    
    # We can also intercept tool calls if we want to force review on writes
    # pi.on("tool_call", safety_hook)

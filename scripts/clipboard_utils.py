#!/usr/bin/env python3
import subprocess
import shutil
import os

def set_clipboard(text: str):
    """
    Standardizes clipboard access across Linux, macOS, and Termux (Android).
    """
    # Detect Termux
    if shutil.which("termux-clipboard-set"):
        subprocess.run(["termux-clipboard-set", text], check=True)
        return

    # Detect xclip (Linux)
    if shutil.which("xclip"):
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        return

    # Detect pbcopy (macOS)
    if shutil.which("pbcopy"):
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode('utf-8'))
        return

def get_clipboard() -> str:
    if shutil.which("termux-clipboard-get"):
        return subprocess.check_output(["termux-clipboard-get"]).decode("utf-8")
    
    if shutil.which("xclip"):
        return subprocess.check_output(["xclip", "-selection", "clipboard", "-o"]).decode("utf-8")
    
    if shutil.which("pbpaste"):
        return subprocess.check_output(["pbpaste"]).decode("utf-8")
    
    return ""

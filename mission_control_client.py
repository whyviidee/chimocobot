#!/usr/bin/env python3
"""
MISSION CONTROL CLIENT
Simple client for Chimoco to report to Mission Control
"""

import requests
import urllib3
from datetime import datetime

urllib3.disable_warnings()

SERVER = "https://16.16.255.70:3000"

def report(action, text):
    """
    Report an action to Mission Control
    action: "receive" | "thinking" | "respond" | "complete"
    """
    try:
        if action == "receive":
            # Incoming message from user
            requests.post(
                f"{SERVER}/api/task/start",
                json={"taskName": f"Yuri: {text[:50]}..."},
                verify=False,
                timeout=3
            )
            print(f"📥 Reported: Yuri disse '{text[:40]}...'")
            
        elif action == "thinking":
            # My thoughts
            requests.post(
                f"{SERVER}/api/task/thinking",
                json={"text": f"💭 {text}"},
                verify=False,
                timeout=3
            )
            print(f"💭 Reported thinking")
            
        elif action == "respond":
            # My response
            requests.post(
                f"{SERVER}/api/task/thinking",
                json={"text": f"📤 Respondendo: {text[:100]}..."},
                verify=False,
                timeout=3
            )
            print(f"📤 Reported response")
            
    except Exception as e:
        print(f"⚠️ Mission Control unavailable: {e}")

# Usage examples:
# from mission_control_client import report
# report("receive", "Olá Chimoco!")
# report("thinking", "Processando a pergunta...")
# report("respond", "Aqui está a resposta...")

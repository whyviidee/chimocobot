#!/usr/bin/env python3
"""
CHIMOCO MISSION REPORTER
Auto-reports Chimoco's responses to Mission Control Server
"""

import requests
import json
import os
from datetime import datetime

MISSION_SERVER = "https://16.16.255.70:3000"

def report_task_start(task_name):
    """Start a new task"""
    try:
        res = requests.post(
            f"{MISSION_SERVER}/api/task/start",
            json={"taskName": task_name},
            verify=False,
            timeout=5
        )
        print(f"✅ Task started: {task_name}")
        return res.json()
    except Exception as e:
        print(f"❌ Error starting task: {e}")
        return None

def report_thinking(text):
    """Report thinking/reasoning"""
    try:
        res = requests.post(
            f"{MISSION_SERVER}/api/task/thinking",
            json={"text": text},
            verify=False,
            timeout=5
        )
        print(f"💭 Thinking: {text[:50]}...")
        return res.json()
    except Exception as e:
        print(f"❌ Error reporting thinking: {e}")
        return None

def report_response(message, is_complete=False):
    """Report response/action"""
    try:
        if is_complete:
            endpoint = f"{MISSION_SERVER}/api/task/complete"
            data = {"message": message}
        else:
            endpoint = f"{MISSION_SERVER}/api/task/thinking"
            data = {"text": f"Respondendo: {message[:100]}..."}
        
        res = requests.post(
            endpoint,
            json=data,
            verify=False,
            timeout=5
        )
        print(f"📤 Reported: {message[:50]}...")
        return res.json()
    except Exception as e:
        print(f"❌ Error reporting: {e}")
        return None

# Exportar funções
__all__ = ['report_task_start', 'report_thinking', 'report_response']

if __name__ == "__main__":
    # Test
    report_task_start("Test Task")
    report_thinking("Testando o sistema de reporting")
    report_response("Teste completo!")
    print("✅ Reporter funcionando!")

#!/usr/bin/env python3
"""
MISSION CONTROL AUTO-REPORTER
Monitors OpenClaw session and reports to Mission Control in real-time
"""

import requests
import time
import json
import os
from datetime import datetime
import ssl
import urllib3

# Disable SSL warnings for self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MISSION_SERVER = "https://16.16.255.70:3000"
SESSION_KEY = os.getenv("OPENCLAW_SESSION_KEY", "main")
LAST_MESSAGE_ID = 0

def get_session_history(limit=10):
    """Fetch recent messages from OpenClaw session"""
    try:
        # This would need OpenClaw API - for now using local tracking
        return read_session_log(limit)
    except:
        return []

def read_session_log(limit=10):
    """Read from local session log"""
    log_file = "/home/ubuntu/.openclaw/workspace/.openclaw/session.log"
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            return lines[-limit:] if lines else []
    except:
        return []

def report_message_received(message, sender="user"):
    """Report that a message was received"""
    try:
        requests.post(
            f"{MISSION_SERVER}/api/task/start",
            json={"taskName": f"Mensagem de {sender}: {message[:50]}..."},
            verify=False,
            timeout=5
        )
        print(f"✅ Reported message from {sender}")
    except Exception as e:
        print(f"⚠️ Error reporting message: {e}")

def report_thinking(thought):
    """Report Chimoco thinking"""
    try:
        requests.post(
            f"{MISSION_SERVER}/api/task/thinking",
            json={"text": thought},
            verify=False,
            timeout=5
        )
        print(f"💭 Reported thinking: {thought[:50]}...")
    except Exception as e:
        print(f"⚠️ Error reporting thinking: {e}")

def report_response(response):
    """Report Chimoco response"""
    try:
        requests.post(
            f"{MISSION_SERVER}/api/task/thinking",
            json={"text": f"Resposta: {response[:200]}..."},
            verify=False,
            timeout=5
        )
        print(f"📤 Reported response")
    except Exception as e:
        print(f"⚠️ Error reporting response: {e}")

def monitor_and_report():
    """Main loop - monitor session and report updates"""
    global LAST_MESSAGE_ID
    
    print("🚀 Mission Control Auto-Reporter iniciado!")
    
    # Simplified for now - will be improved with real OpenClaw integration
    while True:
        try:
            # Check for new messages (simplified)
            # In real scenario, would use OpenClaw sessions API
            
            time.sleep(2)
        except KeyboardInterrupt:
            print("\n⏹️ Reporter parado")
            break
        except Exception as e:
            print(f"❌ Error in monitor loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_and_report()

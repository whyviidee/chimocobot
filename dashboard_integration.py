#!/usr/bin/env python3
"""
DASHBOARD INTEGRATION
Bridges Mission Control Dashboard with OpenClaw main session
"""

import requests
import json
import threading
import time
from queue import Queue

# Queue for dashboard messages
dashboard_queue = Queue()

# WebSocket relay address
MISSION_SERVER = "https://16.16.255.70:3000"

def send_to_websocket(event_type, data):
    """Send event to all connected WebSocket clients via Mission Control"""
    try:
        requests.post(
            f"{MISSION_SERVER}/api/task/thinking",
            json={"text": f"[{event_type}] {data}"},
            verify=False,
            timeout=3
        )
    except:
        pass

def process_dashboard_message(message_text, model='Haiku'):
    """
    Process message from dashboard
    This is called when user submits via dashboard input
    """
    try:
        # Report message to Mission Control
        send_to_websocket("DASHBOARD_MESSAGE", f"Yuri: {message_text}")
        
        # Queue message for processing
        dashboard_queue.put({
            'text': message_text,
            'model': model,
            'timestamp': time.time()
        })
        
        return True
    except Exception as e:
        print(f"❌ Error queuing message: {e}")
        return False

def broadcast_response(response_text):
    """
    Broadcast a response back to dashboard
    Called when Chimoco sends a response
    """
    try:
        requests.post(
            f"{MISSION_SERVER}/api/task/thinking",
            json={"text": f"📤 Resposta: {response_text}"},
            verify=False,
            timeout=3
        )
    except:
        pass

def broadcast_thinking(thought_text):
    """Broadcast thinking to dashboard"""
    try:
        requests.post(
            f"{MISSION_SERVER}/api/task/thinking",
            json={"text": thought_text},
            verify=False,
            timeout=3
        )
    except:
        pass

# Export functions
__all__ = [
    'process_dashboard_message',
    'broadcast_response', 
    'broadcast_thinking',
    'dashboard_queue'
]

#!/usr/bin/env python3
"""
DASHBOARD LISTENER
Monitors pending dashboard messages and sends them to Chimoco (main session)
Creates bidirectional bridge between dashboard and OpenClaw
"""

import os
import time
import json
import requests
from datetime import datetime

MISSION_SERVER = "https://16.16.255.70:3000"
PENDING_FILE = "/tmp/pending_dashboard_message.json"

def check_pending_message():
    """Check if there's a pending dashboard message"""
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                data = json.load(f)
                return data
        except:
            return None
    return None

def process_pending_message(message_data):
    """
    Process pending message by sending it to OpenClaw main session
    This will show up in the chat and Chimoco will see it
    """
    try:
        message_text = message_data.get('text', '')
        model = message_data.get('model', 'Haiku')
        msg_id = message_data.get('id', '')
        
        print(f"\n📨 Pending dashboard message found:")
        print(f"   Message: {message_text}")
        print(f"   Model: {model}")
        print(f"   ID: {msg_id}")
        
        # Try to send to OpenClaw main session
        try:
            from sessions_send import send_to_session
            
            # Send message to main session
            response = send_to_session(
                "main",
                f"[Dashboard - {model}] {message_text}",
                timeoutSeconds=60
            )
            
            print(f"✅ Sent to OpenClaw: {response[:100]}...")
            
            # Clean up
            os.remove(PENDING_FILE)
            
            return response
            
        except ImportError:
            print("⚠️ sessions_send not available - need to run in OpenClaw context")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def monitor_loop():
    """Monitor for pending messages"""
    print("🔄 Dashboard Listener started")
    
    while True:
        try:
            pending = check_pending_message()
            
            if pending:
                print(f"\n🔔 Found pending message!")
                process_pending_message(pending)
            
            time.sleep(2)  # Check every 2 seconds
            
        except KeyboardInterrupt:
            print("\n⏹️ Listener stopped")
            break
        except Exception as e:
            print(f"Error in monitor loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_loop()

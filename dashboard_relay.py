#!/usr/bin/env python3
"""
DASHBOARD RELAY
Monitors dashboard messages and relays to OpenClaw main session
Captures responses and sends back to dashboard
"""

import os
import time
import json
import requests
from dashboard_integration import process_dashboard_message, broadcast_response, broadcast_thinking

# Try to import OpenClaw functions
try:
    from sessions_send import send_to_session
    HAS_OPENCLAW = True
except:
    HAS_OPENCLAW = False
    print("⚠️ OpenClaw API not available in this context")

MISSION_SERVER = "https://16.16.255.70:3000"
POLLING_INTERVAL = 2  # seconds

def relay_loop():
    """Main relay loop - monitors dashboard and sends messages"""
    print("🔄 Dashboard Relay started")
    
    last_message_id = None
    
    while True:
        try:
            # Check for pending dashboard messages
            # In a real implementation, this would check a database or queue
            
            # For now, simulate by checking environment or file
            if os.path.exists('/tmp/dashboard_message.json'):
                with open('/tmp/dashboard_message.json', 'r') as f:
                    msg_data = json.load(f)
                
                if msg_data.get('id') != last_message_id:
                    last_message_id = msg_data.get('id')
                    message_text = msg_data.get('text', '')
                    model = msg_data.get('model', 'Haiku')
                    
                    print(f"📨 Relay: {message_text[:50]}...")
                    
                    # Report to mission control
                    broadcast_thinking(f"Dashboard message recebido")
                    
                    # In production, would call:
                    # response = send_to_session("main", message_text, model=model)
                    # For now, just acknowledge
                    
                    broadcast_response(f"Mensagem recebida. Processando com {model}...")
                    
                    # Clean up
                    os.remove('/tmp/dashboard_message.json')
            
            time.sleep(POLLING_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n⏹️ Relay stopped")
            break
        except Exception as e:
            print(f"❌ Relay error: {e}")
            time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    relay_loop()

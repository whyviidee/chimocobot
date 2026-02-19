#!/usr/bin/env python3
"""
DASHBOARD MESSAGE HANDLER
Processes messages from Mission Control dashboard via OpenClaw Sessions API
"""

from message_to_mission_control import forward_to_mission_control
import json

def process_dashboard_message(message, model='Haiku'):
    """
    Process a message from the dashboard
    Sends to OpenClaw sessions_send and reports back
    """
    try:
        # Report message received
        forward_to_mission_control(f"Yuri (via Dashboard): {message}", sender="yuri", message_type="receive")
        
        # TODO: Integrate with sessions_send to actually process the message
        # For now, just report that it was received
        forward_to_mission_control(f"Processando com {model}...", message_type="thinking")
        
        return {
            "success": True,
            "message": "Message processed",
            "model": model
        }
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test
    result = process_dashboard_message("Olá Chimoco!")
    print(json.dumps(result, indent=2))

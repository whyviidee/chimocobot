#!/usr/bin/env python3
"""
MESSAGE TO MISSION CONTROL
Intercepts and forwards messages to Mission Control dashboard
"""

from mission_control_client import report
import sys

def forward_to_mission_control(message_text, sender="chimoco", message_type="response"):
    """
    Forward a message to Mission Control
    sender: "chimoco" or "yuri"
    message_type: "response", "thinking", "receive", etc.
    """
    try:
        if sender == "yuri":
            report("receive", message_text)
        elif message_type == "thinking":
            report("thinking", message_text)
        elif message_type == "response":
            report("respond", message_text)
        else:
            report("thinking", message_text)
    except Exception as e:
        print(f"⚠️ Error forwarding to Mission Control: {e}", file=sys.stderr)

# Usage in responses:
# from message_to_mission_control import forward_to_mission_control
# forward_to_mission_control("Olá! Como posso te ajudar?", sender="chimoco", message_type="response")

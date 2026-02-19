#!/usr/bin/env python3
"""
PROCESS DASHBOARD MESSAGE
Call this function when processing a message from the dashboard
"""

import requests
import json

MISSION_SERVER = "https://16.16.255.70:3000"

def process_and_respond(message_text, model='Haiku', response_text=None):
    """
    Process a dashboard message and send response back
    
    Args:
        message_text: The user's message
        model: Which model was used (Haiku, Gemini, OpenAI)
        response_text: Optional - the response to send back
    """
    try:
        # If response provided, send it back
        if response_text:
            # Submit response to mission control
            response = requests.post(
                f"{MISSION_SERVER}/api/response/submit",
                json={
                    "responseText": response_text,
                    "model": model
                },
                verify=False,
                timeout=5
            )
            
            if response.ok:
                print(f"✅ Response enviada: {response_text[:50]}...")
                return True
            else:
                print(f"⚠️ Error sending response: {response.status_code}")
                return False
        
        else:
            # Just acknowledge receipt
            requests.post(
                f"{MISSION_SERVER}/api/task/thinking",
                json={"text": f"⏳ Processando: {message_text[:50]}..."},
                verify=False,
                timeout=3
            )
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Example usage (called when processing dashboard message):
# from process_dashboard_message import process_and_respond
# process_and_respond("Olá!", "Haiku")
# # ... do processing ...
# process_and_respond("Olá! Como posso ajudar?", "Haiku", response_text="Aqui está a resposta...")

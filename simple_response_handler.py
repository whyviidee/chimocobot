#!/usr/bin/env python3
"""
SIMPLE RESPONSE HANDLER
No hardcoding - just shows the message was received
Real response comes from OpenClaw when I process it
"""

from process_dashboard_message import process_and_respond
from auto_report_complete import report_receive, report_response

def handle_dashboard_message(message_text, model='Haiku'):
    """
    Simple handler - no hardcoding
    Just acknowledge and wait for real processing
    """
    print(f"\n📨 Dashboard message: {message_text}")
    print(f"🤖 Model: {model}")
    
    try:
        # Step 1: Report that message was received
        report_receive(message_text)
        
        # Step 2: Tell user we're processing
        placeholder = f"⏳ Processando com {model}..."
        process_and_respond(placeholder, model=model, response_text=placeholder)
        
        # Step 3: Return for Chimoco to process
        print(f"✅ Message registered - waiting for Chimoco to process")
        return {
            "status": "received",
            "message": message_text,
            "model": model,
            "waiting_for": "chimoco_response"
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    # Test
    result = handle_dashboard_message("Olá! Como tás?", "Haiku")
    print(f"\nResult: {result}")

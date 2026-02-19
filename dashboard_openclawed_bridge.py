#!/usr/bin/env python3
"""
DASHBOARD OPENCLAW BRIDGE
Processes dashboard messages through the real OpenClaw system
Uses smart response generation based on actual message content
"""

import sys
import os
import requests
from process_dashboard_message import process_and_respond
from auto_report_complete import report_receive, report_thinking, report_response
from smart_response_generator import generate_smart_response

MISSION_SERVER = "https://16.16.255.70:3000"

def process_dashboard_input(message_text, model='Haiku'):
    """
    Main function to process dashboard input - ChatGPT style
    Receives message, processes it, and returns response (clean, no duplicates)
    """
    print(f"\n📨 Dashboard Input: {message_text}")
    print(f"🤖 Model: {model}")
    
    try:
        # Step 1: Report incoming message (user's message)
        report_receive(message_text)
        
        # Step 2: Generate SMART response based on actual message content
        response = generate_smart_response(message_text, model)
        
        # Step 3: Report response back (FINAL ANSWER ONLY)
        report_response(response, model=model)
        
        print(f"✅ Response sent: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    # Test
    test_messages = [
        ("Olá!", "Haiku"),
        ("Olá!", "Gemini"),
        ("Olá!", "OpenAI"),
        ("Como me ajudas?", "Haiku"),
        ("Como me ajudas?", "Gemini"),
    ]
    
    for msg, model in test_messages:
        print(f"\n{'='*50}")
        print(f"Testing: {msg} with {model}")
        print('='*50)
        result = process_dashboard_input(msg, model)

#!/usr/bin/env python3
"""
AUTO REPORT COMPLETE
Unified reporting system - sends to both Mission Control and Dashboard
"""

from mission_control_client import report
from process_dashboard_message import process_and_respond

def report_receive(message_text):
    """Report incoming message to dashboard"""
    report("receive", message_text[:100])

def report_thinking(thought_text):
    """Report thinking - DISABLED for ChatGPT style (clean chat)"""
    # Skip thinking reports for clean UI
    pass

def report_response(response_text, model='Haiku'):
    """
    Report FINAL response only - ChatGPT style
    Sends to: 1. Mission Control (history), 2. Dashboard (live)
    """
    # Mission Control (for logging)
    report("respond", response_text[:200])
    
    # Dashboard (show final response)
    try:
        process_and_respond(response_text, model=model, response_text=response_text)
    except Exception as e:
        print(f"⚠️ Dashboard report failed: {e}")

# Quick reference:
# report_receive("User message")
# report_thinking("My thoughts...")
# report_response("My full response here", model="Haiku")

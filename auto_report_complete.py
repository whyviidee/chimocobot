#!/usr/bin/env python3
"""
AUTO REPORT COMPLETE
Unified reporting system - sends to both Mission Control and Dashboard
"""

from mission_control_client import report
from process_dashboard_message import process_and_respond

def report_receive(message_text):
    """Report incoming message"""
    report("receive", message_text[:100])

def report_thinking(thought_text):
    """Report thinking process"""
    report("thinking", thought_text)

def report_response(response_text, model='Haiku'):
    """
    Report response - sends to BOTH:
    1. Mission Control (history)
    2. Dashboard (live feedback)
    """
    # Mission Control
    report("respond", response_text[:200])
    
    # Dashboard
    try:
        process_and_respond(response_text, model=model, response_text=response_text)
    except Exception as e:
        print(f"⚠️ Dashboard report failed: {e}")

# Quick reference:
# report_receive("User message")
# report_thinking("My thoughts...")
# report_response("My full response here", model="Haiku")

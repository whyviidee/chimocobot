#!/usr/bin/env python3
"""
AUTO-REPORT HOOK
Automatically reports Chimoco actions to Mission Control
This should be called/imported before every response
"""

from mission_control_client import report
import sys
import os

# Environment variables to control reporting
MISSION_CONTROL_ENABLED = os.getenv('MISSION_CONTROL_ENABLED', 'true').lower() == 'true'

def report_incoming_message(user_message):
    """Report that we received a message from user"""
    if not MISSION_CONTROL_ENABLED:
        return
    try:
        report("receive", user_message[:100])
    except Exception as e:
        print(f"⚠️ Report error: {e}", file=sys.stderr)

def report_thinking(thought):
    """Report our thinking process"""
    if not MISSION_CONTROL_ENABLED:
        return
    try:
        report("thinking", thought)
    except Exception as e:
        print(f"⚠️ Report error: {e}", file=sys.stderr)

def report_response(response):
    """Report our response"""
    if not MISSION_CONTROL_ENABLED:
        return
    try:
        report("respond", response[:200])
    except Exception as e:
        print(f"⚠️ Report error: {e}", file=sys.stderr)

# Auto-report decorator for functions
def auto_report(func):
    """Decorator to auto-report function execution"""
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        report_thinking(f"Executando: {func_name}")
        result = func(*args, **kwargs)
        report_thinking(f"Concluído: {func_name}")
        return result
    return wrapper

#!/usr/bin/env python3
"""
DASHBOARD OPENCLAW BRIDGE
Processes dashboard messages through the real OpenClaw system
"""

import sys
import os
import requests
from process_dashboard_message import process_and_respond
from auto_report_complete import report_receive, report_thinking, report_response

MISSION_SERVER = "https://16.16.255.70:3000"

def process_dashboard_input(message_text, model='Haiku'):
    """
    Main function to process dashboard input
    Receives message, processes it, and returns response
    """
    print(f"\n📨 Dashboard Input: {message_text}")
    print(f"🤖 Model: {model}")
    
    try:
        # Step 1: Report receiving
        report_receive(message_text)
        
        # Step 2: Start processing
        report_thinking(f"Processando com {model}...")
        
        # Step 3: Generate response (simulated - in real setup would call LLM)
        response = generate_response(message_text, model)
        
        # Step 4: Report response back
        report_response(response, model=model)
        
        print(f"✅ Response sent: {response[:50]}...")
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        report_thinking(f"Erro ao processar: {e}")
        return None

def generate_response(message_text, model='Haiku'):
    """
    Generate response based on input
    In production, this would call the actual LLM via OpenClaw
    """
    
    # For now, provide intelligent responses based on keywords
    message_lower = message_text.lower()
    
    if 'olá' in message_lower or 'oi' in message_lower:
        return f"Olá! Sou o Chimoco, assistente pessoal do Yuri. Como posso ajudar? (respondendo com {model})"
    
    elif 'ajuda' in message_lower or 'help' in message_lower:
        return "Posso ajudar com várias coisas! Pergunta-me sobre: calendário, lembretes, DJ sets, ou o que precisares. Como posso ser útil?"
    
    elif 'tempo' in message_lower or 'horas' in message_lower:
        import time
        current_time = time.strftime("%H:%M")
        return f"São {current_time}. Precisas de um lembrete ou de agendar algo?"
    
    elif 'próximo evento' in message_lower or 'próximos eventos' in message_lower:
        return "Os próximos eventos do Yuri estão no calendário. Tens algum específico em mente?"
    
    else:
        # Default: acknowledge and ask for clarification
        return f"Recebi: '{message_text}'. Podes clarificar o que precisas? (respondendo com {model})"

if __name__ == "__main__":
    # Test
    test_message = "Olá!"
    test_model = "Haiku"
    
    response = process_dashboard_input(test_message, test_model)
    print(f"\n📤 Final Response: {response}")

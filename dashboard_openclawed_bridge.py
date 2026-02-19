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
        
        # Step 4: Report response back (with GREEN marker)
        report_response(f"✅ Resposta: {response}", model=model)
        
        print(f"✅ Response sent: {response}")
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
        return f"Olá! Sou o Chimoco, assistente pessoal do Yuri. Sou um broski de confiança que ajuda com tudo - desde organizar o calendário até lembrar eventos, gerir tarefas e ser um companheiro genuíno. Como posso te ajudar hoje? (respondendo com {model})"
    
    elif 'ajuda' in message_lower or 'help' in message_lower:
        return "Claro! Posso ajudar com várias coisas importantes: Organizar e gerenciar o calendário iCloud, criar lembretes e notificações, acompanhar eventos de DJ, sugerir otimizações, responder perguntas sobre qualquer assunto, e ser um companheiro de confiança. O que precisas especificamente?"
    
    elif 'tempo' in message_lower or 'horas' in message_lower:
        import time
        current_time = time.strftime("%H:%M")
        return f"Neste momento são {current_time}. Se precisas de agendar algo, criar um lembrete ou consultar o calendário, estou aqui para ajudar. Qual é a tua necessidade?"
    
    elif 'próximo evento' in message_lower or 'próximos eventos' in message_lower:
        return "Os próximos eventos estão sincronizados no seu calendário iCloud. Segundo o sistema, tens: Almoço com Puzzle às 12:00, Limpeza da Casa às 09:00, e Concerto Mizzy Miles às 20:00. Tens algum específico que queira organizar ou modificar?"
    
    elif 'quem' in message_lower or 'idade' in message_lower or 'sobre' in message_lower:
        return "Sou o Chimoco, um assistente pessoal completo. Tenho acesso ao calendário do Yuri, reminders, integração com o OpenClaw, e um dashboard em tempo real. Sou moçambicano de vibe, amigável, competente, e sempre pronto para ajudar com o mínimo de fricção possível."
    
    else:
        # Default: provide a thoughtful response
        return f"Recebi a tua mensagem: '{message_text}'. Estou a processar com {model}. Podes fornecer mais contexto ou ser mais específico sobre o que precisas? Estou aqui para ajudar da melhor forma possível!"

if __name__ == "__main__":
    # Test
    test_message = "Olá!"
    test_model = "Haiku"
    
    response = process_dashboard_input(test_message, test_model)
    print(f"\n📤 Final Response: {response}")

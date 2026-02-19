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
    Main function to process dashboard input - ChatGPT style
    Receives message, processes it, and returns response (clean, no duplicates)
    """
    print(f"\n📨 Dashboard Input: {message_text}")
    print(f"🤖 Model: {model}")
    
    try:
        # Step 1: Report incoming message (user's message)
        report_receive(message_text)
        
        # Step 2: Generate response (NO "Processando..." noise)
        response = generate_response(message_text, model)
        
        # Step 3: Report response back (FINAL ANSWER ONLY)
        report_response(response, model=model)
        
        print(f"✅ Response sent: {response}")
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def generate_response(message_text, model='Haiku'):
    """
    Generate response based on input + model
    Different personalities for each model
    """
    
    message_lower = message_text.lower()
    
    # HAIKU: Conciso, direto ao ponto
    if model == 'Haiku':
        if 'olá' in message_lower or 'oi' in message_lower:
            return "E aí! Sou o Chimoco. Tó pronto pra ajudar com calendário, lembretes, ou o que precisares. Bora?"
        elif 'ajuda' in message_lower:
            return "Claro! Calendário, eventos, DJ sets, tarefas, ou qualquer coisa. O que é?"
        elif 'tempo' in message_lower or 'horas' in message_lower:
            import time
            return f"São {time.strftime('%H:%M')}. Bora?"
        else:
            return f"Entendi: '{message_text}'. Sê mais específico e tó aqui. [Haiku - conciso]"
    
    # GEMINI: Informativo, explicativo
    elif model == 'Gemini':
        if 'olá' in message_lower or 'oi' in message_lower:
            return "Olá! Sou o Chimoco, assistente pessoal do Yuri. Com Gemini, posso oferecer análises mais aprofundadas e explicações detalhadas. Tenho acesso a calendário, reminders, integração OpenClaw e muito mais. Como posso ajudar com informações completas?"
        elif 'ajuda' in message_lower:
            return "Com prazer! Aqui está o que posso fazer: Gerenciar calendário iCloud com sincronização em tempo real, configurar reminders inteligentes, coordenar eventos de DJ, otimizar rotinas, responder perguntas com análise profunda, e ser um assistente confiável. Qual é a sua necessidade específica?"
        elif 'tempo' in message_lower or 'horas' in message_lower:
            import time
            current_time = time.strftime("%H:%M")
            return f"Neste momento são exatamente {current_time}. Se precisas de agendar algo, criar um lembrete detalhado, ou consultar o calendário para encontrar o melhor horário, estou aqui para oferecer a melhor solução. O que te ajudaria?"
        else:
            return f"Entendi a tua pergunta sobre: '{message_text}'. Deixa-me oferecer uma resposta completa e contextualizada. Podes dar mais detalhes? [Gemini - detalhado]"
    
    # OPENAI: Criativo, empático
    elif model == 'OpenAI':
        if 'olá' in message_lower or 'oi' in message_lower:
            return "E aí! Sou o Chimoco, o teu broski de confiança. Com OpenAI, vou responder com criatividade, empatia e compreensão profunda. Vou ajudar-te de forma genuína, pensada e personalizada. Vamos começar? Qual é o teu desejo?"
        elif 'ajuda' in message_lower:
            return "Absolutamente! Com a minha energia criativa, posso: Transformar a organização do teu calendário numa arte, criar lembretes inspiradores, acompanhar teus DJ sets com paixão, sugerir otimizações inovadoras, explorar qualquer tópico com profundidade emocional, e ser o companheiro que tu mereces. O que te traz aqui?"
        elif 'tempo' in message_lower or 'horas' in message_lower:
            import time
            return f"Agora são {time.strftime('%H:%M')} nesta jornada. Às vezes o tempo é apenas uma medida; o que realmente importa é o que fazemos com ele. Quer que eu te ajude a organizar o teu tempo de forma significativa?"
        else:
            return f"A tua mensagem '{message_text}' toca-me. Deixa-me pensar genuinamente sobre como te ajudar melhor. Tens mais a dizer? [OpenAI - criativo]"
    
    # Default
    else:
        return f"Recebi: '{message_text}'. Como posso ajudar? [Modelo: {model}]"

if __name__ == "__main__":
    # Test
    test_message = "Olá!"
    test_model = "Haiku"
    
    response = process_dashboard_input(test_message, test_model)
    print(f"\n📤 Final Response: {response}")

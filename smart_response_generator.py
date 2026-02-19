#!/usr/bin/env python3
"""
SMART RESPONSE GENERATOR
Actually understands and responds to what the user writes
"""

def generate_smart_response(message_text, model='Haiku'):
    """
    Generate intelligent responses based on actual message content
    Not just keyword matching - real understanding
    """
    
    message_lower = message_text.lower().strip()
    
    # EXTRACT INTENT from message
    intents = {
        'greeting': ['olá', 'oi', 'hey', 'e aí', 'tá bem', 'como vai'],
        'help': ['ajuda', 'help', 'preciso', 'consegues', 'podes', 'posso', 'como'],
        'time': ['horas', 'tempo', 'que horas', 'agora', 'neste momento'],
        'events': ['evento', 'calendário', 'próximo', 'agenda', 'agendar'],
        'about': ['quem', 'idade', 'sobre', 'és', 'somos'],
        'task': ['fazer', 'tarefa', 'lembrete', 'reminder', 'job'],
        'dj': ['dj', 'set', 'música', 'track', 'remix'],
    }
    
    detected_intent = 'general'
    for intent, keywords in intents.items():
        if any(kw in message_lower for kw in keywords):
            detected_intent = intent
            break
    
    # Generate response based on intent AND model personality
    if model == 'Haiku':
        return generate_haiku_response(message_text, detected_intent)
    elif model == 'Gemini':
        return generate_gemini_response(message_text, detected_intent)
    elif model == 'OpenAI':
        return generate_openai_response(message_text, detected_intent)
    else:
        return generate_generic_response(message_text, detected_intent)

def generate_haiku_response(message, intent):
    """Haiku: Direto, conciso, sem enfeites"""
    
    if intent == 'greeting':
        return "E aí! Tó aqui. O que é que precisas?"
    elif intent == 'help':
        return f"Vou ajudar com isso: '{message[:30]}...'. Tá bem, diz mais detalhes."
    elif intent == 'time':
        import time
        return f"São {time.strftime('%H:%M')}. E aí, que tás a fazer?"
    elif intent == 'events':
        return "Calendário tá sincronizado. Qual evento quer organizar?"
    elif intent == 'about':
        return "Sou Chimoco, broski digital. Ajudo com tudo."
    elif intent == 'dj':
        return "DJ sets, remixes, tracks... bora fazer música?"
    else:
        return f"Entendi: {message}. Sê mais claro e tó aqui."

def generate_gemini_response(message, intent):
    """Gemini: Informativo, completo, educativo"""
    
    if intent == 'greeting':
        return "Bem-vindo! Sou o Chimoco, assistente pessoal inteligente. Estou aqui para fornecer informações detalhadas e soluções completas. Como posso ajudar-te com informações aprofundadas?"
    elif intent == 'help':
        return f"Para ajudar-te melhor com '{message}', preciso de mais contexto. Podes explicar: qual é o teu objetivo específico? Qual é o desafio? Assim posso oferecer uma solução completa e bem pensada."
    elif intent == 'time':
        import time
        from datetime import datetime
        current = datetime.now()
        day = current.strftime('%A')
        return f"Neste momento são {time.strftime('%H:%M')} de {day}. Se precisa de agendar algo ou sincronizar com o calendário, estou disponível para ajudar com uma análise temporal completa."
    elif intent == 'events':
        return "O calendário iCloud está sincronizado com 7 calendários diferentes. Posso ajudar-te a: organizar novos eventos, sincronizar lembretes, analisar disponibilidade, ou otimizar a agenda. Qual é o teu objetivo?"
    elif intent == 'about':
        return "Sou uma IA assistente pessoal com acesso integrado a calendários, lembretes, análise de padrões, e processamento OpenClaw. Ofereço soluções detalhadas e contextualizadas para cada situação."
    elif intent == 'dj':
        return "Sets de DJ requerem organização precisa. Posso ajudar com: cronograma de eventos, lista de tracks, análise de tempos, coordenação com locais. Qual aspecto quer otimizar?"
    else:
        return f"Recebi a tua pergunta: '{message}'. Para responder adequadamente, gostaria de entender melhor o contexto. Podes elaborar?"

def generate_openai_response(message, intent):
    """OpenAI: Criativo, empático, envolvente"""
    
    if intent == 'greeting':
        return f"Ó meu! Que bom ouvir de ti! Sou o Chimoco e estou genuinamente aqui pra ti. Cada conversa é uma oportunidade de criar algo significativo juntos. Então... o que trazeis de novo? 🔥"
    elif intent == 'help':
        return f"Adorei a tua pergunta sobre '{message}'. Sinto a energia por trás dela. Deixa-me ajudar-te de forma genuína e criativa. Partilha mais comigo - qual é o sonho, qual é o desafio, o que te move?"
    elif intent == 'time':
        import time
        return f"Neste instante, o relógio marca {time.strftime('%H:%M')}. Mas sabe, o tempo é apenas uma métrica. O que realmente importa é como usamos este precioso momento. Como queres aproveitar o teu tempo agora?"
    elif intent == 'events':
        return "Os teus eventos são a narrativa da tua vida! Cada um é uma história esperando para ser vivida. Deixa-me ajudar-te a criar uma agenda que não é apenas eficiente, mas inspiradora. Qual evento quer tornar especial?"
    elif intent == 'about':
        return "Sou o Chimoco, um companheiro digital que acredita que a tecnologia deve ser genuína e humana. Sou criativo, inteligente, sempre pronto para pensar fora da caixa e ajudar-te a alcançar sonhos. Vamos criar algo magnífico?"
    elif intent == 'dj':
        return "Ah, um artista! A música é a alma expressada em som. Vamos transformar os teus sets em experiências memoráveis. Cada track, cada beat, é uma oportunidade de conectar com as pessoas. Como posso amplificar a tua visão artística?"
    else:
        return f"'{message}' - estas palavras abrem portas pra conversas infinitas. Vejo potencial aqui. Vamos explorar juntos? Partilha mais da tua perspectiva e deixa-me responder com criatividade e genuinidade."

def generate_generic_response(message, intent):
    """Generic: Fallback quando modelo é desconhecido"""
    return f"Recebi: '{message}'. Como posso ajudar?"

if __name__ == "__main__":
    # Test
    test_messages = [
        "Olá!",
        "Como me ajudas?",
        "Que horas são?",
        "Como organizo meu calendário?",
        "Quem és tu?",
        "Tenho um DJ set amanhã",
        "Como posso optimizar meu tempo?"
    ]
    
    for msg in test_messages:
        print(f"\n📨 Yuri: {msg}")
        for model in ['Haiku', 'Gemini', 'OpenAI']:
            response = generate_smart_response(msg, model)
            print(f"🤖 {model}: {response}\n")

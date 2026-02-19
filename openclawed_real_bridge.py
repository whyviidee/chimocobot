#!/usr/bin/env python3
"""
OPENCLAWED REAL BRIDGE
Actually sends messages to OpenClaw for real processing
Not keyword matching - real AI response
"""

import os
import sys
import json

def send_to_openclawed(message_text, model='Haiku'):
    """
    Send message to OpenClaw for REAL processing
    Uses sessions_send to communicate with the main session
    """
    try:
        # Import OpenClaw functions
        from sessions_send import send_to_session
        
        print(f"\n📨 Enviando para OpenClaw: {message_text}")
        print(f"🤖 Modelo: {model}")
        
        # Send to main session
        response = send_to_session(
            "main",
            f"[Dashboard Input - {model}] {message_text}",
            timeoutSeconds=30
        )
        
        print(f"✅ Resposta OpenClaw: {response}")
        return response
        
    except ImportError:
        print("⚠️ sessions_send não disponível - OpenClaw API não encontrada")
        print("Isto precisa rodar dentro do contexto OpenClaw")
        return None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

if __name__ == "__main__":
    # Test
    if len(sys.argv) > 1:
        msg = sys.argv[1]
        model = sys.argv[2] if len(sys.argv) > 2 else 'Haiku'
        result = send_to_openclawed(msg, model)
        print(f"\nResultado Final: {result}")

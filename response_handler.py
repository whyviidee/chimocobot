"""
RESPONSE HANDLER - Evita respostas cortadas por rate limit
Verifica ANTES de responder
"""

from rate_limiter import limiter
import time

class ResponseHandler:
    def __init__(self):
        self.max_attempts = 3
    
    def can_respond(self, required_tokens=100):
        """Verifica se pode responder com segurança"""
        providers_ok = []
        
        for provider in ["anthropic/claude-haiku-4-5", "openai/gpt-4o-mini", "openai/gpt-4"]:
            can_call, reason = limiter.check_rate_limit(provider)
            if can_call:
                providers_ok.append(provider)
        
        if providers_ok:
            return True, f"✅ Posso responder com {providers_ok[0]}"
        else:
            return False, f"⏸️ Todos os modelos bloqueados. Tenta novamente em 30s"
    
    def wait_until_ready(self, timeout=120):
        """Espera até poder responder com segurança"""
        start = time.time()
        attempt = 0
        
        while time.time() - start < timeout:
            can_respond, reason = self.can_respond()
            
            if can_respond:
                print(f"✅ Pronto! {reason}")
                return True
            
            attempt += 1
            wait_time = min(10 * attempt, 60)  # Max 60s entre tentativas
            print(f"⏳ Aguardando... {reason}. Tentativa em {wait_time}s")
            time.sleep(wait_time)
        
        return False
    
    def safe_respond(self, message):
        """Responde de forma segura (completa ou não responde)"""
        can_respond, reason = self.can_respond()
        
        if not can_respond:
            return f"⏸️ Não consigo responder neste momento:\n{reason}\n\nTenta novamente em 30 segundos."
        
        # Se pode responder, retorna a mensagem completa
        return message


# Instância global
handler = ResponseHandler()


if __name__ == "__main__":
    print("🔥 Response Handler\n")
    
    # Teste
    can_respond, reason = handler.can_respond()
    print(f"Posso responder? {reason}\n")
    
    # Teste de resposta segura
    response = handler.safe_respond("Olá! Tudo bem contigo?")
    print(f"Resposta segura: {response}")

"""
API WRAPPER - Integra Rate Limiter + Fallback automático
Zero rate limits, máxima eficiência
"""

import time
from rate_limiter import limiter
from datetime import datetime

class SmartAPIWrapper:
    def __init__(self):
        self.providers = [
            "anthropic/claude-haiku-4-5",
            "openai/gpt-4o-mini",
            "openai/gpt-4"
        ]
        self.current_provider_idx = 0
    
    def get_next_available_provider(self):
        """Retorna o próximo provider disponível"""
        for i in range(len(self.providers)):
            idx = (self.current_provider_idx + i) % len(self.providers)
            provider = self.providers[idx]
            
            can_call, reason = limiter.check_rate_limit(provider)
            if can_call:
                return idx, provider
        
        # Se nenhum disponível, mostra status
        return None, f"⏸️ Todos os modelos bloqueados. Status:\n{limiter.get_status()}"
    
    def call_api(self, prompt, max_retries=3):
        """Chama API com fallback automático"""
        attempt = 0
        last_error = None
        
        while attempt < max_retries:
            # Verificar cache primeiro
            cache_key = f"prompt_{hash(prompt)}"
            cached = limiter.get_cache(cache_key)
            if cached:
                print(f"💾 Resposta do cache (economizou 1 chamada)")
                return cached
            
            # Obter provider disponível
            idx, provider = self.get_next_available_provider()
            
            if idx is None:
                print(provider)  # Mostra mensagem de bloqueio
                time.sleep(5)
                attempt += 1
                continue
            
            print(f"📤 Tentativa {attempt + 1}: Usando {provider}")
            
            try:
                # Aqui entra a chamada real à API
                # Por enquanto, simular sucesso
                limiter.record_call(provider)
                
                response = f"[Resposta de {provider}]"
                limiter.set_cache(cache_key, response)
                
                print(f"✅ Sucesso com {provider}")
                self.current_provider_idx = idx  # Manter este provider como padrão
                return response
            
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Erro em {provider}: {error_msg}")
                
                # Se for rate limit, bloqueia este provider
                if "429" in error_msg or "rate_limit" in error_msg:
                    limiter.mark_rate_limit(provider)
                
                last_error = e
                # Move para próximo provider
                self.current_provider_idx = (idx + 1) % len(self.providers)
                attempt += 1
                time.sleep(2)  # Espera antes de retry
        
        return f"❌ Falha após {max_retries} tentativas. Último erro: {last_error}"
    
    def get_status(self):
        """Mostra status completo"""
        return limiter.get_status()
    
    def reset(self):
        """Reset de tudo"""
        limiter.reset()


# Instância global
api = SmartAPIWrapper()


if __name__ == "__main__":
    print("🔥 Smart API Wrapper\n")
    
    # Teste
    result = api.call_api("Olá, qual é o teu nome?")
    print(f"Resultado: {result}\n")
    
    print("Status:")
    print(api.get_status())

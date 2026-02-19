"""
RATE LIMITER SYSTEM
Controla chamadas à API pra evitar bloqueios
"""

import time
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self):
        # Rastrear chamadas por provider
        self.calls = defaultdict(list)  # timestamps das chamadas
        self.blocked = {}  # {provider: blocked_until}
        self.cache = {}  # {cache_key: (value, timestamp)}
        self.cache_ttl = 300  # 5 minutos
        
        # Configuração
        self.max_calls_per_minute = 50  # prudente pra todos os providers
        self.min_interval = 1  # mínimo 1 segundo entre chamadas
        self.cooldown_on_429 = 60  # bloqueia por 60s quando 429
    
    def check_rate_limit(self, provider):
        """Verifica se pode fazer chamada"""
        now = datetime.now()
        
        # Se bloqueado, verifica se desbloqueia
        if provider in self.blocked:
            if now < self.blocked[provider]:
                remaining = (self.blocked[provider] - now).total_seconds()
                return False, f"⏸️ {provider} bloqueado por {int(remaining)}s"
            else:
                del self.blocked[provider]
        
        # Limpar chamadas antigas (>1 min)
        minute_ago = now - timedelta(minutes=1)
        self.calls[provider] = [t for t in self.calls[provider] if t > minute_ago]
        
        # Verificar limite por minuto
        if len(self.calls[provider]) >= self.max_calls_per_minute:
            return False, f"🚫 {provider}: limite de {self.max_calls_per_minute}/min atingido"
        
        # Verificar intervalo mínimo
        if self.calls[provider]:
            last_call = self.calls[provider][-1]
            time_since = (now - last_call).total_seconds()
            if time_since < self.min_interval:
                wait_time = self.min_interval - time_since
                return False, f"⏱️ Espera {wait_time:.1f}s antes da próxima chamada"
        
        return True, "✅ Permitido"
    
    def record_call(self, provider):
        """Registra uma chamada bem-sucedida"""
        self.calls[provider].append(datetime.now())
    
    def mark_rate_limit(self, provider):
        """Marca um provider como rate limited (429)"""
        self.blocked[provider] = datetime.now() + timedelta(seconds=self.cooldown_on_429)
        print(f"⚠️ {provider.upper()} rate limited! Bloqueado por {self.cooldown_on_429}s")
    
    def get_cache(self, key):
        """Retorna valor em cache se válido"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return value
            else:
                del self.cache[key]
        return None
    
    def set_cache(self, key, value):
        """Guarda valor em cache"""
        self.cache[key] = (value, datetime.now())
    
    def get_status(self):
        """Status de todos os providers"""
        now = datetime.now()
        status = []
        
        for provider in ["anthropic/claude-haiku-4-5", "openai/gpt-4o-mini", "openai/gpt-4"]:
            if provider in self.blocked and now < self.blocked[provider]:
                remaining = (self.blocked[provider] - now).total_seconds()
                status.append(f"🔴 {provider}: Bloqueado ({int(remaining)}s)")
            else:
                call_count = len([t for t in self.calls[provider] if t > now - timedelta(minutes=1)])
                status.append(f"🟢 {provider}: {call_count}/{self.max_calls_per_minute} chamadas/min")
        
        return "\n".join(status)
    
    def reset(self):
        """Reset manual de tudo"""
        self.calls.clear()
        self.blocked.clear()
        self.cache.clear()
        print("✅ Rate limiter resetado")


# Instância global
limiter = RateLimiter()


if __name__ == "__main__":
    print("🔥 Rate Limiter System\n")
    print(limiter.get_status())
    
    # Simular alguns bloqueios
    print("\nSimulando rate limit no Haiku...")
    limiter.mark_rate_limit("anthropic/claude-haiku-4-5")
    
    print("\n" + limiter.get_status())

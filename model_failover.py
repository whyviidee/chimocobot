"""
MODEL FAILOVER SYSTEM
Alternância automática entre Haiku → OpenAI → Gemini quando rate limit
"""

import time
from datetime import datetime, timedelta

class ModelFailover:
    def __init__(self):
        self.models = [
            {"name": "haiku", "provider": "anthropic", "status": "active", "last_error": None, "blocked_until": None},
            {"name": "openai", "provider": "openai", "status": "active", "last_error": None, "blocked_until": None},
            {"name": "gemini", "provider": "google", "status": "active", "last_error": None, "blocked_until": None},
        ]
        self.current_idx = 0
        self.cooldown_duration = 60  # segundos
    
    def get_next_available_model(self):
        """Retorna o próximo modelo disponível"""
        now = datetime.now()
        
        # Primeiro, verifica qual modelo usar
        for i in range(len(self.models)):
            idx = (self.current_idx + i) % len(self.models)
            model = self.models[idx]
            
            # Se modelo está bloqueado e cooldown ainda ativo, pula
            if model["blocked_until"] and now < model["blocked_until"]:
                continue
            
            # Se modelo está desbloqueado, usa este
            if model["blocked_until"] and now >= model["blocked_until"]:
                model["blocked_until"] = None
                model["last_error"] = None
            
            return idx, model
        
        # Se todos bloqueados, retorna o que vai desbloquear primeiro
        earliest = min(self.models, key=lambda m: m["blocked_until"] or datetime.max)
        wait_time = (earliest["blocked_until"] - now).total_seconds()
        return None, {"error": f"Todos modelos bloqueados. Espera {int(wait_time)}s", "blocked_until": earliest["blocked_until"]}
    
    def mark_rate_limit(self, model_idx):
        """Marca um modelo como rate limited"""
        if model_idx < len(self.models):
            model = self.models[model_idx]
            model["blocked_until"] = datetime.now() + timedelta(seconds=self.cooldown_duration)
            model["last_error"] = "RATE_LIMIT"
            print(f"⚠️ {model['name'].upper()} bloqueado por {self.cooldown_duration}s")
            
            # Move pro próximo
            self.current_idx = (model_idx + 1) % len(self.models)
    
    def mark_error(self, model_idx, error_msg):
        """Marca um erro genérico (não rate limit)"""
        if model_idx < len(self.models):
            model = self.models[model_idx]
            model["last_error"] = error_msg
            print(f"❌ {model['name'].upper()}: {error_msg}")
    
    def get_status(self):
        """Retorna status de todos os modelos"""
        now = datetime.now()
        status = []
        for model in self.models:
            if model["blocked_until"] and now < model["blocked_until"]:
                remaining = (model["blocked_until"] - now).total_seconds()
                status.append(f"🔴 {model['name']}: Bloqueado ({int(remaining)}s)")
            else:
                status.append(f"🟢 {model['name']}: Disponível")
        return "\n".join(status)
    
    def reset_all(self):
        """Reset de todos os modelos (uso manual)"""
        for model in self.models:
            model["blocked_until"] = None
            model["last_error"] = None
        self.current_idx = 0
        print("✅ Todos os modelos resetados")


# Instância global
failover = ModelFailover()


# Exemplo de uso
if __name__ == "__main__":
    print("🔥 Model Failover System\n")
    
    # Simular rate limit no Haiku
    print("Simulando: Haiku rate limit...")
    failover.mark_rate_limit(0)
    
    # Próximo modelo disponível
    idx, model = failover.get_next_available_model()
    print(f"Próximo modelo: {model['name'].upper()}\n")
    
    # Status
    print("Status:")
    print(failover.get_status())

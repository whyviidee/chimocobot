"""
CHIMOCO MISSION CONTROL - API CLIENT
Envia dados em tempo real pro servidor WebSocket
"""

import requests
import json
from datetime import datetime
import threading

class ChimocoAPI:
    def __init__(self, server_url="http://localhost:3000"):
        self.server_url = server_url
        self.current_task = None
        self.thinking_history = []
        
        # Testar conexão
        try:
            response = requests.get(f"{self.server_url}/health", timeout=2)
            if response.status_code == 200:
                print("✅ Conectado ao Chimoco Mission Control Server")
            else:
                print("⚠️ Servidor não respondendo corretamente")
        except Exception as e:
            print(f"⚠️ Servidor não está disponível: {e}")
    
    def start_task(self, task_name, model="Haiku"):
        """Inicia uma nova tarefa"""
        try:
            data = {
                "taskName": task_name,
                "model": model
            }
            response = requests.post(
                f"{self.server_url}/api/task/start",
                json=data,
                timeout=5
            )
            self.current_task = task_name
            self.thinking_history = []
            print(f"▶️ Tarefa iniciada: {task_name}")
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao iniciar tarefa: {e}")
            return None
    
    def add_thinking(self, text):
        """Adiciona um pensamento/step"""
        try:
            data = {"text": text}
            response = requests.post(
                f"{self.server_url}/api/task/thinking",
                json=data,
                timeout=5
            )
            self.thinking_history.append(text)
            print(f"🧠 {text}")
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao enviar pensamento: {e}")
            return None
    
    def complete_task(self, action=None, success=True):
        """Completa uma tarefa"""
        try:
            data = {
                "action": action or self.current_task,
                "success": success
            }
            response = requests.post(
                f"{self.server_url}/api/task/complete",
                json=data,
                timeout=5
            )
            print(f"✅ Tarefa concluída!")
            self.current_task = None
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao completar tarefa: {e}")
            return None
    
    def get_status(self):
        """Obtém status atual"""
        try:
            response = requests.get(
                f"{self.server_url}/api/status",
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao obter status: {e}")
            return None
    
    def reset(self):
        """Reset completo"""
        try:
            response = requests.post(
                f"{self.server_url}/api/reset",
                timeout=5
            )
            self.current_task = None
            self.thinking_history = []
            print("🔄 Sistema resetado!")
            return response.json()
        except Exception as e:
            print(f"❌ Erro ao fazer reset: {e}")
            return None


# Instância global
chimoco = ChimocoAPI()


# Exemplo de uso
if __name__ == "__main__":
    # Simular uma tarefa
    chimoco.start_task("Testando integração")
    chimoco.add_thinking("→ Conectando ao iCloud...")
    chimoco.add_thinking("→ Autenticado com sucesso")
    chimoco.add_thinking("→ Procurando eventos...")
    chimoco.add_thinking("→ ✓ Encontrado!")
    chimoco.complete_task("Teste completo")

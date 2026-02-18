"""
CHIMOCO AUTO-INTEGRATION WRAPPER
Integra automaticamente com Mission Control
"""

import time
import functools
from chimoco_api import chimoco

def report_task(task_name=None):
    """
    Decorator que reporta automaticamente uma tarefa ao Mission Control
    
    Uso:
    @report_task("Editando calendário")
    def editar_evento():
        pass
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Nome da tarefa (default é nome da função)
            task = task_name or func.__name__.replace('_', ' ').title()
            
            # Iniciar tarefa
            chimoco.start_task(task)
            
            try:
                # Executar função
                result = func(*args, **kwargs)
                
                # Completar com sucesso
                chimoco.add_thinking(f"✓ {task} concluída")
                chimoco.complete_task(task, success=True)
                
                return result
            except Exception as e:
                # Completar com erro
                chimoco.add_thinking(f"✗ Erro: {str(e)}")
                chimoco.complete_task(task, success=False)
                raise
        
        return wrapper
    return decorator


def report_thinking(message):
    """
    Função simples pra reportar um pensamento
    
    Uso:
    report_thinking("→ Procurando evento no calendário...")
    """
    chimoco.add_thinking(message)


def report_action(action_name):
    """
    Reporta uma ação individual
    
    Uso:
    with report_action("Editando evento"):
        # código aqui
    """
    class ActionContext:
        def __init__(self, name):
            self.name = name
        
        def __enter__(self):
            chimoco.start_task(self.name)
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type:
                chimoco.add_thinking(f"✗ Erro: {exc_val}")
                chimoco.complete_task(self.name, success=False)
            else:
                chimoco.add_thinking(f"✓ {self.name} concluída")
                chimoco.complete_task(self.name, success=True)
            
            return False
    
    return ActionContext(action_name)


# Exemplo de uso automático
if __name__ == "__main__":
    
    # Exemplo 1: Decorator
    @report_task("Criando evento de teste")
    def create_event():
        report_thinking("→ Conectando ao iCloud...")
        time.sleep(0.5)
        report_thinking("→ Autenticado")
        time.sleep(0.5)
        report_thinking("→ Criando evento...")
        time.sleep(1)
        return {"success": True}
    
    # Exemplo 2: Context Manager
    def edit_event():
        with report_action("Editando evento"):
            report_thinking("→ Procurando evento...")
            time.sleep(0.5)
            report_thinking("→ Removendo emojis...")
            time.sleep(0.5)
            report_thinking("→ Guardando mudanças...")
            time.sleep(0.5)
    
    # Executar exemplos
    print("=== TESTE 1: Decorator ===")
    create_event()
    
    print("\n=== TESTE 2: Context Manager ===")
    edit_event()
    
    print("\n✅ Testes concluídos!")

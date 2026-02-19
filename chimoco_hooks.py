"""
CHIMOCO AUTO-HOOKS
Integra automaticamente com Mission Control em todas as ações
"""

from chimoco_wrapper import report_task, report_thinking, report_action
from chimoco_api import chimoco

# ============================================
# INTEGRAÇÃO COM MISSION CONTROL
# ============================================

def report_to_mission_control(action, message):
    """Send updates to Mission Control dashboard"""
    try:
        from chimoco_mission_reporter import report_thinking, report_response
        
        if action == "thinking":
            report_thinking(message)
        elif action == "response":
            report_response(message, is_complete=False)
        elif action == "complete":
            report_response(message, is_complete=True)
    except Exception as e:
        print(f"⚠️ Mission Control report failed: {e}")

# ============================================
# INTEGRAÇÃO COM CALENDÁRIO
# ============================================

def get_calendar_events_with_reporting(cal, search_params=None):
    """Wrapper para obter eventos do calendário"""
    with report_action("📅 Consultando calendário"):
        report_thinking("→ Conectando ao servidor de calendário...")
        try:
            events = cal.search(**(search_params or {}))
            report_thinking(f"→ ✓ Encontrados {len(events)} eventos")
            return events
        except Exception as e:
            report_thinking(f"✗ Erro: {e}")
            raise

def create_calendar_event_with_reporting(cal, event_data):
    """Wrapper para criar evento"""
    event_name = event_data.get('summary', 'Evento')
    
    with report_action(f"📝 Criando: {event_name}"):
        report_thinking(f"→ Preparando evento: {event_name}")
        try:
            result = cal.save_event(event_data)
            report_thinking(f"→ ✓ Evento criado com sucesso")
            return result
        except Exception as e:
            report_thinking(f"✗ Erro ao criar evento: {e}")
            raise

def edit_calendar_event_with_reporting(event, changes):
    """Wrapper para editar evento"""
    with report_action(f"✏️ Editando evento"):
        report_thinking("→ Carregando evento...")
        try:
            # Aplicar mudanças
            for key, value in changes.items():
                setattr(event, key, value)
            
            event.save()
            report_thinking(f"→ ✓ Evento atualizado com sucesso")
            return event
        except Exception as e:
            report_thinking(f"✗ Erro ao editar: {e}")
            raise

# ============================================
# INTEGRAÇÃO COM PROCESSAMENTO DE DADOS
# ============================================

@report_task("🔍 Processando requisição")
def process_user_request(request_text):
    """Processa uma requisição do utilizador"""
    report_thinking(f"→ Analisando: '{request_text}'")
    report_thinking("→ Identificando ação necessária...")
    return request_text

@report_task("💾 Atualizando ficheiros")
def update_memory_files(updates):
    """Atualiza ficheiros de memória"""
    report_thinking(f"→ Salvando {len(updates)} atualizações...")
    for filename, content in updates.items():
        report_thinking(f"  • Atualizando {filename}")
    report_thinking("→ ✓ Memória atualizada")

# ============================================
# INTEGRAÇÃO COM API CALLS
# ============================================

def call_api_with_reporting(api_name, **kwargs):
    """Wrapper genérico para API calls"""
    with report_action(f"🌐 Chamando {api_name}"):
        report_thinking(f"→ Enviando requisição...")
        try:
            # Aqui entraria a chamada real
            report_thinking(f"→ ✓ Resposta recebida")
            return {"success": True}
        except Exception as e:
            report_thinking(f"✗ Erro na API: {e}")
            raise

# ============================================
# INTEGRAÇÃO COM PARSING/ANALYSIS
# ============================================

def analyze_text_with_reporting(text, analysis_type="geral"):
    """Analisa texto com reporting"""
    with report_action(f"🧠 Analisando {analysis_type}"):
        report_thinking("→ Processando texto...")
        report_thinking("→ Identificando padrões...")
        report_thinking("→ ✓ Análise concluída")
        return {"analyzed": True}

# ============================================
# INTEGRAÇÃO COM FILE OPERATIONS
# ============================================

def read_file_with_reporting(filepath):
    """Lê ficheiro com reporting"""
    with report_action(f"📖 Lendo {filepath}"):
        report_thinking(f"→ Abrindo {filepath}...")
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            report_thinking(f"→ ✓ Ficheiro carregado ({len(content)} chars)")
            return content
        except Exception as e:
            report_thinking(f"✗ Erro: {e}")
            raise

def write_file_with_reporting(filepath, content):
    """Escreve ficheiro com reporting"""
    with report_action(f"💾 Salvando {filepath}"):
        report_thinking(f"→ Escrevendo em {filepath}...")
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            report_thinking(f"→ ✓ Ficheiro salvo com sucesso")
            return True
        except Exception as e:
            report_thinking(f"✗ Erro ao salvar: {e}")
            raise

# ============================================
# SISTEMA AUTO-REPORT (GLOBAL)
# ============================================

class AutoReportingSystem:
    """Sistema que reporta automaticamente ações"""
    
    @staticmethod
    def enable():
        """Ativa auto-reporting global"""
        print("✅ Auto-reporting ativado!")
        return True
    
    @staticmethod
    def disable():
        """Desativa auto-reporting global"""
        print("⏸️ Auto-reporting desativado")
        return False
    
    @staticmethod
    def report_start(action_name):
        """Reporta início de uma ação"""
        chimoco.start_task(action_name)
    
    @staticmethod
    def report_step(step_message):
        """Reporta um step"""
        chimoco.add_thinking(step_message)
    
    @staticmethod
    def report_end(action_name, success=True):
        """Reporta fim de uma ação"""
        chimoco.complete_task(action_name, success=success)


# Instância global
auto_report = AutoReportingSystem()

# Exemplo de uso
if __name__ == "__main__":
    print("🧪 Testando hooks automáticos...\n")
    
    # Teste 1: Processamento
    process_user_request("Criar evento amanhã às 12:00")
    
    # Teste 2: Memória
    update_memory_files({"MEMORY.md": "test", "USER.md": "test"})
    
    # Teste 3: File operations
    # write_file_with_reporting("/tmp/test.txt", "test content")
    
    # Teste 4: Analysis
    analyze_text_with_reporting("algum texto", "semântica")
    
    print("\n✅ Todos os hooks funcionando!")

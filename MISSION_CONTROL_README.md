# 🔥 CHIMOCO MISSION CONTROL - SISTEMA COMPLETO

## O Que É?

Sistema em **tempo real** que mostra:
- ✅ Tarefas atuais do Chimoco
- 🧠 Pensamento/reasoning ao vivo
- 📊 Histórico de ações
- 📈 Estatísticas e performance
- 🎯 Modelos ativos (Haiku, Gemini, OpenAI)

---

## Componentes

### 1. **WebSocket Server (Node.js)**
```bash
cd /home/ubuntu/.openclaw/workspace/chimocobot-server
npm start
# Roda em localhost:3000
```
- API REST para reportar ações
- WebSocket em tempo real
- Broadcast para todos os clientes

### 2. **Dashboard (GitHub Pages)**
```
https://whyviidee.github.io/chimocobot/
```
- Interface visual tipo "Mission Control"
- Atualização em tempo real via WebSocket
- Responsivo (mobile-friendly)

### 3. **Python Client (chimoco_api.py)**
```python
from chimoco_api import chimoco

# Iniciar tarefa
chimoco.start_task("Minha tarefa")

# Adicionar pensamentos
chimoco.add_thinking("→ Step 1")
chimoco.add_thinking("→ Step 2")

# Completar
chimoco.complete_task("Ação realizada")
```

### 4. **Auto-Integration (chimoco_wrapper.py + chimoco_hooks.py)**
```python
from chimoco_hooks import report_action, report_thinking

# Context manager (automático)
with report_action("Editando calendário"):
    report_thinking("→ Procurando evento...")
    # código aqui
    report_thinking("→ ✓ Evento editado")
```

---

## Como Usar

### Opção 1: Decorator (Automático)
```python
from chimoco_wrapper import report_task

@report_task("Criando evento")
def criar_evento():
    # código aqui
    pass

criar_evento()  # Reporta automaticamente
```

### Opção 2: Context Manager
```python
from chimoco_hooks import report_action, report_thinking

with report_action("Editando evento"):
    report_thinking("→ Procurando...")
    # código
    report_thinking("→ ✓ Feito")
```

### Opção 3: Manual
```python
from chimoco_api import chimoco

chimoco.start_task("Tarefa X")
chimoco.add_thinking("→ Passo 1")
chimoco.add_thinking("→ Passo 2")
chimoco.complete_task("Concluído", success=True)
```

---

## API REST Endpoints

### POST /api/task/start
```json
{
  "taskName": "Editando calendário",
  "model": "Haiku"
}
```

### POST /api/task/thinking
```json
{
  "text": "→ Procurando evento..."
}
```

### POST /api/task/complete
```json
{
  "action": "Evento editado",
  "success": true
}
```

### GET /api/status
Retorna estado atual do sistema

---

## Fluxo Típico

1. **Usuário (Yuri)** envia requisição
2. **Chimoco** recebe requisição
3. **Chimoco** inicializa tarefa no Mission Control
4. **Chimoco** envia pensamentos step-by-step
5. **Dashboard** mostra em tempo real via WebSocket
6. **Yuri** vê exatamente o que Chimoco está pensando
7. **Chimoco** completa tarefa e reporta resultado
8. **Dashboard** mostra histórico e estatísticas

---

## Exemplo Completo

```python
# Cenário: Editar evento do calendário

from chimoco_hooks import report_action, report_thinking

with report_action("✏️ Editando: Limpeza da Casa"):
    report_thinking("→ Conectando ao iCloud CalDAV...")
    
    # Conectar (código real aqui)
    
    report_thinking("→ Autenticado com sucesso")
    report_thinking("→ Procurando evento de 23 Fevereiro...")
    
    # Procurar evento
    
    report_thinking("→ ✓ Encontrado!")
    report_thinking("→ Removendo emojis do nome...")
    
    # Editar
    
    report_thinking("→ Sincronizando com iCloud...")
    report_thinking("→ ✓ Evento atualizado!")

# Resultado no dashboard:
# - Tarefa mostrada como "RUNNING" → "COMPLETED"
# - Todos os pensamentos visíveis
# - Tempo total da ação
# - Adicionado ao histórico
```

---

## Status Atual

✅ **Servidor Node.js:** Running (PID: 3837)
✅ **Dashboard:** Live em https://whyviidee.github.io/chimocobot/
✅ **API Python:** Funcionando
✅ **Auto-Integration:** Ativa
✅ **WebSocket:** Conectado

---

## Próximos Passos

1. **Integrar nos workflows principais** — Cada ação minha usa auto-reporting
2. **Customizar dashboard** — Adicionar mais métricas se necessário
3. **Webhook externo** — Se quiseres notificações fora do dashboard
4. **Analytics** — Rastrear performance/padrões

---

## Troubleshooting

### Servidor não responde?
```bash
ps aux | grep node
# Se morreu, reinicia:
cd /home/ubuntu/.openclaw/workspace/chimocobot-server && npm start
```

### Dashboard offline?
```bash
curl http://localhost:3000/health
# Se retornar JSON, servidor está ok
```

### Dados não chegam?
```python
from chimoco_api import chimoco
status = chimoco.get_status()
print(status)  # Ver estado
```

---

## Arquivos

- **Server:** `/home/ubuntu/.openclaw/workspace/chimocobot-server/`
- **Dashboard:** `/home/ubuntu/.openclaw/workspace/chimocobot/`
- **API Python:** `chimoco_api.py`
- **Wrapper:** `chimoco_wrapper.py`
- **Hooks:** `chimoco_hooks.py`

---

## Documentação Rápida

```python
# IMPORTS
from chimoco_api import chimoco
from chimoco_wrapper import report_task, report_thinking, report_action
from chimoco_hooks import auto_report

# START TASK
chimoco.start_task("Nome da tarefa")

# ADD THINKING
chimoco.add_thinking("→ Descrevendo o pensamento")

# COMPLETE TASK
chimoco.complete_task("Descrição da ação", success=True)

# GET STATUS
chimoco.get_status()

# RESET
chimoco.reset()
```

---

**🔥 CHIMOCO MISSION CONTROL v1.0**
**Assistente Pessoal de Yuri | Real-time Reporting System**

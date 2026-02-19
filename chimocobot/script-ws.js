// CHIMOCO MISSION CONTROL - WEBSOCKET CLIENT

// SERVIDOR SEMPRE AWS - SEM LÓGICA COMPLICADA
const SERVER_URL = 'ws://16.16.255.70:3000';

let ws = null;
let taskStartTime = null;
let tasksCompleted = 0;
let reconnectAttempts = 0;
const MAX_RECONNECT = 5;

// Conectar ao servidor WebSocket
function connectWebSocket() {
  try {
    ws = new WebSocket(SERVER_URL);
    
    ws.onopen = () => {
      console.log('✅ Conectado ao Mission Control Server');
      document.querySelector('.status-light').classList.add('online');
      document.querySelector('.status-text').textContent = 'ONLINE';
      reconnectAttempts = 0;
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleServerMessage(data);
    };
    
    ws.onerror = (error) => {
      console.error('❌ Erro WebSocket:', error);
    };
    
    ws.onclose = () => {
      console.log('⚠️ Desconectado do servidor');
      document.querySelector('.status-light').classList.remove('online');
      document.querySelector('.status-text').textContent = 'DEMO MODE';
      
      // Tentar reconectar
      if (reconnectAttempts < MAX_RECONNECT) {
        reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
        console.log(`Tentando reconectar... (${reconnectAttempts}/${MAX_RECONNECT}) em ${delay}ms`);
        setTimeout(connectWebSocket, delay);
      } else {
        console.log('Máximo de tentativas de reconexão atingido.');
      }
    };
  } catch (err) {
    console.error('Erro ao conectar WebSocket:', err);
  }
}

function handleServerMessage(data) {
  const { type, currentTask, history, action, message } = data;
  
  if (type === 'init') {
    updateTaskUI(currentTask);
    updateHistoryUI(history);
  } else if (type === 'task_start') {
    taskStartTime = Date.now();
    updateTaskUI(currentTask);
  } else if (type === 'thinking') {
    updateThinkingUI(message);
  } else if (type === 'task_complete') {
    const duration = Date.now() - taskStartTime;
    tasksCompleted++;
    updateStatsUI();
    updateHistoryUI(history);
  } else if (type === 'action') {
    updateActionUI(action);
  }
}

function updateTaskUI(task) {
  if (!task) return;
  
  const taskName = document.querySelector('[data-section="tarefa"] .section-value');
  const taskStatus = document.querySelector('[data-section="tarefa"] .status-badge');
  const taskTime = document.querySelector('[data-section="tarefa"] .task-time');
  
  if (taskName) taskName.textContent = task.taskName;
  if (taskStatus) taskStatus.textContent = task.status;
  if (taskTime && task.startTime) {
    const elapsed = Math.floor((Date.now() - new Date(task.startTime)) / 1000);
    const hours = String(Math.floor(elapsed / 3600)).padStart(2, '0');
    const minutes = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
    const seconds = String(elapsed % 60).padStart(2, '0');
    taskTime.textContent = `${hours}:${minutes}:${seconds}`;
  }
}

function updateThinkingUI(message) {
  const thinkingBox = document.querySelector('[data-section="pensamento"] .thinking-content');
  if (thinkingBox) {
    thinkingBox.innerHTML += `<div class="thinking-step">→ ${message}</div>`;
    thinkingBox.scrollTop = thinkingBox.scrollHeight;
  }
}

function updateActionUI(action) {
  const actionBox = document.querySelector('[data-section="modelos"] .models-list');
  if (actionBox) {
    const actionEl = document.createElement('div');
    actionEl.className = 'model-item';
    actionEl.innerHTML = `<span class="model-status active">⚙️</span> ${action}`;
    actionBox.appendChild(actionEl);
  }
}

function updateStatsUI() {
  const statsBox = document.querySelector('[data-section="stats"] .stats-content');
  if (statsBox) {
    statsBox.innerHTML = `
      <div class="stat-item">
        <span class="stat-label">TAREFAS</span>
        <span class="stat-value">${tasksCompleted}</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">UPTIME</span>
        <span class="stat-value">99.9%</span>
      </div>
      <div class="stat-item">
        <span class="stat-label">TEMPO MÉDIO</span>
        <span class="stat-value">2.3s</span>
      </div>
    `;
  }
}

function updateHistoryUI(history) {
  const historyBox = document.querySelector('[data-section="historico"] .history-list');
  if (!historyBox) return;
  
  historyBox.innerHTML = '';
  if (history && history.length > 0) {
    history.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = 'history-item';
      itemEl.innerHTML = `
        <span class="history-time">${new Date(item.timestamp).toLocaleTimeString('pt-PT')}</span>
        <span class="history-task">${item.taskName}</span>
        <span class="history-check">✓</span>
      `;
      historyBox.appendChild(itemEl);
    });
  }
}

// Iniciar conexão quando página carrega
document.addEventListener('DOMContentLoaded', () => {
  connectWebSocket();
  
  // Atualizar relógio a cada segundo
  setInterval(() => {
    if (taskStartTime) {
      const elapsed = Math.floor((Date.now() - taskStartTime) / 1000);
      const hours = String(Math.floor(elapsed / 3600)).padStart(2, '0');
      const minutes = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
      const seconds = String(elapsed % 60).padStart(2, '0');
      
      const taskTime = document.querySelector('[data-section="tarefa"] .task-time');
      if (taskTime) taskTime.textContent = `${hours}:${minutes}:${seconds}`;
    }
  }, 1000);
});

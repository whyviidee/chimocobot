// CHIMOCO MISSION CONTROL - WEBSOCKET CLIENT

const SERVER_URL = 'wss://16.16.255.70:3000';
let ws = null;
let taskStartTime = null;

function connectWebSocket() {
  try {
    ws = new WebSocket(SERVER_URL);
    
    ws.onopen = () => {
      console.log('✅ Conectado ao Mission Control Server');
      updateStatus('ONLINE');
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('📨 Mensagem recebida:', data);
        
        if (data.type === 'init') {
          if (data.currentTask) updateTaskUI(data.currentTask);
          if (data.history) updateHistoryUI(data.history);
        } else if (data.type === 'task_start') {
          taskStartTime = Date.now();
          if (data.currentTask) updateTaskUI(data.currentTask);
        } else if (data.type === 'thinking') {
          addThinkingLine(data.text || data.message);
        } else if (data.type === 'task_complete') {
          if (data.history) updateHistoryUI(data.history);
        }
      } catch (e) {
        console.error('Erro ao processar mensagem:', e);
      }
    };
    
    ws.onerror = (error) => {
      console.error('❌ Erro WebSocket:', error);
    };
    
    ws.onclose = () => {
      console.log('⚠️ Desconectado do servidor');
      updateStatus('DEMO MODE');
      setTimeout(connectWebSocket, 3000);
    };
  } catch (err) {
    console.error('Erro ao conectar:', err);
  }
}

function updateStatus(status) {
  const statusEl = document.querySelector('.status-text');
  const lightEl = document.querySelector('.status-light');
  
  if (statusEl) {
    statusEl.textContent = status;
    if (lightEl) {
      if (status === 'ONLINE') {
        lightEl.classList.add('online');
      } else {
        lightEl.classList.remove('online');
      }
    }
  }
}

function updateTaskUI(task) {
  if (!task) return;
  
  const taskName = document.getElementById('taskName');
  const taskStatus = document.getElementById('taskStatus');
  const taskTimer = document.getElementById('taskTimer');
  
  if (taskName) taskName.textContent = task.taskName || 'Sem tarefa';
  if (taskStatus) taskStatus.textContent = task.status || 'IDLE';
  if (taskTimer) taskTimer.textContent = '00:00:00';
}

function addThinkingLine(text) {
  const thinkingContent = document.getElementById('thinkingContent');
  if (!thinkingContent) return;
  
  // Remover placeholder se existir
  const placeholder = thinkingContent.querySelector('.placeholder');
  if (placeholder) placeholder.remove();
  
  const line = document.createElement('div');
  line.className = 'thinking-line';
  line.textContent = '→ ' + text;
  thinkingContent.appendChild(line);
  thinkingContent.scrollTop = thinkingContent.scrollHeight;
}

function updateHistoryUI(history) {
  const historyList = document.querySelector('[data-section="historico"] .history-list');
  if (!historyList || !history) return;
  
  historyList.innerHTML = '';
  history.slice(-5).forEach(item => {
    const itemEl = document.createElement('div');
    itemEl.className = 'history-item';
    const time = new Date(item.timestamp).toLocaleTimeString('pt-PT');
    itemEl.innerHTML = `
      <span class="history-time">${time}</span>
      <span class="history-task">${item.taskName}</span>
      <span class="history-check">✓</span>
    `;
    historyList.appendChild(itemEl);
  });
}

// Timer do relógio
function updateTimer() {
  if (taskStartTime) {
    const elapsed = Math.floor((Date.now() - taskStartTime) / 1000);
    const hours = String(Math.floor(elapsed / 3600)).padStart(2, '0');
    const minutes = String(Math.floor((elapsed % 3600) / 60)).padStart(2, '0');
    const seconds = String(elapsed % 60).padStart(2, '0');
    
    const timer = document.getElementById('taskTimer');
    if (timer) timer.textContent = `${hours}:${minutes}:${seconds}`;
  }
}

// Iniciar quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Iniciando Chimoco Mission Control');
  connectWebSocket();
  
  // Atualizar relógio a cada segundo
  setInterval(updateTimer, 1000);
});

// Reconectar se a página volta ao foco
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && (!ws || ws.readyState !== WebSocket.OPEN)) {
    connectWebSocket();
  }
});

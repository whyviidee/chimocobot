// CHIMOCO MISSION CONTROL - WEBSOCKET CLIENT

// Configurar conexão WebSocket
const SERVER_URL = window.location.hostname === 'localhost' 
  ? 'ws://localhost:3000' 
  : 'ws://' + window.location.hostname + ':3000';

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
      document.querySelector('.status-text').textContent = 'OFFLINE';
      
      // Tentar reconectar
      if (reconnectAttempts < MAX_RECONNECT) {
        reconnectAttempts++;
        console.log(`Tentando reconectar... (${reconnectAttempts}/${MAX_RECONNECT})`);
        setTimeout(connectWebSocket, 3000);
      }
    };
  } catch (error) {
    console.error('Erro ao conectar:', error);
  }
}

// Processar mensagens do servidor
function handleServerMessage(data) {
  switch(data.type) {
    case 'init':
      // Inicialização - receber estado atual
      if (data.currentTask) {
        updateTaskDisplay(data.currentTask);
      }
      if (data.history) {
        updateHistory(data.history);
      }
      break;
    
    case 'taskStart':
      // Tarefa iniciada
      taskStartTime = Date.now();
      updateTaskDisplay(data.task);
      console.log('▶️ Tarefa iniciada:', data.task.taskName);
      break;
    
    case 'thinking':
      // Pensamento recebido
      appendThinking(data.text);
      console.log('🧠', data.text);
      break;
    
    case 'taskComplete':
      // Tarefa completada
      taskStartTime = null;
      tasksCompleted++;
      updateHistory(data.history);
      console.log('✅ Tarefa completada!');
      break;
    
    case 'taskReset':
      // Reset da tarefa
      updateTaskDisplay(data.task);
      clearThinking();
      break;
    
    case 'reset':
      // Reset completo
      location.reload();
      break;
  }
}

// Atualizar display da tarefa
function updateTaskDisplay(task) {
  document.getElementById('taskName').textContent = task.taskName;
  document.getElementById('taskStatus').textContent = task.status;
  
  const statusEl = document.getElementById('taskStatus');
  statusEl.classList.toggle('running', task.status === 'RUNNING');
  
  if (task.status === 'RUNNING') {
    taskStartTime = task.startTime || Date.now();
  }
}

// Adicionar pensamento
function appendThinking(text) {
  const thinkingContent = document.getElementById('thinkingContent');
  
  const placeholder = thinkingContent.querySelector('.placeholder');
  if (placeholder) placeholder.remove();
  
  const p = document.createElement('p');
  p.textContent = text;
  p.style.opacity = '0';
  p.style.transition = 'opacity 0.3s ease';
  p.style.color = '#1dd3b0';
  p.style.marginBottom = '8px';
  
  thinkingContent.appendChild(p);
  
  setTimeout(() => {
    p.style.opacity = '1';
    thinkingContent.scrollTop = thinkingContent.scrollHeight;
  }, 10);
  
  // Limpar se muito grande
  const paragraphs = thinkingContent.querySelectorAll('p');
  if (paragraphs.length > 20) {
    paragraphs[0].remove();
  }
}

// Limpar pensamentos
function clearThinking() {
  const thinkingContent = document.getElementById('thinkingContent');
  thinkingContent.innerHTML = '<p class="placeholder">Pensamento do Chimoco aparecerá aqui...</p>';
}

// Atualizar histórico
function updateHistory(history) {
  const historyContent = document.getElementById('historyContent');
  historyContent.innerHTML = '';
  
  history.forEach(item => {
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.innerHTML = `
      <span class="time">${item.time}</span>
      <span class="action">${item.action}</span>
      <span class="status">${item.status === 'success' ? '✓' : '✗'}</span>
    `;
    historyContent.appendChild(historyItem);
  });
}

// Atualizar relógio
function updateClock() {
  const now = new Date();
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  
  const timeStr = `${hours}:${minutes}:${seconds}`;
  const el = document.getElementById('lastUpdate');
  if (el) el.textContent = timeStr;
}

// Atualizar timer da tarefa
function updateTaskTimer() {
  if (!taskStartTime) return;
  
  const elapsed = Math.floor((Date.now() - taskStartTime) / 1000);
  const hours = Math.floor(elapsed / 3600);
  const minutes = Math.floor((elapsed % 3600) / 60);
  const seconds = elapsed % 60;
  
  const timer = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  
  const el = document.getElementById('taskTimer');
  if (el) el.textContent = timer;
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
  console.log('🔥 Chimoco Mission Control iniciado!');
  
  // Conectar ao servidor
  connectWebSocket();
  
  // Atualizar relógio e timer
  updateClock();
  setInterval(updateClock, 1000);
  setInterval(updateTaskTimer, 1000);
  
  console.log('✓ Sistema pronto para receber dados em tempo real');
});

// Exportar para console (testes)
window.chimocoAPI = {
  sendTaskStart: (name) => {
    fetch('/api/task/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ taskName: name })
    });
  },
  sendThinking: (text) => {
    fetch('/api/task/thinking', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
  },
  sendComplete: (action) => {
    fetch('/api/task/complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, success: true })
    });
  }
};

console.log('API disponível: window.chimocoAPI');

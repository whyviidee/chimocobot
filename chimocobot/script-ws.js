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

// GLOBAL: Current selected model
let selectedModel = 'Haiku';

// Make models clickable
function setupModelSelection() {
  const modelItems = document.querySelectorAll('.model-item');
  
  modelItems.forEach(item => {
    item.style.cursor = 'pointer';
    
    item.addEventListener('click', () => {
      // Remove active from all
      modelItems.forEach(m => m.classList.remove('active'));
      
      // Add active to this
      item.classList.add('active');
      
      // Get model name
      const modelName = item.querySelector('.model-name')?.textContent || 'Haiku';
      selectedModel = modelName;
      
      console.log(`🤖 Selecionado: ${selectedModel}`);
      
      // Report to Mission Control
      fetch('https://16.16.255.70:3000/api/task/thinking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: `🤖 Model selecionado: ${selectedModel}` }),
        credentials: 'omit'
      }).catch(() => {});
    });
  });
  
  // Set Haiku as default active
  modelItems[0]?.classList.add('active');
}

// Chat input handler
function setupChatInput() {
  const chatInput = document.getElementById('chatInput');
  const chatSend = document.getElementById('chatSend');
  const chatResponse = document.getElementById('chatResponse');
  
  if (!chatInput || !chatSend) return;
  
  async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    chatInput.value = '';
    chatResponse.innerHTML = '<p>⏳ Processando com ' + selectedModel + '...</p>';
    chatResponse.style.display = 'block';
    
    try {
      // Iniciar tarefa com modelo selecionado
      await fetch('https://16.16.255.70:3000/api/task/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          taskName: `Chat [${selectedModel}]: ${message.substring(0, 30)}...`,
          model: selectedModel
        }),
        credentials: 'omit'
      });
      
      // Reportar mensagem
      await fetch('https://16.16.255.70:3000/api/task/thinking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: `Yuri (${selectedModel}): ${message}` }),
        credentials: 'omit'
      });
      
      chatResponse.innerHTML = '<p>✅ Mensagem enviada com ' + selectedModel + '!</p>';
      
      setTimeout(() => {
        chatResponse.innerHTML += '<p>💭 Chimoco pensando...</p>';
      }, 1500);
      
    } catch (err) {
      console.error('Erro:', err);
      chatResponse.innerHTML = `<p>⚠️ Enviado (sem resposta visual)</p>`;
    }
  }
  
  chatSend.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
}

// Iniciar quando a página carrega
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Iniciando Chimoco Mission Control');
  connectWebSocket();
  setupModelSelection();
  setupChatInput();
  
  // Atualizar relógio a cada segundo
  setInterval(updateTimer, 1000);
});

// Reconectar se a página volta ao foco
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && (!ws || ws.readyState !== WebSocket.OPEN)) {
    connectWebSocket();
  }
});

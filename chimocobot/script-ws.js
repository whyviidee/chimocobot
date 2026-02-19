// CHIMOCO MISSION CONTROL - WEBSOCKET CLIENT v2

const SERVER_URL = 'wss://16.16.255.70:3000';
let ws = null;
let taskStartTime = null;
let selectedModel = 'Haiku';
let thinkingLines = 0;
let activeTasks = 0;
let completedTasks = 0;

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
        console.log('📨 Mensagem:', data.type);
        
        if (data.type === 'init') {
          if (data.currentTask) updateTaskUI(data.currentTask);
          if (data.history) updateHistoryUI(data.history);
        } else if (data.type === 'task_start') {
          taskStartTime = Date.now();
          activeTasks++;
          if (data.currentTask) updateTaskUI(data.currentTask);
          updateStats();
        } else if (data.type === 'thinking') {
          addThinkingLine(data.text || data.message);
        } else if (data.type === 'task_complete') {
          activeTasks--;
          completedTasks++;
          if (data.history) updateHistoryUI(data.history);
          updateStats();
        }
      } catch (e) {
        console.error('Erro ao processar:', e);
      }
    };
    
    ws.onerror = (error) => {
      console.error('❌ Erro WebSocket:', error);
    };
    
    ws.onclose = () => {
      console.log('⚠️ Desconectado');
      updateStatus('OFFLINE');
      setTimeout(connectWebSocket, 3000);
    };
  } catch (err) {
    console.error('Erro:', err);
  }
}

function updateStatus(status) {
  const statusEl = document.querySelector('.status-text');
  const lightEl = document.querySelector('.status-light');
  
  if (statusEl) statusEl.textContent = status;
  if (lightEl) {
    if (status === 'ONLINE') {
      lightEl.classList.add('online');
    } else {
      lightEl.classList.remove('online');
    }
  }
}

function updateTaskUI(task) {
  if (!task) return;
  
  const taskName = document.getElementById('taskName');
  const taskStatus = document.getElementById('taskStatus');
  
  if (taskName) taskName.textContent = task.taskName || 'Sem tarefa';
  if (taskStatus) taskStatus.textContent = task.status || 'IDLE';
}

function addThinkingLine(text) {
  const thinkingContent = document.getElementById('thinkingContent');
  if (!thinkingContent) return;
  
  // Remove placeholder
  const placeholder = thinkingContent.querySelector('.placeholder');
  if (placeholder) placeholder.remove();
  
  const line = document.createElement('div');
  line.textContent = text;
  
  // Categorize message type
  if (text.includes('📨') || text.includes('Yuri:')) {
    line.className = 'user-message';
  } else if (text.includes('📤') || text.includes('✅ Resposta:') || text.includes('Resposta:')) {
    line.className = 'response';
  } else if (text.includes('💭') || text.includes('Processando') || text.includes('pensamento')) {
    line.className = 'thinking';
  }
  
  // Prevent wrapping with ellipsis
  line.style.wordWrap = 'break-word';
  line.style.whiteSpace = 'normal';
  line.style.maxWidth = '100%';
  
  thinkingContent.appendChild(line);
  
  thinkingLines++;
  
  // Auto-scroll
  setTimeout(() => {
    thinkingContent.scrollTop = thinkingContent.scrollHeight;
  }, 10);
}

function updateHistoryUI(history) {
  const historyList = document.getElementById('historyList');
  if (!historyList || !history) return;
  
  historyList.innerHTML = '';
  history.slice(-5).forEach(item => {
    const itemEl = document.createElement('div');
    itemEl.className = 'history-item';
    const time = new Date(item.timestamp).toLocaleTimeString('pt-PT');
    itemEl.textContent = `${time} - ${item.taskName}`;
    historyList.appendChild(itemEl);
  });
}

function updateStats() {
  const tasksCount = document.getElementById('tasksCount');
  if (tasksCount) {
    tasksCount.textContent = completedTasks;
  }
}

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

// MODEL SELECTION
function setupModelSelection() {
  const modelBtns = document.querySelectorAll('.model-btn');
  
  modelBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modelBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      
      selectedModel = btn.dataset.model;
      console.log(`🤖 Modelo: ${selectedModel}`);
      
      // Report
      fetch(`${SERVER_URL.replace('wss://', 'https://')}/api/task/thinking`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: `🤖 Modelo selecionado: ${selectedModel}` }),
        credentials: 'omit'
      }).catch(() => {});
    });
  });
  
  // Set Haiku as default
  modelBtns[0]?.classList.add('active');
}

// CHAT INPUT
function setupChatInput() {
  const chatInput = document.getElementById('chatInput');
  const chatSend = document.getElementById('chatSend');
  const chatResponse = document.getElementById('chatResponse');
  
  if (!chatInput || !chatSend) return;
  
  async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    chatInput.value = '';
    chatResponse.textContent = `⏳ Enviando com ${selectedModel}...`;
    
    try {
      // Send to Mission Control server
      const res = await fetch(`${SERVER_URL.replace('wss://', 'https://')}/api/chat/message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: message,
          model: selectedModel
        }),
        credentials: 'omit'
      });
      
      if (!res.ok) throw new Error('Server error');
      
      const data = await res.json();
      
      chatResponse.textContent = `✅ Mensagem enviada! Chimoco está a processar...`;
      
      setTimeout(() => {
        chatResponse.textContent = '';
      }, 3000);
      
    } catch (err) {
      console.error('Error:', err);
      chatResponse.textContent = `⚠️ Erro ao enviar`;
      
      setTimeout(() => {
        chatResponse.textContent = '';
      }, 3000);
    }
  }
  
  chatSend.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });
}

// TABS
function setupTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const tabId = btn.dataset.tab;
      
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));
      
      btn.classList.add('active');
      document.getElementById(tabId + '-tab')?.classList.add('active');
    });
  });
}

// INIT
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Chimoco Mission Control v2');
  connectWebSocket();
  setupModelSelection();
  setupChatInput();
  setupTabs();
  
  setInterval(updateTimer, 1000);
});

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible' && (!ws || ws.readyState !== WebSocket.OPEN)) {
    connectWebSocket();
  }
});

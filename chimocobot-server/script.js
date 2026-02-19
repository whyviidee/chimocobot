// CHIMOCO MISSION CONTROL - SCRIPT

// Simular dados em tempo real
let taskStartTime = null;
let tasksCompleted = 0;

// Atualizar relógio
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    document.getElementById('lastUpdate') = `${hours}:${minutes}:${seconds}`;
}

// Atualizar timer da tarefa
function updateTaskTimer() {
    if (!taskStartTime) return;
    
    const elapsed = Math.floor((Date.now() - taskStartTime) / 1000);
    const hours = Math.floor(elapsed / 3600);
    const minutes = Math.floor((elapsed % 3600) / 60);
    const seconds = elapsed % 60;
    
    const timer = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    document.getElementById('taskTimer').textContent = timer;
}

// API para receber dados (webhook)
function receiveTaskData(data) {
    // data: { taskName, status, thinking, model }
    
    if (data.taskName) {
        document.getElementById('taskName').textContent = data.taskName;
    }
    
    if (data.status) {
        const statusEl = document.getElementById('taskStatus');
        statusEl.textContent = data.status;
        statusEl.classList.toggle('running', data.status === 'RUNNING');
        
        if (data.status === 'RUNNING') {
            taskStartTime = Date.now();
        } else if (data.status === 'COMPLETED') {
            taskStartTime = null;
            tasksCompleted++;
            document.getElementById('tasksToday').textContent = tasksCompleted;
        }
    }
    
    if (data.thinking) {
        appendThinking(data.thinking);
    }
    
    if (data.historyItem) {
        addToHistory(data.historyItem);
    }
}

// Adicionar pensamento
function appendThinking(text) {
    const thinkingContent = document.getElementById('thinkingContent');
    
    // Limpar placeholder se existir
    const placeholder = thinkingContent.querySelector('.placeholder');
    if (placeholder) placeholder.remove();
    
    const p = document.createElement('p');
    p.textContent = text;
    p.style.opacity = '0';
    p.style.transition = 'opacity 0.3s ease';
    
    thinkingContent.appendChild(p);
    
    // Scroll ao final
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

// Adicionar ao histórico
function addToHistory(item) {
    const historyContent = document.getElementById('historyContent');
    
    const now = new Date();
    const time = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    historyItem.innerHTML = `
        <span class="time">${time}</span>
        <span class="action">${item.action}</span>
        <span class="status">${item.status === 'success' ? '✓' : '✗'}</span>
    `;
    
    historyContent.insertBefore(historyItem, historyContent.firstChild);
    
    // Manter apenas 5 últimos
    const items = historyContent.querySelectorAll('.history-item');
    for (let i = items.length - 1; i >= 5; i--) {
        items[i].remove();
    }
}

// Simular eventos (para teste)
function simulateTask() {
    const tasks = [
        'Editando evento do calendário',
        'Criando novo evento',
        'Sincronizando com iCloud',
        'Processando pedido de Yuri',
        'Analisando calendários'
    ];
    
    const randomTask = tasks[Math.floor(Math.random() * tasks.length)];
    
    receiveTaskData({
        taskName: randomTask,
        status: 'RUNNING',
        model: 'Haiku'
    });
    
    // Simular pensamento
    setTimeout(() => {
        const thoughts = [
            '→ Procurando evento no calendário...',
            '→ Conectando ao iCloud CalDAV...',
            '→ Autenticado com sucesso',
            '→ Editando dados do evento...',
            '→ Sincronizando mudanças...',
            '→ ✓ Concluído!'
        ];
        
        thoughts.forEach((thought, index) => {
            setTimeout(() => {
                receiveTaskData({ thinking: thought });
            }, index * 300);
        });
    }, 500);
    
    // Completar após 3 segundos
    setTimeout(() => {
        receiveTaskData({
            status: 'COMPLETED',
            historyItem: {
                action: randomTask,
                status: 'success'
            }
        });
    }, 3000);
}

// Função para receber dados via fetch (webhook)
async function setupWebhook() {
    // Simular recepção de dados a cada 30 segundos (para teste)
    // Na prática, isto viria de um webhook enviado pelo Chimoco
    
    // Para desenvolvimento, podes fazer POST aqui:
    // POST /api/task com { taskName, status, thinking }
}

// Inicializar
document.addEventListener('DOMContentLoaded', () => {
    // Atualizar relógio
    updateClock();
    setInterval(updateClock, 1000);
    
    // Atualizar timer
    setInterval(updateTaskTimer, 1000);
    
    // Simular tarefas para teste (remover em produção)
    console.log('Chimoco Mission Control iniciado!');
    console.log('Aguardando dados via webhook...');
    
    // Para teste: descomenta isto para ver simulações
    // simulateTask();
    // setInterval(simulateTask, 8000);
});

// Exportar função para receber dados (webhook)
window.receiveTaskData = receiveTaskData;

console.log('✓ Chimoco Mission Control pronto!');
console.log('Para enviar dados: window.receiveTaskData({ taskName, status, thinking, historyItem })');

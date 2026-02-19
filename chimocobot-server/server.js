// CHIMOCO MISSION CONTROL - WEBSOCKET SERVER

const express = require('express');
const WebSocket = require('ws');
const cors = require('cors');
const https = require('https');
const fs = require('fs');

const app = express();

// Load SSL certificates
const options = {
  key: fs.readFileSync('/tmp/key.pem'),
  cert: fs.readFileSync('/tmp/cert.pem')
};

const server = https.createServer(options, app);
const wss = new WebSocket.Server({ 
  server,
  perMessageDeflate: false,
  clientTracking: true
});
const path = require('path');

const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Servir ficheiros estáticos do dashboard
app.use(express.static(path.join(__dirname, '../chimocobot')));

// Estado global
let connectedClients = [];
let currentTask = {
  taskName: 'Aguardando tarefa...',
  status: 'IDLE',
  thinking: [],
  startTime: null
};

let taskHistory = [];

// WebSocket - Conexão de clientes
wss.on('connection', (ws) => {
  console.log('✅ Cliente conectado ao Mission Control');
  
  // Enviar estado atual
  ws.send(JSON.stringify({
    type: 'init',
    currentTask: currentTask,
    history: taskHistory.slice(-5)
  }));
  
  connectedClients.push(ws);
  
  // Quando cliente desconecta
  ws.on('close', () => {
    console.log('❌ Cliente desconectado');
    connectedClients = connectedClients.filter(client => client !== ws);
  });
  
  // Erro
  ws.on('error', (error) => {
    console.error('Erro WebSocket:', error);
  });
});

// Broadcast para todos os clientes
function broadcastToClients(data) {
  connectedClients.forEach(client => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(data));
    }
  });
}

// API - Iniciar tarefa
app.post('/api/task/start', (req, res) => {
  const { taskName, model } = req.body;
  
  currentTask = {
    taskName: taskName || 'Nova tarefa',
    status: 'RUNNING',
    thinking: [],
    startTime: Date.now(),
    model: model || 'Haiku'
  };
  
  console.log(`🚀 Tarefa iniciada: ${taskName}`);
  
  broadcastToClients({
    type: 'taskStart',
    task: currentTask
  });
  
  res.json({ success: true, task: currentTask });
});

// API - Adicionar pensamento
app.post('/api/task/thinking', (req, res) => {
  const { text } = req.body;
  
  if (text) {
    currentTask.thinking.push(text);
    
    broadcastToClients({
      type: 'thinking',
      text: text,
      thinkingHistory: currentTask.thinking
    });
  }
  
  res.json({ success: true });
});

// API - Completar tarefa
app.post('/api/task/complete', (req, res) => {
  const { success, action } = req.body;
  
  currentTask.status = 'COMPLETED';
  
  // Adicionar ao histórico
  taskHistory.push({
    time: new Date().toLocaleTimeString('pt-PT'),
    action: action || currentTask.taskName,
    status: success !== false ? 'success' : 'error',
    duration: currentTask.startTime ? Date.now() - currentTask.startTime : 0
  });
  
  // Manter apenas últimas 10
  if (taskHistory.length > 10) {
    taskHistory.shift();
  }
  
  console.log(`✅ Tarefa concluída: ${action}`);
  
  broadcastToClients({
    type: 'taskComplete',
    history: taskHistory.slice(-5)
  });
  
  // Reset
  setTimeout(() => {
    currentTask = {
      taskName: 'Aguardando tarefa...',
      status: 'IDLE',
      thinking: [],
      startTime: null
    };
    
    broadcastToClients({
      type: 'taskReset',
      task: currentTask
    });
  }, 1000);
  
  res.json({ success: true });
});

// API - Status
app.get('/api/status', (req, res) => {
  res.json({
    currentTask,
    history: taskHistory,
    connectedClients: connectedClients.length
  });
});

// API - Reset
app.post('/api/reset', (req, res) => {
  currentTask = {
    taskName: 'Aguardando tarefa...',
    status: 'IDLE',
    thinking: [],
    startTime: null
  };
  
  taskHistory = [];
  
  broadcastToClients({
    type: 'reset'
  });
  
  res.json({ success: true });
});

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date() });
});

// Iniciar servidor
server.listen(PORT, '0.0.0.0', () => {
  console.log(`
╔══════════════════════════════════════╗
║  🔥 CHIMOCO MISSION CONTROL SERVER  ║
║  Porta: ${PORT}                        
║  WebSocket: ws://16.16.255.70:${PORT} 
║  API: http://16.16.255.70:${PORT}/api 
╚══════════════════════════════════════╝
  `);
});

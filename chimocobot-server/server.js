// CHIMOCO MISSION CONTROL - WEBSOCKET SERVER

const express = require('express');
const WebSocket = require('ws');
const cors = require('cors');
const https = require('https');
const fs = require('fs');
const { spawn } = require('child_process');

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

// Function to process message with Python bridge
function processMessageWithPython(message, model) {
  return new Promise((resolve) => {
    // Call Python script to process message
    const python = spawn('python3', [
      '/home/ubuntu/.openclaw/workspace/dashboard_openclawed_bridge.py'
    ]);
    
    let output = '';
    let errorOutput = '';
    
    python.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    python.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    python.on('close', (code) => {
      // Try to extract response from output
      const lines = output.split('\n');
      let response = 'Processado com sucesso';
      
      for (let line of lines) {
        if (line.includes('Final Response:')) {
          response = line.replace('Final Response:', '').trim();
          break;
        }
        if (line.includes('Response sent:')) {
          response = line.replace('Response sent:', '').trim();
          break;
        }
      }
      
      resolve(response);
    });
    
    // Give it 10 seconds timeout
    setTimeout(() => {
      python.kill();
      resolve('Timeout ao processar');
    }, 10000);
  });
}

// API - Chat Message from Dashboard
app.post('/api/chat/message', async (req, res) => {
  const { message, model } = req.body;
  
  if (!message) {
    return res.status(400).json({ error: 'Message required' });
  }
  
  // Start task
  currentTask = {
    taskName: `[${model || 'Haiku'}] ${message.substring(0, 40)}...`,
    status: 'RUNNING',
    thinking: [],
    startTime: Date.now(),
    model: model || 'Haiku'
  };
  
  // Add to history
  const historyItem = {
    timestamp: new Date().toISOString(),
    taskName: `Yuri: ${message}`,
    type: 'user_message'
  };
  taskHistory.push(historyItem);
  if (taskHistory.length > 20) taskHistory.shift();
  
  // Broadcast to clients
  broadcastToClients({
    type: 'task_start',
    currentTask: currentTask
  });
  
  // Report message received
  broadcastToClients({
    type: 'thinking',
    text: `📨 Yuri: ${message}`
  });
  
  // Process message asynchronously
  res.json({ 
    success: true,
    message: 'Processing...'
  });
  
  // Process in background
  try {
    const response = await processMessageWithPython(message, model);
    
    // Broadcast response
    broadcastToClients({
      type: 'thinking',
      text: `✅ Resposta: ${response}`
    });
    
    // Add response to history
    taskHistory.push({
      timestamp: new Date().toISOString(),
      taskName: `Response: ${response.substring(0, 50)}...`,
      type: 'response'
    });
    if (taskHistory.length > 20) taskHistory.shift();
    
  } catch (err) {
    console.error('Error processing message:', err);
    broadcastToClients({
      type: 'thinking',
      text: '❌ Erro ao processar'
    });
  }
});

// API - Submit Response from Chimoco
app.post('/api/response/submit', (req, res) => {
  const { responseText, messageId } = req.body;
  
  if (!responseText) {
    return res.status(400).json({ error: 'Response required' });
  }
  
  // Broadcast response to dashboard
  broadcastToClients({
    type: 'thinking',
    text: `📤 Chimoco: ${responseText}`
  });
  
  // Add to history
  taskHistory.push({
    timestamp: new Date().toISOString(),
    taskName: `Response: ${responseText.substring(0, 50)}...`,
    type: 'response'
  });
  if (taskHistory.length > 20) taskHistory.shift();
  
  res.json({
    success: true,
    message: 'Response submitted'
  });
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

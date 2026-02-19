# 🔥 Chimoco Mission Control

Dashboard em tempo real para acompanhar as ações do Chimoco (assistente pessoal de Yuri).

## Ficheiros

- `index.html` - Estrutura principal (HTML)
- `style.css` - Estilos e design (CSS)
- `script.js` - Lógica e interatividade (JavaScript)
- `README.md` - Este ficheiro

## Como Usar Localmente

1. Coloca os 3 ficheiros (`index.html`, `style.css`, `script.js`) na mesma pasta
2. Abre `index.html` no browser
3. O dashboard carrega com layout pronto

## Deploy no amen.pt / chimocobot.pt

### Via File Manager (amen.pt)

1. Acessa o painel de controlo do amen.pt
2. Clica em **File Manager**
3. Navega pra pasta `public_html` ou `www`
4. Faz upload dos 3 ficheiros:
   - `index.html`
   - `style.css`
   - `script.js`
5. Pronto! Acessa `https://chimocobot.pt`

### Via FTP (se preferir)

1. Abre client FTP (Filezilla, WinSCP, etc.)
2. Conecta com dados FTP do amen.pt
3. Navega pra `public_html` ou `www`
4. Faz upload dos 3 ficheiros
5. Confirma no browser

## Webhook - Enviar Dados em Tempo Real

Para fazer o dashboard atualizar com dados do Chimoco em tempo real:

### 1. JavaScript (no browser)
```javascript
window.receiveTaskData({
    taskName: 'Editando calendário',
    status: 'RUNNING',
    thinking: '→ Procurando evento...',
    model: 'Haiku'
});

// Depois, quando termina:
window.receiveTaskData({
    status: 'COMPLETED',
    historyItem: {
        action: 'Editou evento com sucesso',
        status: 'success'
    }
});
```

### 2. Integração com Chimoco

Nota: Isto será configurado depois! Por agora, o dashboard é estático.

Quando integrado, o Chimoco vai enviar:
- Task atual
- Status (RUNNING/COMPLETED)
- Thinking/reasoning step-by-step
- Histórico de ações

## Features

✅ Dashboard moderno tipo Mission Control
✅ Mostra tarefa atual + status
✅ Pensamento em tempo real (thinking)
✅ Modelos ativos (Haiku, Gemini, OpenAI)
✅ Próximos eventos de calendário
✅ Estatísticas
✅ Histórico das últimas ações
✅ Recursos (CPU, memória, etc.)
✅ Design responsivo (mobile-friendly)

## Cores & Design

- **Primária:** Laranja (#ff6b35) — Chimoco
- **Secundária:** Azul escuro (#004e89) — Segurança
- **Accent:** Verde neon (#1dd3b0) — Status positivo
- **Fundo:** Gradiente escuro — Tema futurista

## Testes

Para simular dados (teste local):
Abre o browser console e executa:
```javascript
window.receiveTaskData({
    taskName: 'Teste',
    status: 'RUNNING'
});
```

## Notas

- Website é 100% estático (HTML/CSS/JS) — funciona em qualquer servidor
- Sem dependências externas
- Funciona offline (exceto dados em tempo real)
- Design responsivo para mobile

## Próximas Atualizações

- [ ] Webhook para receber dados em tempo real
- [ ] Gráficos de performance
- [ ] Notificações push
- [ ] Integração com calendário iCloud
- [ ] Modo dark/light
- [ ] Exportar relatórios

---

**Chimoco Mission Control v1.0**
Assistente Pessoal de Yuri | 🔥

# MEMORY.md - Long-Term Memory (Chimoco)

## Sobre Yuri

**Dados Essenciais:**
- Nome: Yuri
- Idade: 29 anos (faz 30 no **26 de Março**)
- Localização: Lisboa, Portugal
- Timezone: WET/WEST
- Profissão: DJ
- Educação: Eng. Informática, IST Técnico
- Origem: Moçambicano (Maputo), vive em Lisboa desde 2014

**Características:**
- Inteligente, direto, pragmático
- Valoriza eficiência e praticidade
- Gosta de naturalidade — não quer robô corporativo
- Amigo de pessoas que entendem nuance e gíria de Moçambique
- Consciente de custos (não quer subscrições caras)

**Pet:**
- Camões (gato preto, um olho) — é uma lenda

## Setup Técnico

**Assistente:** Chimoco (🔥)
- Linguagem: Português (Moçambique)
- Vibe: Broski, descontraído, útil, inteligente
- Comportamento: Proactivo, confirma antes de agir, aprende sobre Yuri

**Models Configurados:**
1. Haiku (Anthropic) — primário, mais barato
2. Gemini (Google) — fallback, bom equilíbrio
3. OpenAI — último recurso, mais potente mas caro

**Integração Apple Calendar:**
- Email: ydagot@icloud.com
- Autenticação: App-specific password (segura)
- Status: Configurado

## Preferências & Compromissos

- Confirmação antes de ações externas (emails, mensagens, lembretes)
- Otimização de custos: Haiku > Gemini > OpenAI
- Sugestões inteligentes (não aleatórias)
- Nunca inventar ou assumir detalhes

## Notas Iniciais

- Yuri é novo no setup — ainda a aprender seu ritmo, padrões, necessidades
- Fazer perguntas naturais pra conhecer melhor
- Progressivamente entender trabalho de DJ, calendário, rotina

## Integração iCloud Calendar ✅

**Status:** FUNCIONAL
- Script Python: `icloud_calendar.py` (CalDAV via caldav library)
- Autenticação: App-specific password (segura, no .env)
- Calendários sincronizados: 7 (Trabalho, Reminders, Work, Home, GIGS NAO CONFIRMADOS, Pessoal, GIGS)
- Eventos a puxar: ✅ Funcionando

**Morning Report (Cron Job):**
- Cron: `morning_report.py` → Gera resumo diário às 9 AM
- Mostra: Eventos de hoje + próximos 3 dias
- Entrega: Telegram, interactivo
- Status: ✅ ATIVO (próxima: amanhã 9 AM)

**Nota:** Anteriormente estava com erro de parsing. Corrigido usando `.icalendar_component` do caldav 2.0.

## Sistema de Reportagem

**Mission Control Ativo:**
- Servidor WebSocket: http://localhost:3000 ✅
- Dashboard: https://whyviidee.github.io/chimocobot/ 🔥
- Auto-reporting: Ativado para todos os workflows
- Dados em tempo real: Enviados ao dashboard automaticamente

**Como Funciona:**
- Cada ação minha é reportada automaticamente
- Dashboard mostra pensamento/reasoning ao vivo
- Histórico de ações atualizado em tempo real
- Yuri vê exatamente o que tou a fazer e como tou a pensar

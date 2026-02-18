# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Chimoco Mission Control

### Server Info
- **URL:** http://localhost:3000
- **WebSocket:** ws://localhost:3000
- **Status:** ✅ Running
- **PID:** 3837

### API Endpoints
- `POST /api/task/start` - Start new task
- `POST /api/task/thinking` - Add thinking step
- `POST /api/task/complete` - Complete task
- `GET /api/status` - Get current status

### Dashboard
- **Public:** https://whyviidee.github.io/chimocobot/
- **Updates:** Real-time via WebSocket

### Python Client
```python
from chimoco_api import chimoco

chimoco.start_task("Task Name")
chimoco.add_thinking("Step 1...")
chimoco.add_thinking("Step 2...")
chimoco.complete_task()
```

---

Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

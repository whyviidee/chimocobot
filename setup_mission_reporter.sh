#!/bin/bash
# Setup Mission Control Auto-Reporter

echo "📊 Configurando Mission Control Auto-Reporter..."

# Create wrapper script that runs after every response
cat > /home/ubuntu/.openclaw/workspace/report_response.sh << 'EOF'
#!/bin/bash
# Called after every response to report to Mission Control

MESSAGE=$1
THINKING=$2

# Send to Mission Control
curl -s -X POST https://16.16.255.70:3000/api/task/thinking \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$THINKING\"}" \
  -k > /dev/null 2>&1

# Log
echo "[$(date)] Reported: $THINKING" >> /tmp/mission_reporter.log
EOF

chmod +x /home/ubuntu/.openclaw/workspace/report_response.sh

echo "✅ Reporter setup completo!"
echo "📝 Script: /home/ubuntu/.openclaw/workspace/report_response.sh"

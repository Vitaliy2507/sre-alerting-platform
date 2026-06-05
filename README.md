# SRE Alerting Platform with AI

Prometheus + Alertmanager + n8n + Claude API + Telegram Bot.

## Quick start

1. Clone repository
2. Copy `.env.example` to `.env` and fill your tokens:
   - `TELEGRAM_BOT_TOKEN` - from @BotFather
   - `CLAUDE_API_KEY` - from proxyapi.ru
3. Start the stack: `docker-compose up -d`
4. Make scripts executable: `chmod +x scripts/set-webhook.sh scripts/send-test-alert.sh`
5. Run ngrok: `ngrok http 5678`
6. Setup Telegram webhook: `./scripts/set-webhook.sh https://your-ngrok-url.ngrok-free.dev YOUR_BOT_TOKEN`
7. Send test alert: `./scripts/send-test-alert.sh https://your-ngrok-url.ngrok-free.dev`

## Workflows

- Alert webhook receives Prometheus alerts
- Claude API analyzes root cause and recommends actions
- Telegram bot shows buttons: Take/Escalate/Decline
- Callback webhook posts public audit messages

## URLs (local)

- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- n8n: http://localhost:5678

## Scripts

- `scripts/set-webhook.sh` - configures Telegram webhook for callback workflow
- `scripts/send-test-alert.sh` - sends test alert to the system
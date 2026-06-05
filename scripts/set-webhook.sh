#!/bin/bash
WEBHOOK_URL=$1
BOT_TOKEN=$2
curl -F "url=${WEBHOOK_URL}/webhook/telegram-callback" \
  https://api.telegram.org/bot${BOT_TOKEN}/setWebhook
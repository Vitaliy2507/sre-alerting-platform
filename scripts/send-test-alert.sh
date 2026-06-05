#!/bin/bash
WEBHOOK_URL=$1
curl -X POST ${WEBHOOK_URL}/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{"alertname": "AppDown", "message": "Database connection timeout, pod crashed"}'
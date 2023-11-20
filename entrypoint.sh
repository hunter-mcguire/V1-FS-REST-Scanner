#!/bin/sh

# Check if PORT environment variable is set, otherwise set it to default value
if [ -z "$PORT" ]; then
  PORT=8000
fi

# Start gunicorn with the specified host and port
gunicorn -k uvicorn.workers.UvicornWorker main:app -w 1 -b 0.0.0.0:${PORT}
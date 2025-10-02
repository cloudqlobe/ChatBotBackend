#!/bin/bash
# Start Action Server
rasa run actions --port 5055 &

# Start Rasa Server (use Render's $PORT env)
rasa run -m models --enable-api --cors "*" --debug --port $PORT

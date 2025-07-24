#!/bin/bash
set -e

echo "Starting Ollama server..."
# Démarrez ollama serve directement (pas en arrière-plan d'abord)
ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
sleep 15

echo "Pulling model: ${OLLAMA_MODEL:-gemma2:2b}"
ollama pull ${OLLAMA_MODEL:-gemma2:2b}

echo "Available models:"
ollama list

echo "Ollama setup complete!"

# Gardez le processus ollama serve au premier plan
wait $OLLAMA_PID
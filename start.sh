#!/usr/bin/env bash

set -e

echo "Installing Lamar OS frontend dependencies..."
cd frontend
npm install

echo "Building Lamar OS executive interface..."
npm run build

cd ..

echo "Starting Lamar PPP OS..."
uvicorn lamar_os.api.app:app \
  --host 0.0.0.0 \
  --port "${PORT:-8000}"

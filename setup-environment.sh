#!/bin/bash
echo "Create virtual environment"
python3 -m venv .venv

echo "Activate the virtual environment"
source .venv/bin/activate

echo "Install requirements"
uv pip install -r requirements.txt 

echo "Start temporal app; http://localhost:8233"
docker run --rm -p 7233:7233 -p 8233:8233 temporalio/temporal:latest server start-dev --ip 0.0.0.0


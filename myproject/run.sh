#!/bin/bash
# DevLocate startup script for Linux/Mac
export PYTHONPATH="$(pwd)"
python -m uvicorn main:app --reload --port 8000

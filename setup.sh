#!/bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is already activated"
else
    # Check if the virtual environment directory exists
    if [ -d ".venv" ]; then
        echo "Activating the virtual environment..."
        source .venv/bin/activate
    else
        echo "Virtual environment not found. Please ensure that '.venv' exists in the current directory."
        exit 1
    fi
fi

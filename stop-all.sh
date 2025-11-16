#!/bin/bash
echo "Stopping OrgLead AI services..."

if [ -f .backend.pid ]; then
    BACKEND_PID=$(cat .backend.pid)
    echo "Stopping Backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null
    rm .backend.pid
fi

if [ -f .python.pid ]; then
    PYTHON_PID=$(cat .python.pid)
    echo "Stopping Python (PID: $PYTHON_PID)..."
    kill $PYTHON_PID 2>/dev/null
    rm .python.pid
fi

echo "All services stopped!"

#!/bin/bash
# start-all.sh - Launch all services for OrgLead AI

echo "=============================================="
echo "  OrgLead AI - Starting All Services"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Create logs directory
mkdir -p logs

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${RED}Port $1 is already in use!${NC}"
        echo "Kill the process: lsof -ti:$1 | xargs kill -9"
        return 1
    fi
    return 0
}

# Check ports
echo "Checking ports..."
check_port 8080 || exit 1
check_port 8000 || exit 1

# Start Backend
echo ""
echo -e "${YELLOW}Starting Spring Boot Backend...${NC}"
cd backend
./mvnw spring-boot:run > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}Backend starting (PID: $BACKEND_PID)${NC}"
cd ..

# Start Python Service
echo ""
echo -e "${YELLOW}Starting Python AI Service...${NC}"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

python app.py > logs/python.log 2>&1 &
PYTHON_PID=$!
echo -e "${GREEN}Python service starting (PID: $PYTHON_PID)${NC}"

# Wait for services
echo ""
echo "Waiting for services to start..."
sleep 10

# Test services
echo ""
echo "Testing services..."

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Python service running on http://localhost:8000${NC}"
else
    echo -e "${RED}✗ Python service failed${NC}"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}Services Started!${NC}"
echo "=============================================="
echo "Backend PID:  $BACKEND_PID"
echo "Python PID:   $PYTHON_PID"
echo ""
echo "Access points:"
echo "  • Backend:  http://localhost:8080"
echo "  • Python:   http://localhost:8000"
echo ""
echo "To stop: kill $BACKEND_PID $PYTHON_PID"
echo "=============================================="

# Save PIDs
echo "$BACKEND_PID" > .backend.pid
echo "$PYTHON_PID" > .python.pid

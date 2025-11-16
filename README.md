# org.lead.ai
CS 1200 Project

# OrgLead AI - Complete Code Files for GitHub

## 📁 File Structure Overview

```
org.lead.ai/
├── backend/
│   └── src/main/java/com/orglead/ai/backend/
│       ├── config/
│       │   └── CorsConfig.java                    [NEW FILE]
│       ├── dto/UserDTO/LlmDTO/
│       │   └── Request.java                       [FIXED]
│       └── service/
│           └── UserService.java                   [FIXED]
├── app.py                                         [NEW FILE]
├── chatBot.py                                     [FIXED]
├── requirements.txt                               [NEW FILE]
├── README.md                                      [UPDATED]
├── start-all.sh                                   [NEW FILE]
├── start-all.bat                                  [NEW FILE]
└── frontend/                                      [NEW FOLDER]
    ├── package.json                               [NEW FILE]
    ├── public/
    │   └── index.html                             [NEW FILE]
    └── src/
        ├── App.js                                 [NEW FILE]
        ├── App.css                                [NEW FILE]
        └── index.js                               [NEW FILE]
```

---

## 1️⃣ FIXED: Request.java

**Path:** `backend/src/main/java/com/orglead/ai/backend/dto/UserDTO/LlmDTO/Request.java`

```java
package com.orglead.ai.backend.dto.UserDTO.LlmDTO;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class Request {
    private String text;
    private Long userId;
}
```

---

## 2️⃣ FIXED: UserService.java

**Path:** `backend/src/main/java/com/orglead/ai/backend/service/UserService.java`

```java
package com.orglead.ai.backend.service;

import com.orglead.ai.backend.dto.UserDTO.CreateAccountRequest;
import com.orglead.ai.backend.dto.UserDTO.LoginRequest;
import com.orglead.ai.backend.dto.UserDTO.Response;
import com.orglead.ai.backend.model.User;
import com.orglead.ai.backend.repository.UserRepository;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {
    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public Response create(CreateAccountRequest userRequest) {
        try {
            User newUser = User.builder()
                    .email(userRequest.getEmail())
                    .password(userRequest.getPassword())
                    .firstName(userRequest.getFirstName())
                    .lastName(userRequest.getLastName())
                    .build();

            userRepository.save(newUser);

            return Response.builder()
                    .message("User created successfully!")
                    .id(newUser.getId())
                    .email(userRequest.getEmail())
                    .firstName(userRequest.getFirstName())
                    .lastName(userRequest.getLastName())
                    .build();
        } catch (Exception e) {
            return Response.builder()
                    .message("Fail: " + e.getMessage())
                    .build();
        }
    }

    public Response login(LoginRequest userRequest) {
        String requestEmail = userRequest.getEmail();
        String requestPassword = userRequest.getPassword();
        Optional<User> user = userRepository.findByEmailAndPassword(requestEmail, requestPassword);

        if (user.isPresent()) {
            return Response.builder()
                    .message("User successfully logged in!")
                    .id(user.get().getId())
                    .email(user.get().getEmail())
                    .firstName(user.get().getFirstName())
                    .lastName(user.get().getLastName())
                    .build();
        }

        return Response.builder()
                .message("Incorrect credentials!")
                .build();
    }

    public Response update(Long id, CreateAccountRequest userRequest) {
       Optional<User> user = userRepository.findById(id);

       if(user.isPresent()) {
           user.get().setEmail(userRequest.getEmail());
           user.get().setPassword(userRequest.getPassword());
           user.get().setFirstName(userRequest.getFirstName());
           user.get().setLastName(userRequest.getLastName());
          userRepository.save(user.get());

          return Response.builder()
                  .message("Account Updated Successfully!")
                  .id(id)
                  .email(user.get().getEmail())
                  .firstName(user.get().getFirstName())
                  .lastName(user.get().getLastName())
                  .build();
       }
       return Response.builder()
               .message("Unable To Update Account! Unable To Find Account!")
               .build();
    }

    public Response delete(Long id) {
        Optional<User> user = userRepository.findById(id);

        if(user.isPresent()) {
            userRepository.delete(user.get());
            return Response.builder()
                    .message("Account Successfully Deleted")
                    .build();
        }
        return Response.builder()
                .message("Unable To Delete Account! Unable To Find Account!")
                .build();
    }
}
```

---

## 3️⃣ NEW: CorsConfig.java

**Path:** `backend/src/main/java/com/orglead/ai/backend/config/CorsConfig.java`

**⚠️ Create the `config` folder first if it doesn't exist!**

```java
package com.orglead.ai.backend.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig {
    
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/**")
                        .allowedOrigins(
                            "http://localhost:3000", 
                            "http://localhost:5173",
                            "http://127.0.0.1:3000",
                            "http://127.0.0.1:5173"
                        )
                        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                        .allowedHeaders("*")
                        .allowCredentials(true)
                        .maxAge(3600);
            }
        };
    }
}
```

---

## 4️⃣ FIXED: chatBot.py

**Path:** `chatBot.py` (root directory)

```python
import re
from datetime import datetime, timedelta

class SchedulingChatbot:
    """
    A simulated AI Chatbot focused on NLP-driven scheduling tasks.
    
    This class simulates the core logic of intent recognition, entity extraction,
    and managing a simple calendar. In a production system, 'extract_intent'
    and 'extract_entities' would be powered by advanced NLP models (e.g., PyTorch,
    spaCy, or Hugging Face Transformers) to handle complex and ambiguous user language.
    """
    
    def __init__(self):
        # A simple dictionary to store scheduled events (simulated calendar)
        # Key: Date string (e.g., "2025-11-05"), Value: List of events/descriptions
        self.calendar = {}
        print("🤖 Scheduling Chatbot initialized. Ready to process input.")

    def extract_intent(self, text: str) -> str:
        """
        Determines the user's intent from the input text.
        (Simulated NLP Intent Classification)
        
        Args:
            text: The raw user input string.
        
        Returns:
            The determined intent ('add_event', 'check_schedule', 'suggestion', 'unknown').
        """
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ["schedule", "add", "put in", "book"]):
            return 'add_event'
        if any(keyword in text_lower for keyword in ["what is", "show me", "check my", "agenda", "calendar"]):
            return 'check_schedule'
        if any(keyword in text_lower for keyword in ["suggest", "advice", "free time", "help me plan"]):
            return 'suggestion'
        return 'unknown'

    def extract_entities(self, text: str) -> dict:
        """
        Extracts key entities (date, time, event name) from the text.
        (Simulated NLP Named Entity Recognition - NER)
        
        Args:
            text: The raw user input string.
        
        Returns:
            A dictionary of extracted entities.
        """
        entities = {'event': None, 'date': None, 'time': None}

        # Simple date pattern simulation (e.g., "tomorrow", "Nov 15", "today")
        date_match = re.search(r'on (.*?)(?: at |$)', text, re.IGNORECASE)
        if date_match:
            entities['date'] = date_match.group(1).strip()
            # Simple simulation to convert common dates
            if 'today' in entities['date'].lower():
                entities['date'] = datetime.now().strftime('%Y-%m-%d')
            elif 'tomorrow' in entities['date'].lower():
                entities['date'] = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            # For demonstration, we assume a clean date format is provided or derived

        # Simple time pattern simulation (e.g., "at 3pm", "14:00")
        time_match = re.search(r'at (\d{1,2}(?::\d{2})?\s?(?:am|pm|o\'clock)?)', text, re.IGNORECASE)
        if time_match:
            entities['time'] = time_match.group(1).strip()

        # Simple event extraction (the rest of the text, typically)
        # This is very basic and would be handled better by a token-based model
        event_match = re.search(r'to (.*?)(?: on |$)', text, re.IGNORECASE)
        if event_match:
            entities['event'] = event_match.group(1).strip()

        return entities

    def add_event(self, date: str, event_details: str) -> str:
        """Adds a new event to the calendar."""
        if not date or not event_details:
            return "❌ Error: I need a date and details to add an event."

        if date not in self.calendar:
            self.calendar[date] = []

        self.calendar[date].append(event_details)
        return f"✅ Success! Event '{event_details}' scheduled for {date}."

    def get_schedule(self, date: str) -> str:
        """Retrieves the schedule for a given date."""
        if not date:
            return "❌ Error: Please specify a date to check the schedule."

        if date in self.calendar and self.calendar[date]:
            events = "\n  - " + "\n  - ".join(self.calendar[date])
            return f"🗓️ Your schedule for {date}:\n{events}"
        else:
            return f"✨ You have no events scheduled for {date}. Free day!"

    def make_suggestion(self) -> str:
        """Offers a scheduling suggestion based on the current calendar state."""
        # Simple suggestion: find the day with the fewest events
        if not self.calendar:
            return "💡 Your calendar is empty! Why not schedule a break or a learning session?"

        day_counts = {date: len(events) for date, events in self.calendar.items()}
        # Find the day with the minimum number of events
        lightest_day = min(day_counts, key=day_counts.get)
        min_events = day_counts[lightest_day]

        if min_events == 0:
            return f"💡 I see {lightest_day} is completely free. That would be a great time for a deep work session or a fitness class."
        elif min_events <= 1:
            return f"💡 {lightest_day} only has {min_events} event(s). I suggest blocking out two hours that day for a high-priority task."
        else:
            return "💡 Your calendar looks pretty packed this week. Make sure to schedule short breaks between your meetings!"

    def process_input(self, user_input: str) -> str:
        """
        The main processing pipeline: intent -> entities -> action.
        """
        intent = self.extract_intent(user_input)
        entities = self.extract_entities(user_input)
        response = ""

        print(f"\n[DEBUG] Input: '{user_input}'")
        print(f"[DEBUG] Intent Detected: {intent}")
        print(f"[DEBUG] Entities Extracted: {entities}")

        if intent == 'add_event':
            event = entities.get('event')
            if event and entities.get('date'):
                response = self.add_event(entities['date'], f"{event} ({entities.get('time', 'Time unspecified')})")
            else:
                response = "🤔 I need more details to schedule that. Please tell me the event and the date/time."

        elif intent == 'check_schedule':
            date_to_check = entities.get('date', datetime.now().strftime('%Y-%m-%d'))  # Default to today
            response = self.get_schedule(date_to_check)

        elif intent == 'suggestion':
            response = self.make_suggestion()

        else:
            response = "I'm sorry, I only handle scheduling and suggestion requests. Try asking to 'schedule a meeting' or 'check my calendar'."

        return response


if __name__ == '__main__':
    # Initialize and run the demonstration
    bot = SchedulingChatbot()
    print("-" * 50)
    print("DEMO: Enter commands to test the chatbot.")
    print("-" * 50)

    # 1. Add an event
    input_1 = "I need to add a meeting to finalize the project proposal to the calendar on 2025-11-15 at 3pm"
    print(f"User: {input_1}")
    print(f"Bot: {bot.process_input(input_1)}")
    print("-" * 20)

    # 2. Add another event (using today shortcut)
    input_2 = "Can you schedule a deep work session on today at 10:00am"
    print(f"User: {input_2}")
    print(f"Bot: {bot.process_input(input_2)}")
    print("-" * 20)

    # 3. Check the schedule
    input_3 = "What is my agenda for 2025-11-15?"
    print(f"User: {input_3}")
    print(f"Bot: {bot.process_input(input_3)}")
    print("-" * 20)

    # 4. Get a suggestion
    input_4 = "Can you suggest when I have free time?"
    print(f"User: {input_4}")
    print(f"Bot: {bot.process_input(input_4)}")
    print("-" * 50)

    # 5. Check today's schedule
    input_5 = "Show me what I have today."
    print(f"User: {input_5}")
    print(f"Bot: {bot.process_input(input_5)}")
    print("-" * 50)
```

---

## 5️⃣ NEW: app.py

**Path:** `app.py` (root directory)

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from chatBot import SchedulingChatbot
import traceback

app = Flask(__name__)
CORS(app)

# Initialize the chatbot
bot = SchedulingChatbot()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_input = data.get('text', '')
        
        if not user_input:
            return jsonify({'error': 'No text provided'}), 400
        
        print(f"[Flask] Received input: {user_input}")
        
        response = bot.process_input(user_input)
        
        print(f"[Flask] Sending response: {response}")
        
        return jsonify({'response': response}), 200
    
    except Exception as e:
        print(f"[Flask] Error: {str(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Chatbot is running'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'OrgLead AI Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            '/chat': 'POST - Send chat messages',
            '/health': 'GET - Check API health'
        }
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("Starting OrgLead AI Scheduling Chatbot API")
    print("=" * 60)
    print("API running on: http://localhost:8000")
    print("Endpoints:")
    print("  - POST http://localhost:8000/chat")
    print("  - GET  http://localhost:8000/health")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8000, debug=True)
```

---

## 6️⃣ NEW: requirements.txt

**Path:** `requirements.txt` (root directory)

```
Flask==3.0.0
flask-cors==4.0.0
Werkzeug==3.0.1
```

---

## 7️⃣ NEW: start-all.sh (Linux/Mac)

**Path:** `start-all.sh` (root directory)

```bash
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
```

**Make it executable:**
```bash
chmod +x start-all.sh
```

---

## 8️⃣ NEW: start-all.bat (Windows)

**Path:** `start-all.bat` (root directory)

```batch
@echo off
echo ==============================================
echo   OrgLead AI - Starting All Services
echo ==============================================

REM Create logs directory
if not exist logs mkdir logs

REM Start Backend
echo.
echo Starting Spring Boot Backend...
cd backend
start "OrgLead Backend" cmd /k "mvnw.cmd spring-boot:run"
cd ..

REM Wait
timeout /t 10 /nobreak

REM Start Python Service
echo.
echo Starting Python AI Service...

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

start "OrgLead Python" cmd /k "python app.py"

echo.
echo ==============================================
echo Services Started!
echo ==============================================
echo.
echo Access points:
echo   - Backend:  http://localhost:8080
echo   - Python:   http://localhost:8000
echo.
echo Close the terminal windows to stop services
echo ==============================================

pause
```

---

## 9️⃣ NEW: stop-all.sh (Linux/Mac)

**Path:** `stop-all.sh` (root directory)

```bash
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
```

**Make it executable:**
```bash
chmod +x stop-all.sh
```

---

## 🔟 UPDATED: README.md

**Path:** `README.md` (root directory)

```markdown
# OrgLead AI

CS 1200 Group Project - AI-Powered Scheduling Assistant

## 🚀 Quick Start

### Prerequisites
- Java 21
- Python 3.8+
- Maven (included as mvnw)
- PostgreSQL (configured via Supabase)

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/org.lead.ai.git
cd org.lead.ai
```

### 2. Start Services

#### Option A: Automated (Recommended)

**Linux/Mac:**
```bash
chmod +x start-all.sh
./start-all.sh
```

**Windows:**
```batch
start-all.bat
```

#### Option B: Manual

**Terminal 1 - Backend:**
```bash
cd backend
./mvnw spring-boot:run
```

**Terminal 2 - Python Service:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 3. Access Application

- Backend API: http://localhost:8080
- Python API: http://localhost:8000
- Frontend: See `frontend/` directory or use React artifact

## 📁 Project Structure

```
org.lead.ai/
├── backend/               # Spring Boot backend
│   ├── src/
│   └── pom.xml
├── frontend/              # React frontend
│   ├── src/
│   └── package.json
├── chatBot.py            # AI chatbot logic
├── app.py                # Flask API wrapper
├── requirements.txt      # Python dependencies
├── start-all.sh          # Linux/Mac startup script
├── start-all.bat         # Windows startup script
└── README.md
```

## 🧪 Testing

### Test Backend
```bash
curl -X POST http://localhost:8080/user/create \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass","firstName":"John","lastName":"Doe"}'
```

### Test Python Service
```bash
curl http://localhost:8000/health
```

### Test Chat
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '"Schedule a meeting tomorrow at 3pm"'
```

## 🛠️ Tech Stack

- **Backend:** Spring Boot, PostgreSQL, JPA
- **AI Service:** Python, Flask, NLP
- **Frontend:** React, Tailwind CSS
- **Database:** PostgreSQL (Supabase)

## 📝 Features

- ✅ User authentication (signup/login)
- ✅ AI-powered scheduling assistant
- ✅ Natural language processing
- ✅ Calendar management
- ✅ Event scheduling and suggestions

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Linux/Mac
lsof -ti:8080 | xargs kill -9

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Backend Won't Start
```bash
cd backend
./mvnw clean install
./mvnw spring-boot:run
```

### Python Errors
```bash
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 👥 Contributors

- David A
- [Add team members]

## 📄 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- CS 1200 Course
- Spring Boot Documentation
- Flask Documentation
```

---

## 1️⃣1️⃣ NEW: .gitignore (Update)

**Path:** `.gitignore` (root directory)

```
# Python
venv/
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Java/Maven
target/
.mvn/wrapper/maven-wrapper.jar
*.class
*.jar
*.war
*.ear

# IDE
.idea/
.vscode/
*.iml
*.iws
*.ipr
.DS_Store

# Logs
logs/
*.log

# Environment
.env
.env.local

# Process IDs
.backend.pid
.python.pid

# Frontend
frontend/node_modules/
frontend/build/
frontend/.env

# Database
*.db
*.sqlite
```

---

## 1️⃣2️⃣ Frontend Files (Optional Standalone)

### package.json

**Path:** `frontend/package.json`

```json
{
  "name": "orglead-ai-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "lucide-react": "^0.263.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

### public/index.html

**Path:** `frontend/public/index.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="OrgLead AI - Your Smart Scheduling Assistant" />
    <title>OrgLead AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
```

### src/index.js

**Path:** `frontend/src/index.js`

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './App.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

### src/App.css

**Path:** `frontend/src/App.css`

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-in-out;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### src/App.js

**Path:** `frontend/src/App.js`

**⚠️ Copy the complete React component from the "Complete React Frontend App" artifact above**

---

## 📋 Checklist for GitHub

- [ ] Copy all fixed Java files to backend
- [ ]



import React, { useState, useEffect, useRef } from 'react';
import { Send, UserPlus, LogIn, Calendar, User, LogOut, Loader } from 'lucide-react';

const API_BASE_URL = 'http://localhost:8080';

export default function OrgLeadAIApp() {
  const [view, setView] = useState('login');
  const [user, setUser] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [signupForm, setSignupForm] = useState({
    email: '', password: '', firstName: '', lastName: ''
  });
  const [error, setError] = useState('');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleLogin = async () => {
    if (!loginForm.email || !loginForm.password) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/user/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginForm)
      });
      
      const data = await response.json();
      
      if (data.id) {
        setUser(data);
        setView('chat');
        setMessages([{
          text: `Welcome back, ${data.firstName}! I'm your scheduling assistant. How can I help you today?`,
          sender: 'bot',
          timestamp: new Date()
        }]);
        setLoginForm({ email: '', password: '' });
      } else {
        setError(data.message || 'Login failed. Please check your credentials.');
      }
    } catch (error) {
      console.error('Login error:', error);
      setError('Cannot connect to server. Please make sure the backend is running on port 8080.');
    }
    
    setLoading(false);
  };

  const handleSignup = async () => {
    if (!signupForm.email || !signupForm.password || !signupForm.firstName || !signupForm.lastName) {
      setError('Please fill in all fields');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      const response = await fetch(`${API_BASE_URL}/user/create`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(signupForm)
      });
      
      const data = await response.json();
      
      if (data.id) {
        alert('Account created successfully! Please login.');
        setView('login');
        setSignupForm({ email: '', password: '', firstName: '', lastName: '' });
        setError('');
      } else {
        setError(data.message || 'Signup failed. Email might already be in use.');
      }
    } catch (error) {
      console.error('Signup error:', error);
      setError('Cannot connect to server. Please make sure the backend is running on port 8080.');
    }
    
    setLoading(false);
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { 
      text: inputMessage, 
      sender: 'user',
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage('');
    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(currentInput)
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const botResponse = await response.text();
      
      setMessages(prev => [...prev, { 
        text: botResponse, 
        sender: 'bot',
        timestamp: new Date()
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      setMessages(prev => [...prev, {
        text: '❌ Sorry, I could not connect to the chatbot service. Please make sure:\n1. Backend is running on port 8080\n2. Python Flask app is running on port 8000',
        sender: 'bot',
        timestamp: new Date()
      }]);
    }
    
    setLoading(false);
  };

  const handleLogout = () => {
    setUser(null);
    setMessages([]);
    setView('login');
    setError('');
  };

  const handleKeyPress = (e, action) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      action();
    }
  };

  if (view === 'login') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md border border-gray-100">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-indigo-100 p-4 rounded-2xl">
              <Calendar className="w-12 h-12 text-indigo-600" />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-center text-gray-800 mb-2">OrgLead AI</h1>
          <p className="text-center text-gray-600 mb-8">Your Smart Scheduling Assistant</p>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input
                type="email"
                placeholder="your@email.com"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                value={loginForm.email}
                onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                onKeyPress={(e) => handleKeyPress(e, handleLogin)}
                disabled={loading}
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              <input
                type="password"
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                onKeyPress={(e) => handleKeyPress(e, handleLogin)}
                disabled={loading}
              />
            </div>
            
            <button
              onClick={handleLogin}
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-lg"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Logging in...
                </>
              ) : (
                <>
                  <LogIn className="w-5 h-5" />
                  Login
                </>
              )}
            </button>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={() => {
                setView('signup');
                setError('');
              }}
              className="text-indigo-600 hover:text-indigo-700 font-semibold transition"
              disabled={loading}
            >
              Don't have an account? Sign up
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (view === 'signup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md border border-gray-100">
          <div className="flex items-center justify-center mb-6">
            <div className="bg-purple-100 p-4 rounded-2xl">
              <UserPlus className="w-12 h-12 text-purple-600" />
            </div>
          </div>
          
          <h1 className="text-4xl font-bold text-center text-gray-800 mb-2">Create Account</h1>
          <p className="text-center text-gray-600 mb-8">Join OrgLead AI today</p>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">First Name</label>
                <input
                  type="text"
                  placeholder="John"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  value={signupForm.firstName}
                  onChange={(e) => setSignupForm({...signupForm, firstName: e.target.value})}
                  disabled={loading}
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Last Name</label>
                <input
                  type="text"
                  placeholder="Doe"
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                  value={signupForm.lastName}
                  onChange={(e) => setSignupForm({...signupForm, lastName: e.target.value})}
                  disabled={loading}
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input
                type="email"
                placeholder="your@email.com"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                value={signupForm.email}
                onChange={(e) => setSignupForm({...signupForm, email: e.target.value})}
                disabled={loading}
              />
            </div>
            
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Password</label>
              <input
                type="password"
                placeholder="••••••••"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition"
                value={signupForm.password}
                onChange={(e) => setSignupForm({...signupForm, password: e.target.value})}
                onKeyPress={(e) => handleKeyPress(e, handleSignup)}
                disabled={loading}
              />
            </div>
            
            <button
              onClick={handleSignup}
              disabled={loading}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-3 rounded-xl hover:from-purple-700 hover:to-pink-700 transition disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-lg flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Creating Account...
                </>
              ) : (
                <>
                  <UserPlus className="w-5 h-5" />
                  Create Account
                </>
              )}
            </button>
          </div>

          <div className="mt-6 text-center">
            <button
              onClick={() => {
                setView('login');
                setError('');
              }}
              className="text-purple-600 hover:text-purple-700 font-semibold transition"
              disabled={loading}
            >
              Already have an account? Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
      <header className="bg-white shadow-md border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-indigo-100 p-2 rounded-xl">
              <Calendar className="w-8 h-8 text-indigo-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">OrgLead AI</h1>
              <p className="text-xs text-gray-500">Scheduling Assistant</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-4 py-2 bg-gray-50 rounded-xl border border-gray-200">
              <User className="w-5 h-5 text-gray-600" />
              <span className="font-semibold text-gray-700">{user?.firstName} {user?.lastName}</span>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 text-gray-700 hover:bg-red-50 hover:text-red-600 rounded-xl transition border border-transparent hover:border-red-200"
            >
              <LogOut className="w-4 h-4" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-5xl w-full mx-auto p-6 flex flex-col">
        <div className="bg-white rounded-3xl shadow-xl flex-1 flex flex-col overflow-hidden border border-gray-200">
          <div className="flex-1 overflow-y-auto p-6 space-y-4" style={{maxHeight: 'calc(100vh - 250px)'}}>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fadeIn`}
              >
                <div
                  className={`max-w-xl px-5 py-3 rounded-2xl shadow-md ${
                    msg.sender === 'user'
                      ? 'bg-gradient-to-r from-indigo-600 to-purple-600 text-white'
                      : 'bg-gradient-to-r from-gray-100 to-gray-50 text-gray-800 border border-gray-200'
                  }`}
                >
                  <div className="whitespace-pre-wrap">{msg.text}</div>
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 px-5 py-3 rounded-2xl border border-gray-200">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="border-t border-gray-200 p-6 bg-gradient-to-r from-gray-50 to-white">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => handleKeyPress(e, handleSendMessage)}
                placeholder="Ask me to schedule something or check your calendar..."
                className="flex-1 px-5 py-4 border-2 border-gray-300 rounded-2xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition shadow-sm"
                disabled={loading}
              />
              <button
                onClick={handleSendMessage}
                disabled={loading || !inputMessage.trim()}
                className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-4 rounded-2xl hover:from-indigo-700 hover:to-purple-700 transition disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              >
                <Send className="w-6 h-6" />
              </button>
            </div>
            
            <div className="mt-3 flex gap-2 flex-wrap">
              <button
                onClick={() => setInputMessage("Schedule a meeting tomorrow at 3pm")}
                className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition"
                disabled={loading}
              >
                Schedule meeting
              </button>
              <button
                onClick={() => setInputMessage("What's on my calendar today?")}
                className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition"
                disabled={loading}
              >
                Check today
              </button>
              <button
                onClick={() => setInputMessage("Suggest when I have free time")}
                className="px-3 py-1 text-xs bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700 transition"
                disabled={loading}
              >
                Get suggestions
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

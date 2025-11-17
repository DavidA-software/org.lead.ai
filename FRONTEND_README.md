# OrgLead AI Frontend

A modern React frontend application with authentication, password reset, and chatbot integration.

## Features

- ✅ User Authentication (Login/Register)
- ✅ Password Reset Functionality
- ✅ AI Chatbot Interface
- ✅ Modern UI with gradient design
- ✅ Responsive layout
- ✅ Real-time chat messaging

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Frontend

```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Backend Endpoints

The frontend connects to the following backend endpoints:

- **Base URL**: `http://localhost:8080`

### User Endpoints
- `POST /user/create` - Register new user
- `POST /user/login` - User login
- `POST /user/forgot-password` - Request password reset
- `POST /user/reset-password` - Reset password with token

### Chatbot Endpoints
- `POST /api/chat` - Send message to chatbot

## Project Structure

```
src/
├── components/
│   ├── Login.js           # Login page
│   ├── Register.js        # Registration page
│   ├── ForgotPassword.js  # Forgot password page
│   ├── ResetPassword.js   # Reset password page
│   ├── Chatbot.js         # Chatbot interface
│   ├── Auth.css           # Authentication styles
│   └── Chatbot.css        # Chatbot styles
├── services/
│   └── api.js             # API service layer
├── App.js                 # Main app component with routing
├── App.css                # App styles
├── index.js               # Entry point
└── index.css              # Global styles
```

## Usage

1. **Register/Login**: Create an account or sign in
2. **Chatbot**: After logging in, interact with the AI scheduling assistant
3. **Password Reset**: Use "Forgot password" link to reset your password

## Notes

- Make sure the backend is running on port 8080
- Make sure the Python chatbot service is running on port 8000
- User sessions are stored in localStorage


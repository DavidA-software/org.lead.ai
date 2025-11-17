import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Login from './components/Login';
import Register from './components/Register';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import Chatbot from './components/Chatbot';
import './App.css';

const queryClient = new QueryClient();

function App() {
  const [user, setUser] = React.useState(() => {
    const savedUser = localStorage.getItem('user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="App">
          <Routes>
            <Route 
              path="/login" 
              element={!user ? <Login setUser={setUser} /> : <Navigate to="/chatbot" />} 
            />
            <Route 
              path="/register" 
              element={!user ? <Register setUser={setUser} /> : <Navigate to="/chatbot" />} 
            />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route 
              path="/chatbot" 
              element={user ? <Chatbot user={user} setUser={setUser} /> : <Navigate to="/login" />} 
            />
            <Route path="/" element={<Navigate to={user ? "/chatbot" : "/login"} />} />
          </Routes>
        </div>
      </Router>
    </QueryClientProvider>
  );
}

export default App;


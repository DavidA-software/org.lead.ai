import React from 'react';
import { Link } from 'react-router-dom';
import './Auth.css';

const ForgotPassword = () => {
  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>OrgLead AI</h1>
        <h2>Reset Password</h2>
        <p className="subtitle">To reset your password, you need your current password</p>

        <div className="info-box">
          <p>Simply go to the reset password page and enter:</p>
          <ul>
            <li>Your email</li>
            <li>Your current password</li>
            <li>Your new password</li>
          </ul>
        </div>

        <Link to="/reset-password" className="submit-btn" style={{ textDecoration: 'none', display: 'block', textAlign: 'center' }}>
          Go to Reset Password
        </Link>

        <p className="auth-switch">
          Remember your password? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;

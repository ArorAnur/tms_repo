import React from 'react';
import { useAuth } from '../contexts/AuthContext';

function WelcomeBanner() {
  const { user } = useAuth();

  // Guard against rendering if user profile state hasn't loaded yet
  if (!user) return null;

  // Capitalize the first letter for clean display presentation
  const formattedName = user.username;

  return (
    <div style={{
      backgroundColor: '#f8f9fa',
      borderLeft: '4px solid #007bff',
      padding: '15px 20px',
      borderRadius: '4px',
      marginBottom: '20px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.02)'
    }}>
      <h3 style={{ margin: 0, color: '#333', fontSize: '20px' }}>
        Welcome back, <span style={{ color: '#007bff' }}>{formattedName}</span>!
      </h3>
    
    </div>
  );
}

export default WelcomeBanner;
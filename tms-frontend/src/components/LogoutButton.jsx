import React from 'react';
import { logoutUser } from '../services/auth';

function LogoutButton() {
  return (
    <button 
      onClick={logoutUser}
      style={{
        padding: '8px 16px',
        backgroundColor: '#dc3545',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontWeight: 'bold'
      }}
    >
      Disconnect Session
    </button>
  );
}

export default LogoutButton;
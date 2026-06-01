import React, { useState } from 'react';
import { getAccessToken, loginUser } from '../services/auth';
import { useAuth } from '../contexts/AuthContext';

function Login() {
  const { loginSuccess } = useAuth(); 
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

 const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
    await loginUser(username, password);
      loginSuccess(getAccessToken()); // Update global auth state with new token
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication rejected.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '100px auto', padding: '30px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h2>TMS Portal Login</h2>
      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
        <button type="submit" disabled={isLoading}>{isLoading ? 'Loading...' : 'Sign In'}</button>
      </form>
    </div>
  );
}

export default Login;
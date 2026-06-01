import React, { createContext, useContext, useState, useEffect } from 'react';
import { getAccessToken, logoutUser } from '../services/auth';
import {jwtDecode} from 'jwt-decode';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const [user, setUser] = useState(null); // Stores metadata like { username: 'anurag', role: 'admin' } 

  useEffect(() => {
    // Run on app initialization to see if an active session exists
    const token = getAccessToken();
    if (token) {
      try {
        const decoded = jwtDecode(token);
        console.log("Decoded token on initialization:", decoded);
        setIsAuthenticated(true);
        setUser({ username: decoded.username, scopes: decoded.scopes }); // Assuming token has 'username' and 'scope' claims
      } catch (error) {
        console.error("Malformed token on initialization:", error);
        logoutUser(); // Clean up corrupted storage
      }
    }
    setIsInitializing(false);
  }, []);

  const loginSuccess = (token) => {

    try {
        const decoded = jwtDecode(token);
        console.log("Decoded token on login:", decoded);
        setIsAuthenticated(true);
        setUser({ username: decoded.username, scopes: decoded.scopes });

    } catch (error) {
        console.error("Malformed token on login:", error);
        logoutUser(); // Clean up corrupted storage
        return; // Exit early since we can't trust the token
    }
   // const decoded = jwtDecode(token);
   // setUser({ username: decoded.username });
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
    logoutUser(); // Clears storage and redirects
  };

  return (
    <AuthContext.Provider value={{ user,isAuthenticated, isInitializing, loginSuccess, handleLogout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
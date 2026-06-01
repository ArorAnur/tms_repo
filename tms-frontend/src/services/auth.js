import axios from 'axios';

// Storage Key Constants to prevent typo bugs
const ACCESS_KEY = 'accessToken';
const REFRESH_KEY = 'refreshToken';

export const getAccessToken = () => localStorage.getItem(ACCESS_KEY);
export const getRefreshToken = () => localStorage.getItem(REFRESH_KEY);

/**
 * Handles credentials exchange and sets up session tokens.
 */
export const loginUser = async (username, password) => {
  // Use a direct axios call to point to the base URL explicitly
  const response = await axios.post('http://localhost:8000/api/token/', { username, password });
  const { access, refresh } = response.data;

  localStorage.setItem(ACCESS_KEY, access);
  localStorage.setItem(REFRESH_KEY, refresh);

  return response.data;
};

/**
 * Silent background refresh worker using an isolated network channel.
 */
export const refreshUserSession = async () => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) throw new Error("Missing rotation credentials.");

  const response = await axios.post('http://localhost:8000/api/token/refresh/', {
    refresh: refreshToken
  });

  const newAccessToken = response.data.access;
  localStorage.setItem(ACCESS_KEY, newAccessToken);
  return newAccessToken;
};

/**
 * Flushes memory arrays and routes user to the login portal.
 */
export const logoutUser = () => {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
  window.location.href = '/login';
};



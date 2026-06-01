import './App.css'
import LogoutButton from './components/LogoutButton';
import Dashboard from './pages/Dashboard'
import Login from './pages/Login';
import { useAuth } from './contexts/AuthContext';


function App() {

  const {isAuthenticated, isInitializing } = useAuth();


  return (
    <>
    {isAuthenticated ? (<><Dashboard /></>) : (<Login />)}
    {isAuthenticated ? (<><LogoutButton /></>) : null}
    </>
  )
}

export default App

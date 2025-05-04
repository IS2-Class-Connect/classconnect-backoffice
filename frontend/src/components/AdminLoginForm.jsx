import { useState } from 'react';
import api from '../api/axios';
import '../styles/LoginForm.css'; 
import { useNavigate } from 'react-router-dom';

function AdminLoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const res = await api.post("/admins/login", {
        email: username,
        password: password,
      });
      localStorage.setItem('token', res.data.access_token);
      navigate('/home');
    } catch (err) {
      console.error(err);
      alert('Login fallido');
    }
    setIsLoading(false);
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Login Admin</h2>
        <form onSubmit={handleLogin} className="login-form">
          <input
            type="text"
            className="login-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            className="login-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit" className="login-button" disabled={isLoading}>
            {isLoading ? 'Iniciando...' : 'Iniciar Sesión'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AdminLoginForm;

import { useState } from 'react';
import api from '../api/axios';
import '../styles/LoginForm.css'; 
import { useNavigate } from 'react-router-dom';

function AdminLoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage(''); // Limpiar mensaje anterior
    try {
      const res = await api.post("/admins/login", {
        email: email,
        password: password,
      });
      localStorage.setItem('token', res.data.access_token);
      navigate('/home');
    } catch (err) {
      console.error(err);
      setErrorMessage('Login failed: Invalid email or password');
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
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
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
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          <button type="submit" className="login-button" disabled={isLoading}>
            {isLoading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AdminLoginForm;

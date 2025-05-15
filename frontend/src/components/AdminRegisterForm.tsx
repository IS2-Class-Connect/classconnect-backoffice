import { useState } from 'react';
import api from '../api/axios';
import '../styles/RegisterForm.css';
import { useNavigate } from 'react-router-dom';

function AdminRegisterForm() {
  const [username, setUsername] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setErrorMessage('');
    try {
      await api.post('/admins', {
        username,
        email,
        password,
      });
      navigate('/home');
    } catch (err: any) {
      console.error('Error response:', err.response);
        if (err.response && err.response.status === 400) {
            setErrorMessage('Registration failed: Invalid data');
        } else if (err.response && err.response.status === 409) {
            setErrorMessage('Registration failed: Email already exists');
        } else {
            setErrorMessage('Registration failed: An unexpected error occurred');
        }
    }
    setIsLoading(false);
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2 className="register-title">Register Admin</h2>
        <form onSubmit={handleRegister} className="register-form">
          <input
            type="text"
            className="register-input"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="email"
            className="register-input"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <input
            type="password"
            className="register-input"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {errorMessage && <div className="error-message">{errorMessage}</div>}
          <button type="submit" className="register-button" disabled={isLoading}>
            {isLoading ? 'Registering...' : 'Register'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default AdminRegisterForm;

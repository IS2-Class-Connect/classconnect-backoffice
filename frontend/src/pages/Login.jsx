import { Link } from 'react-router-dom';
import AdminLoginForm from '../components/AdminLoginForm';

export default function Login() {
  return (
    <div>
      <AdminLoginForm />
      <p>
        Don't have an account? <Link to="/register">Register here</Link>
      </p>
    </div>
  );
}
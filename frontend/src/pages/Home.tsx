import { Link } from 'react-router-dom';
import UserList from '../components/UserList';
import '../styles/Home.css';

export default function Home() {
  return (
    <div className="home-container">
      <UserList />
      <p>
        Register an Admin <Link to="/register">here</Link>
      </p>
    </div>
  );
}

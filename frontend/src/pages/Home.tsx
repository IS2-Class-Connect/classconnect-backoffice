import { Link } from 'react-router-dom';
import UserList from '../components/UserList';
import { ToastContainer } from 'react-toastify';
import '../styles/Home.css';
import 'react-toastify/dist/ReactToastify.css'
import Dashboards from './Dashboards';

export default function Home() {
  return (
    <div className="home-container">
    <Dashboards />
      <UserList />
      <p>
        Register an Admin <Link to="/register">here</Link>
      </p>
      <ToastContainer
        position="top-right"
        autoClose={2000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        pauseOnHover
        draggable
      />
    </div>
  );
}

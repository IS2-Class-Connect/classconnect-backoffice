import { useEffect, useState } from 'react';
import api from '../api/axios';
import '../styles/UserList.css';

const UserList = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersResponse = await api.get('/admins/users');
        setUsers(usersResponse.data);
        console.log(usersResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>User List</h1>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.uuid}>
              <td>{user.name}</td>
              <td>Active</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserList;
import { useEffect, useState } from 'react';
import api from '../api/axios';
import '../styles/UserList.css';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [admins, setAdmins] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersResponse = await api.get('/admin-backend/users');
        const adminsResponse = await api.get('admins');
        setAdmins(adminsResponse.data);
        setUsers(usersResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);
  const updateUserLockStatus = async (uuid, locked) => {
    try {
      await api.patch(`/admin-backend/users/${uuid}/lock-status`, { locked });
      setUsers((prevUsers) =>
        prevUsers.map((user) =>
          user.uuid === uuid ? { ...user, accountLockedByAdmins: locked } : user
        )
      );
    } catch (error) {
      console.error(`Failed to ${locked ? 'block' : 'unblock'} user:`, error);
    }
  };


  const formatActiveness = (isBlocked) => {
    return isBlocked ? 'Blocked' : 'Active';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  };

  return (
    <div>
      <h1>User Management</h1>
      <h2>Users</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Status</th>
            <th>Registration Date</th>
            <th>Actions</th> 
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.uuid}>
              <td>{user.name}</td>
              <td>{formatActiveness(user.accountLockedByAdmins)}</td>
              <td>{formatDate(user.createdAt)}</td>
              <td>
                {user.accountLockedByAdmins ? (
                  <button onClick={() => updateUserLockStatus(user.uuid,false)}>Unblock</button>
                ) : (
                  <button onClick={() => updateUserLockStatus(user.uuid,true)}>Block</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Admins</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Registration Date</th>
          </tr>
        </thead>
        <tbody>
          {admins.map((admin) => (
            <tr key={admin.id}>
              <td>{admin.username}</td>
              <td>{formatDate(admin.registration_date)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default UserList;

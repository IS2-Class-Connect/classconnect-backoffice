import { useEffect, useState } from 'react';
import api from '../api/axios';
import '../styles/UserList.css';

const UserList = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [admins, setAdmins] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersResponse = await api.get('/admins/users');
        const adminsResponse = await api.get('/admins');
        const adminsEnrollmentResponse = await api.get('/admins/courses/enrollments');

        const users = usersResponse.data;
        const enrollments = adminsEnrollmentResponse.data;

        const enrollmentsMap = new Map();

        enrollments.forEach(({ userId, role, course }) => {
          if (!enrollmentsMap.has(userId)) {
            enrollmentsMap.set(userId, []);
          }
          enrollmentsMap.get(userId).push({ role, course });
        });

        const usersWithEnrollments = users.map(user => ({
          ...user,
          enrollments: enrollmentsMap.get(user.uuid) || [],
        }));

        setAdmins(adminsResponse.data);
        setUsers(usersWithEnrollments);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);


  const updateUserLockStatus = async (uuid: string, locked: boolean) => {
    try {
      await api.patch(`/admins/users/${uuid}/lock-status`, { locked });
      setUsers((prevUsers: any[]) =>
        prevUsers.map((user) =>
          user.uuid === uuid ? { ...user, accountLockedByAdmins: locked } : user
        )
      );
    } catch (error) {
      console.error(`Failed to ${locked ? 'block' : 'unblock'} user:`, error);
    }
  };

  const updateUserRole = async (uuid: string, courseId: string, newRole: string) => {
    try {
      await api.patch(`/admins/courses/${courseId}/enrollments/${uuid}`, { role: newRole });
      setUsers((prevUsers) =>
        prevUsers.map((user) => {
          if (user.uuid === uuid) {
            return {
              ...user,
              enrollments: user.enrollments.map((enrollment) =>
                enrollment.course.id === courseId
                  ? { ...enrollment, role: newRole }
                  : enrollment
              ),
            };
          }
          return user;
        })
      );
    } catch (error) {
      console.error('Error updating user role:', error);
    }
  };

  const formatActiveness = (isBlocked: boolean) => {
    return isBlocked ? 'Blocked' : 'Active';
  };

  const formatDate = (dateString: string) => {
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
            <th>Courses</th>
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
                {user.enrollments && user.enrollments.length > 0 ? (
                  user.enrollments.map((enrollment) => (
                    <div key={enrollment.course.id} className="course-entry">
                      <span>{enrollment.course.title} - </span>
                      <select
                        value={enrollment.role}
                        onChange={(e) =>
                          updateUserRole(user.uuid, enrollment.course.id, e.target.value)
                        }
                      >
                        <option value="STUDENT">Student</option>
                        <option value="ASSISTANT">Assistant</option>
                      </select>
                    </div>
                  ))
                ) : (
                  <span>No enrollments available</span>
                )}
              </td>
              <td>
                {user.accountLockedByAdmins ? (
                  <button onClick={() => updateUserLockStatus(user.uuid, false)}>Unblock</button>
                ) : (
                  <button onClick={() => updateUserLockStatus(user.uuid, true)}>Block</button>
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

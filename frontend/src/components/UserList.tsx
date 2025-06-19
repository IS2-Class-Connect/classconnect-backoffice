import { useEffect, useState } from 'react';
import api from '../api/axios';
import '../styles/UserList.css';
import { toast } from 'react-toastify';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';
interface Course {
  id: string;
  title: string;
}

interface Enrollment {
  userId: string;
  role: string;
  course: Course;
}

interface User {
  uuid: string;
  name: string;
  email: string;
  enrollments: Enrollment[];
}

const UserList = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [admins, setAdmins] = useState<any[]>([]);
  const [confirmDialog, setConfirmDialog] = useState<{
    open: boolean;
    title: string;
    message: string;
    onConfirm: () => void;
    onCancel: () => void;
  }>({
    open: false,
    title: '',
    message: '',
    onConfirm: () => { },
    onCancel: () => { },
  });

  const navigate = useNavigate();
  const handleAddRules = () => {
    navigate('/rules'); 
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersResponse = await api.get('/admins/users');
        const adminsResponse = await api.get('/admins');
        const adminsEnrollmentResponse = await api.get('/admins/courses/enrollments');

        const users = usersResponse.data;
        const enrollments = adminsEnrollmentResponse.data;

        const enrollmentsMap = new Map();

        enrollments.forEach(({ userId, role, course }: Enrollment) => {
          if (!enrollmentsMap.has(userId)) {
            enrollmentsMap.set(userId, []);
          }
          enrollmentsMap.get(userId).push({ role, course });
        });

        const usersWithEnrollments = users.map((user: User) => ({
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
      const username = users.find((user) => user.uuid === uuid)?.name || '';
      const action = locked ? "block" : "unblock";
      setConfirmDialog({
        open: true,
        title: 'Confirm Action',
        message: `Are you sure you want to ${action} user ${username}?`,
        onConfirm: async () => {
          setConfirmDialog((prev) => ({ ...prev, open: false }));
          await api.patch(`/admins/users/${uuid}/lock-status`, { locked });

          setUsers((prevUsers: any[]) => prevUsers.map(
            (user) => {
              return user.uuid === uuid ? { ...user, accountLockedByAdmins: locked } : user;
            }
          ));

          toast.info(`${locked ? "Blocked" : "Unblocked"} user ${username}`)
        },
        onCancel: () => {
          setConfirmDialog((prev) => ({ ...prev, open: false }));
        },
      });
    } catch (error) {
      console.error(`Failed to ${locked ? 'block' : 'unblock'} user:`, error);
      toast.error(`Failed to ${locked ? "block" : "unblock"} user`);
    }
  };

  const updateUserRole = async (uuid: string, courseId: string, newRole: string) => {
    try {
      const username = users.find((user) => user.uuid === uuid)?.name || '';

      setConfirmDialog({
        open: true,
        title: 'Confirm Action',
        message: `Are you sure you want to set the role of ${username} to ${newRole.toLowerCase()} for this course?`,
        onConfirm: async () => {
          setConfirmDialog((prev) => ({ ...prev, open: false }));
          await api.patch(`/admins/courses/${courseId}/enrollments/${uuid}`, { role: newRole });

          setUsers((prevUsers) =>
            prevUsers.map((user) => {
              if (user.uuid === uuid) {
                return {
                  ...user,
                  enrollments: user.enrollments.map((enrollment: Enrollment) => (
                    enrollment.course.id === courseId
                      ? { ...enrollment, role: newRole }
                      : enrollment
                  )),
                };
              }
              return user;
            })
          );

          toast.success(`Updated role for ${username} to ${newRole.toLowerCase()}!`)
        },
        onCancel: () => {
          setConfirmDialog((prev) => ({ ...prev, open: false }));
        },
      });
    } catch (error) {
      console.error("Error updating user role:", error);
      toast.error("Error updating user role")
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
    <div className="top-actions">
      <Button className="add-rules-button" onClick={handleAddRules}>
        Add rules
      </Button>
    </div>

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
                  user.enrollments.map((enrollment: Enrollment) => (
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

      <ConfirmDialog
        open={confirmDialog.open}
        title={confirmDialog.title}
        message={confirmDialog.message}
        onConfirm={confirmDialog.onConfirm}
        onCancel={confirmDialog.onCancel}
      />
    </div>
  );
};

export function ConfirmDialog({ open, title, message, onConfirm, onCancel }: {
  open: boolean;
  title: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  return (
    <Dialog open={open} onClose={onCancel}>
      <DialogTitle>{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{message}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onCancel}>Cancel</Button>
        <Button onClick={onConfirm} color="primary" autoFocus>
          Confirm
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default UserList;

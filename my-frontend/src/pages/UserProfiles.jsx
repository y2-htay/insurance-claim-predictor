import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function UserProfiles() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem("access");
      const response = await axios.get("http://127.0.0.1:8001/api/user_profiles/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data);
    };

    fetchUsers();
  }, []);

  return (
    <div className="table-container">
      <h2>User Profiles</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Username</th></tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}><td>{user.id}</td><td>{user.username}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserProfiles;

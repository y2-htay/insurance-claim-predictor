import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function EndUsers() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const fetchUsers = async () => {
      const token = localStorage.getItem("access");
      try {
        const response = await axios.get("http://127.0.0.1:8001/api/end_users/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setUsers(response.data);
      } catch (error) {
        console.error("Error fetching End Users:", error);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div className="table-container">
      <h2>End Users</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.full_name || "N/A"}</td>
              <td>{user.email || "N/A"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EndUsers;

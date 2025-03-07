import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function Finance() {
  const [financeUsers, setFinanceUsers] = useState([]);

  useEffect(() => {
    const fetchFinanceUsers = async () => {
      const token = localStorage.getItem("access");
      const response = await axios.get("http://127.0.0.1:8001/api/finance/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setFinanceUsers(response.data);
    };

    fetchFinanceUsers();
  }, []);

  return (
    <div className="table-container">
      <h2>Finance Users</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th></tr>
        </thead>
        <tbody>
          {financeUsers.map(user => (
            <tr key={user.id}><td>{user.id}</td><td>{user.name}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Finance;

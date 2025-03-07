import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function Administrators() {
  const [admins, setAdmins] = useState([]);

  useEffect(() => {
    const fetchAdmins = async () => {
      const token = localStorage.getItem("access");
      const response = await axios.get("http://127.0.0.1:8001/api/administrators/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAdmins(response.data);
    };

    fetchAdmins();
  }, []);

  return (
    <div className="table-container">
      <h2>Administrators</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th></tr>
        </thead>
        <tbody>
          {admins.map(admin => (
            <tr key={admin.id}><td>{admin.id}</td><td>{admin.name}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Administrators;

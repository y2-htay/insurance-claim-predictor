import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function AiEngineers() {
  const [engineers, setEngineers] = useState([]);

  useEffect(() => {
    const fetchEngineers = async () => {
      const token = localStorage.getItem("access");
      const response = await axios.get("http://127.0.0.1:8001/api/ai_engineers/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setEngineers(response.data);
    };

    fetchEngineers();
  }, []);

  return (
    <div className="table-container">
      <h2>AI Engineers</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Name</th></tr>
        </thead>
        <tbody>
          {engineers.map(engineer => (
            <tr key={engineer.id}><td>{engineer.id}</td><td>{engineer.name}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AiEngineers;

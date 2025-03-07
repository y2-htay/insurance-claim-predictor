import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function ClaimTrainingData() {
  const [claims, setClaims] = useState([]);

  useEffect(() => {
    const fetchClaims = async () => {
      const token = localStorage.getItem("access");
      const response = await axios.get("http://127.0.0.1:8001/api/claim_training_data/", {
        headers: { Authorization: `Bearer ${token}` }
      });
      setClaims(response.data);
    };

    fetchClaims();
  }, []);

  return (
    <div className="table-container">
      <h2>Claim Training Data</h2>
      <table>
        <thead>
          <tr><th>ID</th><th>Description</th></tr>
        </thead>
        <tbody>
          {claims.map(claim => (
            <tr key={claim.id}><td>{claim.id}</td><td>{claim.description}</td></tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ClaimTrainingData;

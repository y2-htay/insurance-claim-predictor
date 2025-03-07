import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function VehicleTypes() {
  const [vehicleTypes, setVehicleTypes] = useState([]);

  useEffect(() => {
    const fetchVehicleTypes = async () => {
      try {
        const token = localStorage.getItem("access");
        const response = await axios.get("http://127.0.0.1:8001/api/vehicle_types/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setVehicleTypes(response.data);
      } catch (error) {
        console.error("Error fetching vehicle types:", error);
      }
    };

    fetchVehicleTypes();
  }, []);

  return (
    <div className="container">
      <h2>Vehicle Types</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {vehicleTypes.length > 0 ? (
            vehicleTypes.map(vehicle => (
              <tr key={vehicle.id}>
                <td>{vehicle.id}</td>
                <td>{vehicle.name}</td> {/* Changed from vehicle.type -> vehicle.name */}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="2">No Vehicle Types Available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default VehicleTypes;

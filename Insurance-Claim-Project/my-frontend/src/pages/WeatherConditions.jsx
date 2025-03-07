import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/table.css";

function WeatherConditions() {
  const [weatherConditions, setWeatherConditions] = useState([]);

  useEffect(() => {
    const fetchWeatherConditions = async () => {
      try {
        const token = localStorage.getItem("access");
        const response = await axios.get("http://127.0.0.1:8001/api/weather_conditions/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setWeatherConditions(response.data);
      } catch (error) {
        console.error("Error fetching weather conditions:", error);
      }
    };

    fetchWeatherConditions();
  }, []);

  return (
    <div className="container">
      <h2>Weather Conditions</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Condition</th>
          </tr>
        </thead>
        <tbody>
          {weatherConditions.length > 0 ? (
            weatherConditions.map(condition => (
              <tr key={condition.id}>
                <td>{condition.id}</td>
                <td>{condition.description}</td> {/* Changed from condition.name -> condition.description */}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="2">No Weather Conditions Available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default WeatherConditions;

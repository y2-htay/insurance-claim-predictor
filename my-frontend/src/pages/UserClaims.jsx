import { useEffect, useState } from "react";
import axios from "axios";
import "../styles/form.css";
import "../styles/table.css";

function UserClaims() {
  const [claims, setClaims] = useState([]);
  const [vehicleTypes, setVehicleTypes] = useState([]);
  const [weatherConditions, setWeatherConditions] = useState([]);
  
  // Define gender choices (from Django model)
  const genderChoices = [
    { id: "M", name: "Male" },
    { id: "F", name: "Female" },
    { id: "O", name: "Other" }
  ];

  const [formData, setFormData] = useState({
    vehicle_type: "",
    weather_condition: "",
    passengers_involved: "",
    psychological_injury: false,
    injury_prognosis_months: "",
    exceptional_circumstance: false,
    dominant_injury: "",
    whiplash: false,
    driver_age: "",
    vehicle_age: "",
    police_report: false,
    witness_present: false,
    gender: "",
    user: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Fetch Vehicle Types & Weather Conditions
  useEffect(() => {
    const token = localStorage.getItem("access");

    const fetchVehicleTypes = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8001/api/vehicle_types/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setVehicleTypes(response.data);
      } catch (error) {
        console.error("Error fetching Vehicle Types:", error);
      }
    };

    const fetchWeatherConditions = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8001/api/weather_conditions/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setWeatherConditions(response.data);
      } catch (error) {
        console.error("Error fetching Weather Conditions:", error);
      }
    };

    fetchVehicleTypes();
    fetchWeatherConditions();
  }, []);

  // Fetch user profile & store user ID instead of username
  useEffect(() => {
    const fetchUserProfile = async () => {
      const token = localStorage.getItem("access");
      try {
        const response = await axios.get("http://127.0.0.1:8001/api/auth/users/me/", {
          headers: { Authorization: `Bearer ${token}` }
        });
        setFormData(prevData => ({ ...prevData, user: response.data.username }));  // Save username instead of ID
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    };

    fetchUserProfile();
  }, []);

  // Fetch Existing Claims
  useEffect(() => {
    const fetchClaims = async () => {
      const token = localStorage.getItem("access");
      try {
        const response = await axios.get("http://127.0.0.1:8001/api/user_claims/", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setClaims(response.data);
      } catch (error) {
        console.error("Error fetching User Claims:", error);
      }
    };

    fetchClaims();
  }, []);

  // Handle form input change
  const handleChange = (e) => {
    const { name, type, value, checked } = e.target;
    setFormData({ ...formData, [name]: type === "checkbox" ? checked : value });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    const token = localStorage.getItem("access");

    try {
      const response = await axios.post("http://127.0.0.1:8001/api/user_claims/", formData, {
        headers: { 
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      setClaims([...claims, response.data]); // Add new claim to the list
      setSuccess("Claim submitted successfully!");
      setFormData({
        vehicle_type: "",
        weather_condition: "",
        passengers_involved: "",
        psychological_injury: false,
        injury_prognosis_months: "",
        exceptional_circumstance: false,
        dominant_injury: "",
        whiplash: false,
        driver_age: "",
        vehicle_age: "",
        police_report: false,
        witness_present: false,
        gender: "",
        user: formData.user, // Keep user field unchanged
      });
    } catch (error) {
      setError("Error submitting claim. Please try again.");
      console.error("Error submitting claim:", error.response?.data);
    }
  };

  return (
    <div className="container">
      <h2>User Claims</h2>

      {/* Claim Submission Form */}
      <div className="form-container">
        <h3>Submit a New Claim</h3>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}
        <form onSubmit={handleSubmit}>
          <label>User</label>
          <input type="text" name="user" value={formData.user} onChange={handleChange} required />

          <label>Vehicle Type</label>
<select name="vehicle_type" value={formData.vehicle_type} onChange={handleChange} required>
  <option value="">Select Vehicle Type</option>
  {vehicleTypes.map(vehicle => (
    <option key={vehicle.id} value={vehicle.id}>{vehicle.name}</option>  // Changed from vehicle.type -> vehicle.name
  ))}
</select>

<label>Weather Condition</label>
<select name="weather_condition" value={formData.weather_condition} onChange={handleChange} required>
  <option value="">Select Weather Condition</option>
  {weatherConditions.map(condition => (
    <option key={condition.id} value={condition.id}>{condition.description}</option>  // Changed from condition.name -> condition.description
  ))}
</select>

          <label>Passengers Involved</label>
          <input type="number" name="passengers_involved" value={formData.passengers_involved} onChange={handleChange} required />

          <label>Gender</label>
          <select name="gender" value={formData.gender} onChange={handleChange} required>
            <option value="">Select Gender</option>
            {genderChoices.map(gender => (
              <option key={gender.id} value={gender.id}>{gender.name}</option>
            ))}
          </select>

          <label>Psychological Injury</label>
          <input type="checkbox" name="psychological_injury" checked={formData.psychological_injury} onChange={handleChange} />

          <label>Injury Prognosis (Months)</label>
          <input type="number" name="injury_prognosis_months" value={formData.injury_prognosis_months} onChange={handleChange} required />

          <label>Dominant Injury</label>
          <input type="text" name="dominant_injury" value={formData.dominant_injury} onChange={handleChange} required />

          <label>Police Report</label>
          <input type="checkbox" name="police_report" checked={formData.police_report} onChange={handleChange} />

          <label>Witness Present</label>
          <input type="checkbox" name="witness_present" checked={formData.witness_present} onChange={handleChange} />

          <button type="submit" className="submit-button">Submit Claim</button>
        </form>
      </div>
    </div>
  );
}

export default UserClaims;

import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await axios.post("http://127.0.0.1:8001/api/auth/jwt/create/", {
        username,
        password
      });

      console.log("Login Response:", response.data); // Debugging output

      // Store tokens in localStorage
      localStorage.setItem("access", response.data.access);
      localStorage.setItem("refresh", response.data.refresh);

      console.log("Access Token Stored:", localStorage.getItem("access")); // Debugging output
      navigate("/dashboard");
    } catch (error) {
      console.error("Login error:", error.response?.data);
      setError("Invalid username or password");
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleLogin}>
        <input type="text" placeholder="Username" value={username} 
          onChange={(e) => setUsername(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} 
          onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default Login;

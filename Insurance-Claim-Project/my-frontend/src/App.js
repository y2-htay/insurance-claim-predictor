import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Login from "./pages/login";
import Dashboard from "./pages/Dashboard";
import UserProfiles from "./pages/UserProfiles";
import EndUsers from "./pages/EndUsers";
import AiEngineers from "./pages/AiEngineers";
import Finance from "./pages/Finance";
import Signup from "./pages/Signup";
import Administrators from "./pages/Administrators";
import VehicleTypes from "./pages/VehicleTypes";
import WeatherConditions from "./pages/WeatherConditions";
import ClaimTrainingData from "./pages/ClaimTrainingData";
import UserClaims from "./pages/UserClaims";
import ProtectedRoute from "./components/ProtectedRoute";
import "./styles/navbar.css";

function App() {
  return (
    <Router>
      <nav>
        <Link to="/login">Login</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/user-profiles">User Profiles</Link>
        <Link to="/end-users">End Users</Link>
        <Link to="/ai-engineers">AI Engineers</Link>
        <Link to="/finance">Finance</Link>
        <Link to="/administrators">Administrators</Link>
        <Link to="/vehicle-types">Vehicle Types</Link>
        <Link to="/weather-conditions">Weather Conditions</Link>
        <Link to="/claim-training-data">Claim Training Data</Link>
        <Link to="/user-claims">User Claims</Link>
      </nav>

      <Routes>
      <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/user-profiles" element={<ProtectedRoute><UserProfiles /></ProtectedRoute>} />
        <Route path="/end-users" element={<ProtectedRoute><EndUsers /></ProtectedRoute>} />
        <Route path="/ai-engineers" element={<ProtectedRoute><AiEngineers /></ProtectedRoute>} />
        <Route path="/finance" element={<ProtectedRoute><Finance /></ProtectedRoute>} />
        <Route path="/administrators" element={<ProtectedRoute><Administrators /></ProtectedRoute>} />
        <Route path="/vehicle-types" element={<ProtectedRoute><VehicleTypes /></ProtectedRoute>} />
        <Route path="/weather-conditions" element={<ProtectedRoute><WeatherConditions /></ProtectedRoute>} />
        <Route path="/claim-training-data" element={<ProtectedRoute><ClaimTrainingData /></ProtectedRoute>} />
        <Route path="/user-claims" element={<ProtectedRoute><UserClaims /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;

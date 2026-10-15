import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import Employees from "./pages/Employees";
import EmployeeProfile from "./pages/EmployeeProfile";
import CreateEmployee from "./pages/CreateEmployee";
import Departments from "./pages/Departments";
import CreateDepartment from "./pages/CreateDepartment";
import LeaveRequests from "./pages/LeaveRequests";
import { AuthProvider } from "./context/AuthContext";

const HR_ROLES = ["admin", "hr_manager"];

function App() {
    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/login" element={<Login />} />

                    <Route element={<ProtectedRoute />}>
                        <Route element={<Layout />}>
                            <Route path="/dashboard" element={<Dashboard />} />
                            <Route path="/leave-requests" element={<LeaveRequests />} />
                            <Route path="/employees" element={<Employees />} />
                            <Route path="/employees/:id" element={<EmployeeProfile />} />

                            <Route element={<ProtectedRoute allowedRoles={HR_ROLES} />}>
                                <Route path="/employees/new" element={<CreateEmployee />} />
                                <Route path="/departments" element={<Departments />} />
                                <Route path="/departments/new" element={<CreateDepartment />} />
                            </Route>
                        </Route>
                    </Route>

                    <Route path="*" element={<Navigate to="/login" replace />} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;
import {useEffect, useMemo, useState} from "react";
import {useNavigate} from "react-router-dom";
import {getEmployees} from "../api/employees";
import {getDepartments} from "../api/departments";
import {useAuth} from "../context/AuthContext";

function Employees() {
    const navigate = useNavigate();
    const {user} = useAuth();

    const [employees, setEmployees] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [error, setError] = useState("");
    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const [loading, setLoading] = useState(true);

    const canManageEmployees = ["admin", "hr_manager"].includes(user?.role);

    useEffect(() => {
        let active = true;

        async function loadData() {
            setLoading(true);
            setError("");

            try {
                const employeesData = await getEmployees();

                if (!active) return;

                setEmployees(Array.isArray(employeesData) ? employeesData : []);

                if (canManageEmployees) {
                    try {
                        const departmentsData = await getDepartments();

                        if (active) {
                            setDepartments(Array.isArray(departmentsData) ? departmentsData : []);
                        }
                    } catch {
                        if (active) {
                            setDepartments([]);
                        }
                    }
                } else {
                    setDepartments([]);
                }
            } catch (loadError) {
                if (active) {
                    setError(loadError.message || "Unable to load employees.");
                }
            } finally {
                if (active) {
                    setLoading(false);
                }
            }
        }

        if (user) {
            void loadData();
        }

        return () => {
            active = false;
        };
    }, [user, canManageEmployees]);

    const departmentById = useMemo(
        () => new Map(departments.map((department) => [department.id, department])),
        [departments],
    );

    function getDepartmentName(departmentId) {
        return departmentById.get(departmentId)?.name || "—";
    }

    function getInitials(employee) {
        return `${employee.first_name?.[0] || ""}${employee.last_name?.[0] || ""}`.toUpperCase();
    }

    const filteredEmployees = useMemo(() => {
        const normalizedSearch = search.trim().toLowerCase();

        return employees.filter((employee) => {
            const fullName = `${employee.first_name || ""} ${employee.last_name || ""}`.toLowerCase();
            const email = employee.email?.toLowerCase() || "";
            const position = employee.position?.toLowerCase() || "";
            const department = getDepartmentName(employee.department_id).toLowerCase();

            const matchesSearch =
                !normalizedSearch ||
                fullName.includes(normalizedSearch) ||
                email.includes(normalizedSearch) ||
                position.includes(normalizedSearch) ||
                department.includes(normalizedSearch);

            const matchesStatus = statusFilter === "all" || employee.status === statusFilter;

            return matchesSearch && matchesStatus;
        });
    }, [employees, search, statusFilter, departmentById]);

    if (loading) {
        return (
            <div className="employees-page">
                <div className="employees-header">
                    <div>
                        <h1>Employees</h1>
                        <p>Browse people across your organization</p>
                    </div>
                </div>
                <div className="employees-empty">
                    <strong>Loading employees...</strong>
                    <span>Please wait while we retrieve the employee directory.</span>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="employees-page">
                <div className="employees-header">
                    <div>
                        <h1>Employees</h1>
                        <p>Browse people across your organization</p>
                    </div>
                </div>
                <div className="form-error" role="alert">{error}</div>
            </div>
        );
    }

    return (
        <div className="employees-page">
            <div className="employees-header">
                <div>
                    <h1>Employees</h1>
                    <p>
                        {canManageEmployees
                            ? "Manage people across your organization"
                            : "Browse people across your organization"}
                    </p>
                </div>

                {canManageEmployees && (
                    <button
                        type="button"
                        className="primary-button"
                        onClick={() => navigate("/employees/new")}
                    >
                        + Add Employee
                    </button>
                )}
            </div>

            <div className="employees-toolbar">
                <div className="employees-search">
                    <svg
                        width="17"
                        height="17"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <circle cx="11" cy="11" r="7"/>
                        <path d="m20 20-4-4"/>
                    </svg>

                    <input
                        type="text"
                        placeholder="Search employees..."
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        aria-label="Search employees"
                    />
                </div>

                <select
                    className="employees-status-filter"
                    value={statusFilter}
                    onChange={(event) => setStatusFilter(event.target.value)}
                    aria-label="Filter employees by status"
                >
                    <option value="all">All statuses</option>
                    <option value="active">Active</option>
                    <option value="on_leave">On leave</option>
                    <option value="inactive">Inactive</option>
                </select>
            </div>

            <div className="employees-list-header">
                <span>
                    {filteredEmployees.length}{" "}
                    {filteredEmployees.length === 1 ? "employee" : "employees"}
                </span>
            </div>

            <div className="employees-table-container">
                <table className="employees-table">
                    <thead>
                    <tr>
                        <th>Employee</th>
                        <th>Position</th>
                        <th>Department</th>
                        <th>Status</th>
                    </tr>
                    </thead>

                    <tbody>
                    {filteredEmployees.map((employee) => (
                        <tr key={employee.id}>
                            <td>
                                <button
                                    type="button"
                                    className="employee-table-person"
                                    onClick={() => navigate(`/employees/${employee.id}`)}
                                >
                                        <span className="employee-table-avatar">
                                            {getInitials(employee)}
                                        </span>

                                    <span className="employee-table-person-info">
                                            <strong>
                                                {employee.first_name} {employee.last_name}
                                            </strong>
                                            <span>{employee.email}</span>
                                        </span>
                                </button>
                            </td>

                            <td>{employee.position || "—"}</td>
                            <td>{getDepartmentName(employee.department_id)}</td>
                            <td>
                                    <span className={`status-badge status-${employee.status}`}>
                                        {(employee.status || "unknown").replace("_", " ")}
                                    </span>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>

                {filteredEmployees.length === 0 && (
                    <div className="employees-empty">
                        <strong>No employees found</strong>
                        <span>
                            {search || statusFilter !== "all"
                                ? "Try changing your search or filters."
                                : "No employees are available to display."}
                        </span>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Employees;
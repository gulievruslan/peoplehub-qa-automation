import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
    deleteEmployee,
    getEmployee,
    getEmployees,
    updateEmployee,
} from "../api/employees";
import { getDepartments } from "../api/departments";
import { getCurrentUser } from "../api/auth";

function EmployeeProfile() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [employee, setEmployee] = useState(null);
    const [employees, setEmployees] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [user, setUser] = useState(null);
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState(null);
    const [error, setError] = useState("");
    const [saving, setSaving] = useState(false);
    const [deleting, setDeleting] = useState(false);

    useEffect(() => {
        async function loadData() {
            try {
                const [
                    employeeData,
                    employeesData,
                    departmentsData,
                    userData,
                ] = await Promise.all([
                    getEmployee(id),
                    getEmployees(),
                    getDepartments(),
                    getCurrentUser(),
                ]);

                setEmployee(employeeData);
                setEmployees(employeesData);
                setDepartments(departmentsData);
                setFormData(employeeData);
                setUser(userData);
            } catch (error) {
                setError(error.message);
            }
        }

        loadData();
    }, [id]);

    function getDepartmentName(departmentId) {
        const department = departments.find(
            (item) => item.id === departmentId,
        );

        return department?.name || "—";
    }

    function getManagerName(managerId) {
        const manager = employees.find(
            (item) => item.id === managerId,
        );

        if (!manager) {
            return "—";
        }

        return `${manager.first_name} ${manager.last_name}`;
    }

    function getInitials() {
        return `${employee.first_name?.[0] || ""}${employee.last_name?.[0] || ""}`.toUpperCase();
    }

    function getStatusLabel(status) {
        if (status === "on_leave") {
            return "On Leave";
        }

        if (status === "active") {
            return "Active";
        }

        if (status === "inactive") {
            return "Inactive";
        }

        return status || "Unknown";
    }

    function handleChange(event) {
        const { name, value } = event.target;

        setFormData((current) => ({
            ...current,
            [name]: value,
        }));
    }

    async function handleSave(event) {
        event.preventDefault();

        setError("");
        setSaving(true);

        try {
            const updatedEmployee = await updateEmployee(id, {
                first_name: formData.first_name,
                last_name: formData.last_name,
                email: formData.email,
                phone: formData.phone,
                position: formData.position,
                status: formData.status,
                department_id: Number(
                    formData.department_id,
                ),
                manager_id: formData.manager_id
                    ? Number(formData.manager_id)
                    : null,
            });

            setEmployee(updatedEmployee);
            setFormData(updatedEmployee);
            setEditing(false);
        } catch (error) {
            setError(error.message);
        } finally {
            setSaving(false);
        }
    }

    async function handleDelete() {
        const confirmed = window.confirm(
            "Are you sure you want to delete this employee?",
        );

        if (!confirmed) {
            return;
        }

        setError("");
        setDeleting(true);

        try {
            await deleteEmployee(id);
            navigate("/employees");
        } catch (error) {
            setError(error.message);
            setDeleting(false);
        }
    }

    if (error && !employee) {
        return <p>{error}</p>;
    }

    if (!employee || !formData || !user) {
        return <p>Loading...</p>;
    }

    const canEdit =
        user.role === "admin" ||
        user.role === "hr_manager";

    const canDelete = user.role === "admin";

    return (
        <div className="employee-profile-page">
            <div className="employee-profile-header">
                <div className="employee-profile-heading">
                    <button
                        className="employee-back-button"
                        onClick={() => navigate("/employees")}
                    >
                        ← Back to Employees
                    </button>

                    <div className="employee-profile-identity">
                        <div className="employee-profile-avatar">
                            {getInitials()}
                        </div>

                        <div>
                            <h1>
                                {employee.first_name}{" "}
                                {employee.last_name}
                            </h1>

                            <p>{employee.position}</p>
                        </div>
                    </div>
                </div>

                <div className="employee-profile-actions">
                    {!editing && canEdit && (
                        <button
                            className="secondary-button"
                            onClick={() => {
                                setEditing(true);
                                setError("");
                            }}
                        >
                            Edit
                        </button>
                    )}

                    {!editing && canDelete && (
                        <button
                            className="danger-button"
                            onClick={handleDelete}
                            disabled={deleting}
                        >
                            {deleting
                                ? "Deleting..."
                                : "Delete"}
                        </button>
                    )}
                </div>
            </div>

            {error && (
                <p className="form-error">
                    {error}
                </p>
            )}

            {editing ? (
                <form
                    className="employee-profile-card"
                    onSubmit={handleSave}
                >
                    <div className="employee-profile-card-header">
                        <div>
                            <h2>Edit Employee</h2>
                            <p>
                                Update employee information
                            </p>
                        </div>
                    </div>

                    <div className="employee-form-grid">
                        <div className="form-field">
                            <label htmlFor="first_name">
                                First Name
                            </label>

                            <input
                                id="first_name"
                                name="first_name"
                                value={formData.first_name}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="last_name">
                                Last Name
                            </label>

                            <input
                                id="last_name"
                                name="last_name"
                                value={formData.last_name}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="email">
                                Email
                            </label>

                            <input
                                id="email"
                                name="email"
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="phone">
                                Phone
                            </label>

                            <input
                                id="phone"
                                name="phone"
                                value={formData.phone || ""}
                                onChange={handleChange}
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="position">
                                Position
                            </label>

                            <input
                                id="position"
                                name="position"
                                value={formData.position}
                                onChange={handleChange}
                                required
                            />
                        </div>

                        <div className="form-field">
                            <label htmlFor="status">
                                Status
                            </label>

                            <select
                                id="status"
                                name="status"
                                value={formData.status}
                                onChange={handleChange}
                            >
                                <option value="active">
                                    Active
                                </option>

                                <option value="on_leave">
                                    On Leave
                                </option>

                                <option value="inactive">
                                    Inactive
                                </option>
                            </select>
                        </div>

                        <div className="form-field">
                            <label htmlFor="department_id">
                                Department
                            </label>

                            <select
                                id="department_id"
                                name="department_id"
                                value={
                                    formData.department_id || ""
                                }
                                onChange={handleChange}
                            >
                                <option value="">
                                    Select department
                                </option>

                                {departments.map(
                                    (department) => (
                                        <option
                                            key={department.id}
                                            value={department.id}
                                        >
                                            {department.name}
                                        </option>
                                    ),
                                )}
                            </select>
                        </div>

                        <div className="form-field">
                            <label htmlFor="manager_id">
                                Manager
                            </label>

                            <select
                                id="manager_id"
                                name="manager_id"
                                value={
                                    formData.manager_id || ""
                                }
                                onChange={handleChange}
                            >
                                <option value="">
                                    No manager
                                </option>

                                {employees
                                    .filter(
                                        (item) =>
                                            item.id !==
                                            employee.id,
                                    )
                                    .map((item) => (
                                        <option
                                            key={item.id}
                                            value={item.id}
                                        >
                                            {item.first_name}{" "}
                                            {item.last_name}
                                        </option>
                                    ))}
                            </select>
                        </div>
                    </div>

                    <div className="employee-form-actions">
                        <button
                            type="button"
                            className="secondary-button"
                            onClick={() => {
                                setFormData(employee);
                                setEditing(false);
                                setError("");
                            }}
                        >
                            Cancel
                        </button>

                        <button
                            type="submit"
                            className="primary-button"
                            disabled={saving}
                        >
                            {saving
                                ? "Saving..."
                                : "Save Changes"}
                        </button>
                    </div>
                </form>
            ) : (
                <div className="employee-profile-layout">
                    <div className="employee-profile-card">
                        <div className="employee-profile-card-header">
                            <div>
                                <h2>Employee Information</h2>
                                <p>
                                    Personal and professional
                                    details
                                </p>
                            </div>

                            <span
                                className={`status-badge status-${employee.status}`}
                            >
                                {getStatusLabel(
                                    employee.status,
                                )}
                            </span>
                        </div>

                        <div className="employee-profile-grid">
                            <div>
                                <span>First Name</span>
                                <strong>
                                    {employee.first_name}
                                </strong>
                            </div>

                            <div>
                                <span>Last Name</span>
                                <strong>
                                    {employee.last_name}
                                </strong>
                            </div>

                            <div>
                                <span>Email</span>
                                <strong>
                                    {employee.email}
                                </strong>
                            </div>

                            <div>
                                <span>Phone</span>
                                <strong>
                                    {employee.phone || "—"}
                                </strong>
                            </div>

                            <div>
                                <span>Position</span>
                                <strong>
                                    {employee.position}
                                </strong>
                            </div>

                            <div>
                                <span>Department</span>
                                <strong>
                                    {getDepartmentName(
                                        employee.department_id,
                                    )}
                                </strong>
                            </div>

                            <div>
                                <span>Manager</span>
                                <strong>
                                    {getManagerName(
                                        employee.manager_id,
                                    )}
                                </strong>
                            </div>
                        </div>
                    </div>

                    <div className="employee-profile-card employee-profile-summary">
                        <div className="employee-profile-card-header">
                            <div>
                                <h2>Overview</h2>
                                <p>
                                    Employment summary
                                </p>
                            </div>
                        </div>

                        <div className="employee-overview-item">
                            <span>Status</span>

                            <strong>
                                {getStatusLabel(
                                    employee.status,
                                )}
                            </strong>
                        </div>

                        <div className="employee-overview-item">
                            <span>Department</span>

                            <strong>
                                {getDepartmentName(
                                    employee.department_id,
                                )}
                            </strong>
                        </div>

                        <div className="employee-overview-item">
                            <span>Manager</span>

                            <strong>
                                {getManagerName(
                                    employee.manager_id,
                                )}
                            </strong>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

export default EmployeeProfile;
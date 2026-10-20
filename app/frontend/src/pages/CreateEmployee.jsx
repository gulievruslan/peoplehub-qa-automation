
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createEmployee } from "../api/employees";
import { createPayroll } from "../api/payroll";
import { useAuth } from "../context/AuthContext";

function CreateEmployee() {
  const navigate = useNavigate();
  const { user } = useAuth();
  const isHRManager = user?.role === "hr_manager";

  const [formData, setFormData] = useState({
    first_name: "",
    last_name: "",
    email: "",
    phone: "",
    position: "",
    status: "active",
    department_id: "",
    manager_id: "",
    salary: "",
  });

  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const [createdEmployee, setCreatedEmployee] = useState(null);

  function handleChange(event) {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (createdEmployee) {
      return;
    }

    setError("");
    setSaving(true);

    let employee;

    try {
      employee = await createEmployee({
        first_name: formData.first_name,
        last_name: formData.last_name,
        email: formData.email,
        phone: formData.phone || null,
        position: formData.position,
        status: formData.status,
        department_id: Number(formData.department_id),
        manager_id: formData.manager_id
          ? Number(formData.manager_id)
          : null,
      });
    } catch (error) {
      setError(error.message || "Failed to create employee.");
      setSaving(false);
      return;
    }

    if (isHRManager) {
      const now = new Date();

      try {
        await createPayroll({
          employee_id: employee.id,
          month: now.getMonth() + 1,
          year: now.getFullYear(),
          salary: Number(formData.salary),
          status: "pending",
        });
      } catch (error) {
        setCreatedEmployee(employee);
        setError(
          `Employee was created, but the salary record could not be created. ` +
            `Do not create the employee again. Details: ${error.message || "Unknown error"}`,
        );
        setSaving(false);
        return;
      }
    }

    navigate(`/employees/${employee.id}`);
  }

  return (
    <div className="employee-profile-page">
      <div className="employee-profile-header">
        <div>
          <h1>Add Employee</h1>
          <p>Create a new employee profile</p>
        </div>
      </div>

      {error && <p className="form-error">{error}</p>}

      {createdEmployee && (
        <div>
          <p>
            The employee profile exists, but the salary record was not saved.
            Open the employee profile and resolve the salary issue there.
          </p>
          <button
            type="button"
            className="primary-button"
            onClick={() => navigate(`/employees/${createdEmployee.id}`)}
          >
            Open Employee Profile
          </button>
        </div>
      )}

      <form className="employee-profile-card" onSubmit={handleSubmit}>
        <h2>Employee Information</h2>

        <div className="employee-form-grid">
          <div className="form-field">
            <label htmlFor="first_name">First Name</label>
            <input
              id="first_name"
              name="first_name"
              value={formData.first_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="last_name">Last Name</label>
            <input
              id="last_name"
              name="last_name"
              value={formData.last_name}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="email">Email</label>
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
            <label htmlFor="phone">Phone</label>
            <input
              id="phone"
              name="phone"
              value={formData.phone}
              onChange={handleChange}
            />
          </div>

          <div className="form-field">
            <label htmlFor="position">Position</label>
            <input
              id="position"
              name="position"
              value={formData.position}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="status">Status</label>
            <select
              id="status"
              name="status"
              value={formData.status}
              onChange={handleChange}
            >
              <option value="active">Active</option>
              <option value="on_leave">On Leave</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>

          <div className="form-field">
            <label htmlFor="department_id">Department ID</label>
            <input
              id="department_id"
              name="department_id"
              type="number"
              min="1"
              value={formData.department_id}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="manager_id">Manager ID</label>
            <input
              id="manager_id"
              name="manager_id"
              type="number"
              min="1"
              value={formData.manager_id}
              onChange={handleChange}
            />
          </div>

          {isHRManager && (
            <div className="form-field">
              <label htmlFor="salary">Monthly Salary</label>
              <input
                id="salary"
                name="salary"
                type="number"
                min="0.01"
                step="0.01"
                value={formData.salary}
                onChange={handleChange}
                required
              />
            </div>
          )}
        </div>

        <div className="employee-form-actions">
          <button
            type="button"
            className="secondary-button"
            onClick={() => navigate("/employees")}
          >
            Cancel
          </button>

          {!createdEmployee && (
            <button
              type="submit"
              className="primary-button"
              disabled={saving}
            >
              {saving ? "Creating..." : "Create Employee"}
            </button>
          )}
        </div>
      </form>
    </div>
  );
}

export default CreateEmployee;

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createDepartment } from "../api/departments";

function CreateDepartment() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    setError("");
    setSaving(true);

    try {
      await createDepartment({
        name,
      });

      navigate("/departments");
    } catch (error) {
      setError(error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="employee-profile-page">
      <div className="employee-profile-header">
        <div>
          <h1>Add Department</h1>
          <p>Create a new department</p>
        </div>
      </div>

      {error && (
        <p className="form-error">
          {error}
        </p>
      )}

      <form
        className="employee-profile-card"
        onSubmit={handleSubmit}
      >
        <h2>Department Information</h2>

        <div className="form-field">
          <label htmlFor="name">
            Department Name
          </label>

          <input
            id="name"
            name="name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
          />
        </div>

        <div className="employee-form-actions">
          <button
            type="button"
            className="secondary-button"
            onClick={() => navigate("/departments")}
          >
            Cancel
          </button>

          <button
            type="submit"
            className="primary-button"
            disabled={saving}
          >
            {saving ? "Creating..." : "Create Department"}
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreateDepartment;
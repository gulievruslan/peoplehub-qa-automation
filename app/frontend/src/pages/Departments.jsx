import {useEffect, useState} from "react";
import {useNavigate} from "react-router-dom";
import {
    deleteDepartment,
    getDepartments,
    updateDepartment,
} from "../api/departments";
import {getCurrentUser} from "../api/auth";

function Departments() {
    const [departments, setDepartments] = useState([]);
    const [error, setError] = useState("");
    const [editingId, setEditingId] = useState(null);
    const [editingName, setEditingName] = useState("");
    const [user, setUser] = useState(null);
    const [search, setSearch] = useState("");

    const navigate = useNavigate();

    useEffect(() => {
        async function loadDepartments() {
            try {
                const data = await getDepartments();
                setDepartments(data);
            } catch (error) {
                setError(error.message);
            }
        }

        async function loadUser() {
            try {
                const data = await getCurrentUser();
                setUser(data);
            } catch (error) {
                setError(error.message);
            }
        }

        loadDepartments();
        loadUser();
    }, []);

    async function handleUpdate(departmentId) {
        const trimmedName = editingName.trim();

        if (!trimmedName) {
            setError("Department name cannot be empty.");
            return;
        }

        setError("");

        try {
            await updateDepartment(departmentId, {
                name: trimmedName,
            });

            setDepartments((currentDepartments) =>
                currentDepartments.map((department) =>
                    department.id === departmentId
                        ? {
                            ...department,
                            name: trimmedName,
                        }
                        : department,
                ),
            );

            setEditingId(null);
            setEditingName("");
        } catch (error) {
            setError(error.message);
        }
    }

    async function handleDelete(departmentId) {
        const confirmed = window.confirm(
            "Are you sure you want to delete this department?",
        );

        if (!confirmed) {
            return;
        }

        setError("");

        try {
            await deleteDepartment(departmentId);

            setDepartments((currentDepartments) =>
                currentDepartments.filter(
                    (department) =>
                        department.id !== departmentId,
                ),
            );
        } catch (error) {
            setError(error.message);
        }
    }

    if (!user) {
        return <p>Loading...</p>;
    }

    const canEdit =
        user.role === "admin" ||
        user.role === "hr_manager";

    const canDelete = user.role === "admin";

    const canManageDepartments =
        canEdit || canDelete;

    const filteredDepartments = departments.filter(
        (department) =>
            department.name
                ?.toLowerCase()
                .includes(search.trim().toLowerCase()),
    );

    return (
        <div className="departments-page">
            <div className="departments-header">
                <div>
                    <h1>Departments</h1>
                    <p>
                        Manage departments across your organization
                    </p>
                </div>

                {canEdit && (
                    <button
                        className="primary-button"
                        onClick={() =>
                            navigate("/departments/new")
                        }
                    >
                        + Add Department
                    </button>
                )}
            </div>

            {error && (
                <p className="form-error">
                    {error}
                </p>
            )}

            <div className="departments-toolbar">
                <div className="departments-search">
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
                        placeholder="Search departments..."
                        value={search}
                        onChange={(event) =>
                            setSearch(event.target.value)
                        }
                    />
                </div>

                <span>
        {filteredDepartments.length}{" "}
                    {filteredDepartments.length === 1
                        ? "department"
                        : "departments"}
    </span>
            </div>

            <div className="departments-table-container">
                <table className="departments-table">
                    <thead>
                    <tr>
                        <th>Department</th>

                        {canManageDepartments && (
                            <th>Actions</th>
                        )}
                    </tr>
                    </thead>

                    <tbody>
                    {filteredDepartments.map((department) => (
                        <tr key={department.id}>
                            <td>
                                {editingId === department.id ? (
                                    <input
                                        className="department-edit-input"
                                        value={editingName}
                                        onChange={(event) =>
                                            setEditingName(
                                                event.target.value,
                                            )
                                        }
                                        onKeyDown={(event) => {
                                            if (
                                                event.key ===
                                                "Enter"
                                            ) {
                                                handleUpdate(
                                                    department.id,
                                                );
                                            }

                                            if (
                                                event.key ===
                                                "Escape"
                                            ) {
                                                setEditingId(null);
                                                setEditingName("");
                                                setError("");
                                            }
                                        }}
                                        autoFocus
                                    />
                                ) : (
                                    <div className="department-name">
                                            <span className="department-avatar">
                                                {department.name
                                                    ?.charAt(0)
                                                    .toUpperCase()}
                                            </span>

                                        <strong>
                                            {department.name}
                                        </strong>
                                    </div>
                                )}
                            </td>

                            {canManageDepartments && (
                                <td>
                                    {editingId === department.id ? (
                                        <div className="department-actions">
                                            <button
                                                className="primary-button"
                                                onClick={() =>
                                                    handleUpdate(
                                                        department.id,
                                                    )
                                                }
                                            >
                                                Save
                                            </button>

                                            <button
                                                className="secondary-button"
                                                onClick={() => {
                                                    setEditingId(
                                                        null,
                                                    );
                                                    setEditingName(
                                                        "",
                                                    );
                                                    setError("");
                                                }}
                                            >
                                                Cancel
                                            </button>
                                        </div>
                                    ) : (
                                        <div className="department-actions">
                                            {canEdit && (
                                                <button
                                                    className="secondary-button"
                                                    onClick={() => {
                                                        setEditingId(
                                                            department.id,
                                                        );
                                                        setEditingName(
                                                            department.name,
                                                        );
                                                        setError("");
                                                    }}
                                                >
                                                    Edit
                                                </button>
                                            )}

                                            {canDelete && (
                                                <button
                                                    className="danger-button"
                                                    onClick={() =>
                                                        handleDelete(
                                                            department.id,
                                                        )
                                                    }
                                                >
                                                    Delete
                                                </button>
                                            )}
                                        </div>
                                    )}
                                </td>
                            )}
                        </tr>
                    ))}
                    </tbody>
                </table>

                {departments.length === 0 && (
                    <div className="departments-empty">
                        <strong>No departments yet</strong>

                        <span>
                            Create your first department to get
                            started.
                        </span>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Departments;
import {useCallback, useEffect, useMemo, useState} from "react";
import {getEmployees} from "../api/employees";
import {
    createLeaveRequest,
    deleteLeaveRequest,
    getLeaveRequests,
    updateLeaveRequest,
} from "../api/leaveRequests";
import {useAuth} from "../context/AuthContext";

const HR_ROLES = ["admin", "hr_manager"];

const STATUS_LABELS = {
    pending: "Pending",
    approved: "Approved",
    rejected: "Rejected",
};

const EMPTY_FORM = {
    employee_id: "",
    start_date: "",
    end_date: "",
    reason: "",
};

function formatDate(value) {
    if (!value) return "—";

    const date = new Date(`${value}`.slice(0, 10) + "T00:00:00");

    return date.toLocaleDateString("en-US", {
        month: "short",
        day: "2-digit",
        year: "numeric",
    });
}

function getEmployeeName(employee) {
    if (!employee) return "Unknown employee";

    return (
        [employee.first_name, employee.last_name].filter(Boolean).join(" ") ||
        `Employee #${employee.id}`
    );
}

function getErrorMessage(error) {
    return error?.message || "Something went wrong. Please try again.";
}

function LeaveRequests() {
    const {user} = useAuth();
    const isEmployee = user?.role === "employee";
    const isAdmin = user?.role === "admin";
    const canManageRequests = HR_ROLES.includes(user?.role);

    const [requests, setRequests] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] = useState("all");
    const [formOpen, setFormOpen] = useState(false);
    const [editingRequest, setEditingRequest] = useState(null);
    const [form, setForm] = useState(EMPTY_FORM);

    const employeeById = useMemo(
        () => new Map(employees.map((employee) => [employee.id, employee])),
        [employees],
    );

    const loadData = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const requestsPromise = getLeaveRequests();
            const employeesPromise = canManageRequests ? getEmployees() : Promise.resolve([]);
            const [requestsData, employeesData] = await Promise.all([
                requestsPromise,
                employeesPromise,
            ]);

            setRequests(Array.isArray(requestsData) ? requestsData : []);
            setEmployees(Array.isArray(employeesData) ? employeesData : []);
        } catch (loadError) {
            setError(getErrorMessage(loadError));
        } finally {
            setLoading(false);
        }
    }, [canManageRequests]);

    useEffect(() => {
        loadData();
    }, [loadData]);

    const filteredRequests = useMemo(() => {
        const normalizedSearch = search.trim().toLowerCase();

        return requests.filter((request) => {
            const employeeName = isEmployee
                ? "My request"
                : getEmployeeName(employeeById.get(request.employee_id));

            const matchesStatus = statusFilter === "all" || request.status === statusFilter;
            const matchesSearch =
                !normalizedSearch ||
                [employeeName, request.reason, String(request.id)].some((value) =>
                    String(value || "").toLowerCase().includes(normalizedSearch),
                );

            return matchesStatus && matchesSearch;
        });
    }, [requests, employeeById, search, statusFilter, isEmployee]);

    const counts = useMemo(
        () => ({
            total: requests.length,
            pending: requests.filter((request) => request.status === "pending").length,
            approved: requests.filter((request) => request.status === "approved").length,
            rejected: requests.filter((request) => request.status === "rejected").length,
        }),
        [requests],
    );

    function openCreateForm() {
        if (isEmployee && !user?.employee_id) {
            setError("Your account is not linked to an employee record. Please contact HR.");
            return;
        }

        setEditingRequest(null);
        setForm({
            ...EMPTY_FORM,
            employee_id: isEmployee ? String(user.employee_id) : "",
        });
        setError("");
        setSuccess("");
        setFormOpen(true);
    }

    function openEditForm(request) {
        setEditingRequest(request);
        setForm({
            employee_id: String(request.employee_id),
            start_date: String(request.start_date).slice(0, 10),
            end_date: String(request.end_date).slice(0, 10),
            reason: request.reason || "",
        });
        setError("");
        setSuccess("");
        setFormOpen(true);
    }

    function closeForm() {
        if (saving) return;

        setFormOpen(false);
        setEditingRequest(null);
        setForm(EMPTY_FORM);
    }

    function handleFormChange(event) {
        const {name, value} = event.target;
        setForm((current) => ({...current, [name]: value}));
    }

    async function handleSubmit(event) {
        event.preventDefault();

        if (saving) return;

        setError("");
        setSuccess("");

        if (isEmployee && !user?.employee_id) {
            setError("Your account is not linked to an employee record. Please contact HR.");
            return;
        }

        if (!form.start_date || !form.end_date) {
            setError("Please select both leave dates.");
            return;
        }

        if (form.start_date > form.end_date) {
            setError("The start date must be before or equal to the end date.");
            return;
        }

        if (!editingRequest && !isEmployee && !form.employee_id) {
            setError("Please select an employee.");
            return;
        }

        const payload = {
            start_date: form.start_date,
            end_date: form.end_date,
            reason: form.reason.trim(),
        };

        if (!editingRequest) {
            payload.employee_id = Number(isEmployee ? user.employee_id : form.employee_id);
        }

        setSaving(true);

        try {
            if (editingRequest) {
                await updateLeaveRequest(editingRequest.id, payload);
            } else {
                await createLeaveRequest(payload);
            }

            setFormOpen(false);
            setEditingRequest(null);
            setForm(EMPTY_FORM);
            setSuccess(
                editingRequest
                    ? "Leave request updated successfully."
                    : "Leave request submitted successfully.",
            );

            await loadData();
        } catch (submitError) {
            setError(getErrorMessage(submitError));
        } finally {
            setSaving(false);
        }
    }

    async function handleStatusChange(request, status) {
        if (saving) return;

        setError("");
        setSuccess("");
        setSaving(true);

        try {
            await updateLeaveRequest(request.id, {status});
            setSuccess(`Request #${request.id} marked as ${STATUS_LABELS[status].toLowerCase()}.`);
            await loadData();
        } catch (updateError) {
            setError(getErrorMessage(updateError));
        } finally {
            setSaving(false);
        }
    }

    async function handleDelete(request) {
        if (saving) return;

        const action = isAdmin ? "permanently delete" : "cancel";
        const confirmed = window.confirm(
            `Are you sure you want to ${action} leave request #${request.id}?`,
        );

        if (!confirmed) return;

        setError("");
        setSuccess("");
        setSaving(true);

        try {
            await deleteLeaveRequest(request.id);
            setSuccess(
                isAdmin
                    ? "Leave request deleted successfully."
                    : "Leave request cancelled successfully.",
            );
            await loadData();
        } catch (deleteError) {
            setError(getErrorMessage(deleteError));
        } finally {
            setSaving(false);
        }
    }

    function renderActions(request) {
        const isPending = request.status === "pending";
        const canEdit = isPending && (isEmployee || canManageRequests);
        const canCancel = isEmployee && isPending;
        const canDelete = isAdmin;

        if (!canEdit && !canCancel && !canDelete && !(canManageRequests && isPending)) {
            return <span className="leave-no-actions">No actions</span>;
        }

        return (
            <div className="leave-actions">
                {canManageRequests && isPending && (
                    <>
                        <button
                            type="button"
                            className="leave-action-button leave-approve-button"
                            onClick={() => handleStatusChange(request, "approved")}
                            disabled={saving}
                        >
                            Approve
                        </button>
                        <button
                            type="button"
                            className="leave-action-button leave-reject-button"
                            onClick={() => handleStatusChange(request, "rejected")}
                            disabled={saving}
                        >
                            Reject
                        </button>
                    </>
                )}

                {canEdit && (
                    <button
                        type="button"
                        className="leave-action-button"
                        onClick={() => openEditForm(request)}
                        disabled={saving}
                    >
                        Edit
                    </button>
                )}

                {(canCancel || canDelete) && (
                    <button
                        type="button"
                        className="leave-action-button leave-delete-button"
                        onClick={() => handleDelete(request)}
                        disabled={saving}
                    >
                        {canDelete ? "Delete" : "Cancel"}
                    </button>
                )}
            </div>
        );
    }

    return (
        <div className="leave-requests-page">
            <div className="leave-requests-header">
                <div>
                    <h1>Leave Requests</h1>
                    <p>
                        {isEmployee
                            ? "Manage your time-off requests."
                            : "Review and manage employee time-off requests."}
                    </p>
                </div>

                <button type="button" className="primary-button" onClick={openCreateForm}>
                    + New Request
                </button>
            </div>

            {error && <div className="form-error" role="alert">{error}</div>}
            {success && <div className="leave-success" role="status">{success}</div>}

            <div className="leave-summary-grid">
                <button
                    type="button"
                    className={`leave-summary-card ${statusFilter === "all" ? "selected" : ""}`}
                    onClick={() => setStatusFilter("all")}
                >
                    <span>Total Requests</span>
                    <strong>{counts.total}</strong>
                </button>
                <button
                    type="button"
                    className={`leave-summary-card ${statusFilter === "pending" ? "selected" : ""}`}
                    onClick={() => setStatusFilter("pending")}
                >
                    <span>Pending</span>
                    <strong>{counts.pending}</strong>
                </button>
                <button
                    type="button"
                    className={`leave-summary-card ${statusFilter === "approved" ? "selected" : ""}`}
                    onClick={() => setStatusFilter("approved")}
                >
                    <span>Approved</span>
                    <strong>{counts.approved}</strong>
                </button>
                <button
                    type="button"
                    className={`leave-summary-card ${statusFilter === "rejected" ? "selected" : ""}`}
                    onClick={() => setStatusFilter("rejected")}
                >
                    <span>Rejected</span>
                    <strong>{counts.rejected}</strong>
                </button>
            </div>

            <div className="leave-toolbar">
                <div className="employees-search">
                    <svg
                        width="17"
                        height="17"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                    >
                        <circle cx="11" cy="11" r="7"/>
                        <path d="m20 20-4-4"/>
                    </svg>
                    <input
                        type="search"
                        value={search}
                        onChange={(event) => setSearch(event.target.value)}
                        placeholder={isEmployee ? "Search your requests..." : "Search employee, reason or ID..."}
                        aria-label="Search leave requests"
                    />
                </div>

                <select
                    className="employees-status-filter"
                    value={statusFilter}
                    onChange={(event) => setStatusFilter(event.target.value)}
                    aria-label="Filter by status"
                >
                    <option value="all">All statuses</option>
                    <option value="pending">Pending</option>
                    <option value="approved">Approved</option>
                    <option value="rejected">Rejected</option>
                </select>
            </div>

            <div className="employees-list-header">
                <span>
                    {loading
                        ? "Loading requests..."
                        : `${filteredRequests.length} request${filteredRequests.length === 1 ? "" : "s"} found`}
                </span>
                <button
                    type="button"
                    className="leave-refresh-button"
                    onClick={loadData}
                    disabled={loading || saving}
                >
                    Refresh
                </button>
            </div>

            <div className="leave-table-container">
                {loading ? (
                    <div className="leave-empty">
                        <strong>Loading requests</strong>
                        <span>Please wait while we retrieve the latest data.</span>
                    </div>
                ) : filteredRequests.length === 0 ? (
                    <div className="leave-empty">
                        <strong>No leave requests found</strong>
                        <span>
                            {search || statusFilter !== "all"
                                ? "Try changing your search or filters."
                                : "Create a request when you need time off."}
                        </span>
                    </div>
                ) : (
                    <table className="leave-table">
                        <thead>
                        <tr>
                            <th>Employee</th>
                            <th>Leave Period</th>
                            <th>Reason</th>
                            <th>Duration</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        {filteredRequests.map((request) => {
                            const employee = employeeById.get(request.employee_id);
                            const employeeName = isEmployee
                                ? "My request"
                                : getEmployeeName(employee);
                            const employeeInitials = employeeName
                                .split(" ")
                                .map((part) => part[0])
                                .join("")
                                .slice(0, 2)
                                .toUpperCase();
                            const start = new Date(
                                `${request.start_date}`.slice(0, 10) + "T00:00:00",
                            );
                            const end = new Date(
                                `${request.end_date}`.slice(0, 10) + "T00:00:00",
                            );
                            const duration = Math.round((end - start) / 86400000) + 1;

                            return (
                                <tr key={request.id}>
                                    <td>
                                        <div className="leave-employee-cell">
                                            <div className="employee-table-avatar">
                                                {employeeInitials}
                                            </div>
                                            <div>
                                                <strong>{employeeName}</strong>
                                                <span>Request #{request.id}</span>
                                            </div>
                                        </div>
                                    </td>
                                    <td>
                                        <div className="leave-period-cell">
                                            <strong>{formatDate(request.start_date)}</strong>
                                            <span>to {formatDate(request.end_date)}</span>
                                        </div>
                                    </td>
                                    <td>
                                            <span className="leave-reason">
                                                {request.reason || "—"}
                                            </span>
                                    </td>
                                    <td>
                                        {duration} {duration === 1 ? "day" : "days"}
                                    </td>
                                    <td>
                                            <span
                                                className={`leave-status-badge leave-status-${request.status}`}
                                            >
                                                {STATUS_LABELS[request.status] || request.status}
                                            </span>
                                    </td>
                                    <td>{renderActions(request)}</td>
                                </tr>
                            );
                        })}
                        </tbody>
                    </table>
                )}
            </div>

            {formOpen && (
                <div
                    className="leave-modal-backdrop"
                    onMouseDown={(event) => {
                        if (event.target === event.currentTarget && !saving) closeForm();
                    }}
                >
                    <section
                        className="leave-modal"
                        role="dialog"
                        aria-modal="true"
                        aria-labelledby="leave-modal-title"
                    >
                        <div className="leave-modal-header">
                            <div>
                                <h2 id="leave-modal-title">
                                    {editingRequest ? "Edit Leave Request" : "New Leave Request"}
                                </h2>
                                <p>
                                    {editingRequest
                                        ? "Update the dates or reason for this request."
                                        : "Enter the details for the requested time off."}
                                </p>
                            </div>
                            <button
                                type="button"
                                className="leave-modal-close"
                                onClick={closeForm}
                                disabled={saving}
                                aria-label="Close form"
                            >
                                ×
                            </button>
                        </div>

                        <form onSubmit={handleSubmit}>
                            {!isEmployee && !editingRequest && (
                                <div className="form-field">
                                    <label htmlFor="leave-employee">Employee</label>
                                    <select
                                        id="leave-employee"
                                        name="employee_id"
                                        value={form.employee_id}
                                        onChange={handleFormChange}
                                        required
                                    >
                                        <option value="">Select an employee</option>
                                        {employees.map((employee) => (
                                            <option key={employee.id} value={employee.id}>
                                                {getEmployeeName(employee)}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            )}

                            <div className="leave-form-date-grid">
                                <div className="form-field">
                                    <label htmlFor="leave-start-date">Start date</label>
                                    <input
                                        id="leave-start-date"
                                        type="date"
                                        name="start_date"
                                        value={form.start_date}
                                        onChange={handleFormChange}
                                        max={form.end_date || undefined}
                                        required
                                    />
                                </div>
                                <div className="form-field">
                                    <label htmlFor="leave-end-date">End date</label>
                                    <input
                                        id="leave-end-date"
                                        type="date"
                                        name="end_date"
                                        value={form.end_date}
                                        onChange={handleFormChange}
                                        min={form.start_date || undefined}
                                        required
                                    />
                                </div>
                            </div>

                            <div className="form-field leave-reason-field">
                                <label htmlFor="leave-reason">Reason</label>
                                <textarea
                                    id="leave-reason"
                                    name="reason"
                                    value={form.reason}
                                    onChange={handleFormChange}
                                    placeholder="Add a short explanation..."
                                    rows="4"
                                    maxLength="1000"
                                />
                            </div>

                            {error && <div className="form-error" role="alert">{error}</div>}

                            <div className="leave-modal-actions">
                                <button
                                    type="button"
                                    className="secondary-button"
                                    onClick={closeForm}
                                    disabled={saving}
                                >
                                    Cancel
                                </button>
                                <button type="submit" className="primary-button" disabled={saving}>
                                    {saving
                                        ? "Saving..."
                                        : editingRequest
                                            ? "Save Changes"
                                            : "Submit Request"}
                                </button>
                            </div>
                        </form>
                    </section>
                </div>
            )}
        </div>
    );
}

export default LeaveRequests;
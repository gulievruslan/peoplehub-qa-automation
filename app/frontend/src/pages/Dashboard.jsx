
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getDashboard, getMyDashboard } from "../api/dashboard";
import { getEmployees } from "../api/employees";
import { getLeaveRequests } from "../api/leaveRequests";
import {
    getPayrolls,
    getPayrollByEmployee,
    getPayrollHistory,
    getPayrollSummary,
} from "../api/payroll";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
    const { user } = useAuth();
    const navigate = useNavigate();

    const [dashboard, setDashboard] = useState(null);
    const [myDashboard, setMyDashboard] = useState(null);
    const [myPayrolls, setMyPayrolls] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [leaveRequests, setLeaveRequests] = useState([]);
    const [payrollSummary, setPayrollSummary] = useState(null);
    const [payrollHistory, setPayrollHistory] = useState([]);
    const [payrollByEmployee, setPayrollByEmployee] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        if (!user) {
            return;
        }

        let active = true;

        async function loadDashboard() {
            setError("");

            try {
                if (user.role === "employee") {
                    const [dashboardData, payrollData] =
                        await Promise.all([
                            getMyDashboard(),
                            getPayrolls(),
                        ]);

                    if (!active) return;

                    setMyDashboard(dashboardData);
                    setMyPayrolls(payrollData.items ?? []);
                    return;
                }

                const [
                    dashboardData,
                    employeesData,
                    leaveRequestsData,
                    payrollSummaryData,
                    payrollHistoryData,
                    payrollByEmployeeData,
                ] = await Promise.all([
                    getDashboard(),
                    getEmployees(),
                    getLeaveRequests(),
                    getPayrollSummary(),
                    getPayrollHistory(),
                    getPayrollByEmployee(),
                ]);

                if (!active) return;

                setDashboard(dashboardData);
                setEmployees(employeesData);
                setLeaveRequests(leaveRequestsData);
                setPayrollSummary(payrollSummaryData);
                setPayrollHistory(payrollHistoryData);
                setPayrollByEmployee(payrollByEmployeeData);
            } catch (error) {
                if (active) {
                    setError(error.message);
                }
            }
        }

        loadDashboard();

        return () => {
            active = false;
        };
    }, [user]);

    if (error) {
        return <p>{error}</p>;
    }

    // Personal dashboard for employees
    if (user?.role === "employee") {
        if (!myDashboard) {
            return <p>Loading...</p>;
        }

        const paidPayrolls = myPayrolls.filter(
            (payroll) => payroll.status === "paid",
        );

        const totalPaid = paidPayrolls.reduce(
            (total, payroll) => total + Number(payroll.salary),
            0,
        );

        const latestPayroll = myPayrolls[0];

        return (
            <div className="dashboard-page">
                <div className="dashboard-header">
                    <h2>Dashboard</h2>
                </div>

                <div className="dashboard-top-grid">
                    <div className="dashboard-card">
                        <div className="dashboard-card-top">
                            <span>Total Leave Requests</span>
                        </div>
                        <strong>
                            {myDashboard.total_leave_requests}
                        </strong>
                        <small>Your submitted requests</small>
                    </div>

                    <div className="dashboard-card">
                        <div className="dashboard-card-top">
                            <span>Pending Requests</span>
                        </div>
                        <strong>
                            {myDashboard.pending_leave_requests}
                        </strong>
                        <small>Awaiting a decision</small>
                    </div>

                    <div className="dashboard-card">
                        <div className="dashboard-card-top">
                            <span>Approved Requests</span>
                        </div>
                        <strong>
                            {myDashboard.approved_leave_requests}
                        </strong>
                        <small>Approved leave requests</small>
                    </div>
                </div>

                <div className="dashboard-top-grid">
                    <div className="dashboard-card">
                        <div className="dashboard-card-top">
                            <span>Latest Salary</span>
                        </div>
                        <strong>
                            {latestPayroll
                                ? `$${Number(
                                      latestPayroll.salary,
                                  ).toLocaleString("en-US", {
                                      minimumFractionDigits: 2,
                                      maximumFractionDigits: 2,
                                  })}`
                                : "—"}
                        </strong>
                        <small>
                            {latestPayroll
                                ? new Date(
                                      latestPayroll.year,
                                      latestPayroll.month - 1,
                                      1,
                                  ).toLocaleDateString("en-US", {
                                      month: "long",
                                      year: "numeric",
                                  })
                                : "No payroll records yet"}
                        </small>
                    </div>

                    <div className="dashboard-card">
                        <div className="dashboard-card-top">
                            <span>Total Paid</span>
                        </div>
                        <strong>
                            $
                            {totalPaid.toLocaleString("en-US", {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2,
                            })}
                        </strong>
                        <small>Across recorded paid payrolls</small>
                    </div>

                    <div className="dashboard-card">
                        <div className="dashboard-card-top">
                            <span>Payroll Records</span>
                        </div>
                        <strong>{myPayrolls.length}</strong>
                        <small>
                            {myPayrolls.filter(
                                (payroll) => payroll.status === "pending",
                            ).length}{" "}
                            pending payments
                        </small>
                    </div>
                </div>

                <div className="dashboard-panel salary-panel">
                    <div className="dashboard-panel-header">
                        <div>
                            <h2>My Payroll</h2>
                            <p>Your salary and payment history</p>
                        </div>
                    </div>

                    {myPayrolls.length === 0 ? (
                        <p>No payroll records available yet.</p>
                    ) : (
                        <div className="salary-by-employee-list">
                            {myPayrolls.map((payroll) => (
                                <div
                                    className="salary-by-employee-row"
                                    key={payroll.id}
                                >
                                    <div className="salary-employee-info">
                                        <strong>
                                            {new Date(
                                                payroll.year,
                                                payroll.month - 1,
                                                1,
                                            ).toLocaleDateString("en-US", {
                                                month: "long",
                                                year: "numeric",
                                            })}
                                        </strong>
                                    </div>

                                    <strong className="salary-value">
                                        $
                                        {Number(
                                            payroll.salary,
                                        ).toLocaleString("en-US", {
                                            minimumFractionDigits: 2,
                                            maximumFractionDigits: 2,
                                        })}
                                    </strong>

                                    <span
                                        className={
                                            payroll.status === "paid"
                                                ? "dashboard-approved"
                                                : "dashboard-pending"
                                        }
                                    >
                                        {payroll.status === "paid"
                                            ? "Paid"
                                            : payroll.status}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        );
    }

    // Corporate dashboard for ADMIN and HR_MANAGER
    if (!dashboard || !payrollSummary) {
        return <p>Loading...</p>;
    }

    const pendingLeaveRequests = leaveRequests.filter(
        (leaveRequest) => leaveRequest.status === "pending",
    ).length;

    const approvedLeaveRequests = leaveRequests.filter(
        (leaveRequest) => leaveRequest.status === "approved",
    ).length;

    const totalLeaveRequests = leaveRequests.length;

    const payrollMonth = new Date(
        payrollSummary.year,
        payrollSummary.month - 1,
        1,
    ).toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
    });

    const payrollCompletion = Math.round(
        payrollSummary.completion_percentage,
    );

    const totalPayroll = payrollSummary.total_payroll;
    const averageSalary = payrollSummary.average_salary;

    const rawMaxPayroll = Math.max(
        ...payrollHistory.map((payroll) => payroll.total_payroll),
        1,
    );

    const chartMaxPayroll = Math.ceil(rawMaxPayroll / 5000) * 5000;
    const chartStep = chartMaxPayroll / 4;

    const maxEmployeeSalary = Math.max(
        ...payrollByEmployee.map((payroll) => payroll.salary),
        1,
    );

    return (
        <div className="dashboard-page">
            <div className="dashboard-header">
                <h2>Dashboard</h2>
            </div>

            <div className="dashboard-top-grid">
                <div className="dashboard-card dashboard-employees-card">
                    <div className="dashboard-card-top">
                        <span>Total Employees</span>
                        <span className="dashboard-card-icon">
                            <svg
                                width="17"
                                height="17"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
                                <circle cx="9" cy="7" r="4" />
                                <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
                                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                            </svg>
                        </span>
                    </div>

                    <strong>{dashboard.total_employees}</strong>

                    <div className="employee-status-summary">
                        <div>
                            <span className="status-dot status-dot-active"></span>
                            <span>Active</span>
                            <strong>{dashboard.active_employees}</strong>
                        </div>
                        <div>
                            <span className="status-dot status-dot-leave"></span>
                            <span>On Leave</span>
                            <strong>{dashboard.on_leave_employees}</strong>
                        </div>
                        <div>
                            <span className="status-dot status-dot-inactive"></span>
                            <span>Inactive</span>
                            <strong>{dashboard.inactive_employees}</strong>
                        </div>
                    </div>
                </div>

                <div className="dashboard-card">
                    <div className="dashboard-card-top">
                        <span>Leave Requests</span>
                        <span className="dashboard-card-icon">
                            <svg
                                width="17"
                                height="17"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <rect x="3" y="4" width="18" height="17" rx="2" />
                                <line x1="16" y1="2" x2="16" y2="6" />
                                <line x1="8" y1="2" x2="8" y2="6" />
                                <line x1="3" y1="10" x2="21" y2="10" />
                                <path d="M8 14h2" />
                                <path d="M14 14h2" />
                                <path d="M8 18h2" />
                            </svg>
                        </span>
                    </div>

                    <strong>{totalLeaveRequests}</strong>

                    <small>
                        <span className="dashboard-pending">
                            {pendingLeaveRequests} pending
                        </span>
                        {" · "}
                        <span className="dashboard-approved">
                            {approvedLeaveRequests} approved
                        </span>
                    </small>
                </div>

                <div className="dashboard-card">
                    <div className="dashboard-card-top">
                        <span>Payroll Completion</span>
                        <span className="dashboard-card-icon">
                            <svg
                                width="17"
                                height="17"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="1.8"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <rect x="2" y="5" width="20" height="14" rx="2" />
                                <line x1="2" y1="10" x2="22" y2="10" />
                                <circle cx="12" cy="15" r="2.5" />
                                <path d="M12 13.5v3" />
                                <path d="M10.5 15h3" />
                            </svg>
                        </span>
                    </div>

                    <strong>{payrollCompletion}%</strong>

                    <div className="dashboard-progress">
                        <div className="dashboard-progress-bar">
                            <div
                                className="dashboard-progress-value"
                                style={{ width: `${payrollCompletion}%` }}
                            ></div>
                        </div>
                        <small>{payrollMonth} payroll</small>
                    </div>
                </div>
            </div>

            <div className="dashboard-main-grid">
                <div className="dashboard-left-column">
                    <div className="dashboard-panel payroll-panel">
                        <div className="dashboard-panel-header">
                            <div>
                                <h2>Payroll Overview</h2>
                                <p>Monthly payroll expenses</p>
                            </div>
                            <span className="dashboard-period">
                                {payrollMonth}
                            </span>
                        </div>

                        <div className="payroll-chart">
                            <div className="chart-y-axis">
                                <span>
                                    ${(chartMaxPayroll / 1000).toLocaleString()}k
                                </span>
                                <span>
                                    ${((chartStep * 3) / 1000).toLocaleString()}k
                                </span>
                                <span>
                                    ${((chartStep * 2) / 1000).toLocaleString()}k
                                </span>
                                <span>
                                    ${(chartStep / 1000).toLocaleString()}k
                                </span>
                                <span>$0</span>
                            </div>

                            <div className="chart-area">
                                <div className="chart-grid-line"></div>
                                <div className="chart-grid-line"></div>
                                <div className="chart-grid-line"></div>
                                <div className="chart-grid-line"></div>

                                <div className="chart-bars">
                                    {payrollHistory.map((payroll) => {
                                        const height =
                                            (payroll.total_payroll /
                                                chartMaxPayroll) *
                                            100;

                                        const monthLabel = new Date(
                                            payroll.year,
                                            payroll.month - 1,
                                            1,
                                        ).toLocaleDateString("en-US", {
                                            month: "short",
                                        });

                                        const isCurrentMonth =
                                            payroll.month === payrollSummary.month &&
                                            payroll.year === payrollSummary.year;

                                        return (
                                            <div
                                                className="chart-bar-wrapper"
                                                key={`${payroll.year}-${payroll.month}`}
                                            >
                                                <div
                                                    className={
                                                        isCurrentMonth
                                                            ? "chart-bar chart-bar-current"
                                                            : "chart-bar"
                                                    }
                                                    style={{ height: `${height}%` }}
                                                ></div>
                                                <span>{monthLabel}</span>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>

                        <div className="payroll-summary">
                            <div>
                                <span>Total payroll</span>
                                <strong>
                                    ${totalPayroll.toLocaleString("en-US")}
                                </strong>
                            </div>
                            <div>
                                <span>Employees paid</span>
                                <strong>{payrollSummary.employees_paid}</strong>
                            </div>
                            <div>
                                <span>Average salary</span>
                                <strong>
                                    ${averageSalary.toLocaleString("en-US")}
                                </strong>
                            </div>
                        </div>
                    </div>

                    <div className="dashboard-panel salary-panel">
                        <div className="dashboard-panel-header">
                            <div>
                                <h2>Salary by Employee</h2>
                                <p>Current month salaries</p>
                            </div>
                            <span className="dashboard-period">
                                {payrollMonth}
                            </span>
                        </div>

                        <div className="salary-by-employee-list">
                            {payrollByEmployee.map((payroll) => (
                                <div
                                    className="salary-by-employee-row"
                                    key={payroll.employee_id}
                                >
                                    <div className="salary-employee-info">
                                        <strong>{payroll.employee_name}</strong>
                                    </div>

                                    <div className="salary-bar-wrapper">
                                        <div
                                            className="salary-bar"
                                            style={{
                                                width: `${
                                                    (payroll.salary /
                                                        maxEmployeeSalary) *
                                                    100
                                                }%`,
                                            }}
                                        ></div>
                                    </div>

                                    <strong className="salary-value">
                                        ${payroll.salary.toLocaleString("en-US")}
                                    </strong>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="dashboard-panel status-panel">
                    <div className="dashboard-panel-header">
                        <div>
                            <h2>Employee Status</h2>
                            <p>Current employee activity</p>
                        </div>

                        <button
                            className="dashboard-link-button"
                            onClick={() => navigate("/employees")}
                        >
                            View all
                        </button>
                    </div>

                    <div className="employee-status-list">
                        {employees.map((employee) => {
                            const approvedLeave = leaveRequests.find(
                                (leaveRequest) =>
                                    leaveRequest.employee_id === employee.id &&
                                    leaveRequest.status === "approved",
                            );

                            const initials =
                                `${employee.first_name[0]}${employee.last_name[0]}`.toUpperCase();

                            const statusLabel = approvedLeave
                                ? "On leave"
                                : employee.status === "inactive"
                                  ? "Inactive"
                                  : "Active";

                            const statusClass =
                                statusLabel === "Active"
                                    ? "status-active-text"
                                    : "";

                            return (
                                <div
                                    className="employee-status-row"
                                    key={employee.id}
                                >
                                    <div className="employee-avatar">
                                        {initials}
                                    </div>

                                    <div className="employee-status-info">
                                        <strong>
                                            {employee.first_name}{" "}
                                            {employee.last_name}
                                        </strong>
                                        <span className={statusClass}>
                                            {statusLabel}
                                        </span>
                                    </div>

                                    <div className="employee-status-date">
                                        {approvedLeave ? (
                                            <>
                                                <span>Until</span>
                                                <strong>
                                                    {new Date(
                                                        approvedLeave.end_date,
                                                    ).toLocaleDateString(
                                                        "en-US",
                                                        {
                                                            month: "short",
                                                            day: "2-digit",
                                                        },
                                                    )}
                                                </strong>
                                            </>
                                        ) : (
                                            <>
                                                <span>Status</span>
                                                <strong>
                                                    {employee.status === "active"
                                                        ? "Working"
                                                        : "Not active"}
                                                </strong>
                                            </>
                                        )}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Dashboard;

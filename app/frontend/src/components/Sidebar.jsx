import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Sidebar() {
    const { user } = useAuth();

    const canManageEmployees = ["admin", "hr_manager"].includes(user?.role);

    return (
        <aside className="sidebar">
            <div className="sidebar-logo">
                <div className="sidebar-logo-mark">
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                        <circle cx="16" cy="8" r="4" fill="white" />
                        <circle cx="8" cy="16" r="4" fill="white" />
                        <circle cx="24" cy="16" r="4" fill="white" />
                        <path d="M16 12V24" stroke="white" strokeWidth="3" strokeLinecap="round" />
                        <path
                            d="M10.5 18.5L16 24L21.5 18.5"
                            stroke="white"
                            strokeWidth="3"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        />
                    </svg>
                </div>

                <span className="sidebar-logo-text">PeopleHub</span>
            </div>

            <nav className="sidebar-nav">
                <NavLink to="/dashboard" className="sidebar-link">
                    <svg
                        className="sidebar-link-icon"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <rect x="3" y="3" width="7" height="7" rx="1" />
                        <rect x="14" y="3" width="7" height="7" rx="1" />
                        <rect x="3" y="14" width="7" height="7" rx="1" />
                        <rect x="14" y="14" width="7" height="7" rx="1" />
                    </svg>
                    <span>Dashboard</span>
                </NavLink>

                <NavLink to="/leave-requests" className="sidebar-link">
                    <svg
                        className="sidebar-link-icon"
                        width="18"
                        height="18"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <rect x="3" y="5" width="18" height="16" rx="2" />
                        <path d="M16 3v4M8 3v4M3 11h18" />
                        <path d="m9 16 2 2 4-4" />
                    </svg>
                    <span>Leave Requests</span>
                </NavLink>

                <NavLink to="/employees" className="sidebar-link">
                    <svg
                        className="sidebar-link-icon"
                        width="18"
                        height="18"
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
                    <span>Employees</span>
                </NavLink>

                {canManageEmployees && (
                    <NavLink to="/departments" className="sidebar-link">
                        <svg
                            className="sidebar-link-icon"
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <rect x="3" y="3" width="7" height="7" rx="1" />
                            <rect x="14" y="3" width="7" height="7" rx="1" />
                            <path d="M6.5 10v4" />
                            <path d="M17.5 10v4" />
                            <path d="M6.5 14h11" />
                            <rect x="3" y="14" width="7" height="7" rx="1" />
                            <rect x="14" y="14" width="7" height="7" rx="1" />
                        </svg>
                        <span>Departments</span>
                    </NavLink>
                )}
            </nav>
        </aside>
    );
}

export default Sidebar;
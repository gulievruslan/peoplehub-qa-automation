import {useEffect, useRef, useState} from "react";
import {useNavigate} from "react-router-dom";
import {getCurrentUser} from "../api/auth";
import {
    getNotifications,
    getUnreadNotificationsCount,
    markAllNotificationsAsRead,
    markNotificationAsRead,
} from "../api/notifications";

function Header() {
    const [user, setUser] = useState(null);
    const [notifications, setNotifications] = useState([]);
    const [notificationsOpen, setNotificationsOpen] =
        useState(false);
    const [unreadCount, setUnreadCount] = useState(0);
    const notificationRef = useRef(null);

    const navigate = useNavigate();

    useEffect(() => {
        async function loadUser() {
            try {
                const data = await getCurrentUser();
                setUser(data);
            } catch (error) {
                console.error(error);
            }
        }

        loadUser();
    }, []);

    useEffect(() => {
        function handleClickOutside(event) {
            if (
                notificationRef.current &&
                !notificationRef.current.contains(event.target)
            ) {
                setNotificationsOpen(false);
            }
        }

        document.addEventListener(
            "mousedown",
            handleClickOutside
        );

        return () => {
            document.removeEventListener(
                "mousedown",
                handleClickOutside
            );
        };
    }, []);

    useEffect(() => {
        if (!user) {
            return;
        }

        async function loadNotifications() {
            try {
                const [
                    notificationsData,
                    unreadData,
                ] = await Promise.all([
                    getNotifications(),
                    getUnreadNotificationsCount(),
                ]);

                setNotifications(notificationsData);
                setUnreadCount(unreadData.count);
            } catch (error) {
                console.error(error);
            }
        }

        loadNotifications();
    }, [user]);

    function handleLogout() {
        localStorage.removeItem("access_token");
        navigate("/login");
    }

    async function handleNotificationsClick() {
        setNotificationsOpen((current) => !current);
    }

    async function handleNotificationClick(notificationId) {
        try {
            await markNotificationAsRead(notificationId);

            setNotifications((current) =>
                current.map((notification) =>
                    notification.id === notificationId
                        ? {
                            ...notification,
                            is_read: true,
                        }
                        : notification
                )
            );

            setUnreadCount((current) =>
                Math.max(current - 1, 0)
            );
        } catch (error) {
            console.error(error);
        }
    }

    async function handleMarkAllAsRead() {
        try {
            await markAllNotificationsAsRead();

            setNotifications((current) =>
                current.map((notification) => ({
                    ...notification,
                    is_read: true,
                }))
            );

            setUnreadCount(0);
        } catch (error) {
            console.error(error);
        }
    }

    return (
        <header className="app-header">
            <div className="header-user">
                {user && (
                    <>
                        <div
                            className="notification-wrapper"
                            ref={notificationRef}
                        >
                            <button
                                className="notification-button"
                                type="button"
                                onClick={
                                    handleNotificationsClick
                                }
                            >
                                <svg
                                    width="19"
                                    height="19"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    strokeWidth="1.8"
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                >
                                    <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9"/>
                                    <path d="M10 21h4"/>
                                </svg>

                                {unreadCount > 0 && (
                                    <span className="notification-badge">
                                        {unreadCount}
                                    </span>
                                )}
                            </button>

                            {notificationsOpen && (
                                <div className="notifications-dropdown">
                                    <div className="notifications-header">
                                        <strong>
                                            Notifications
                                        </strong>

                                        <span>
                                            {unreadCount} new
                                        </span>
                                    </div>

                                    {notifications.length ===
                                    0 ? (
                                        <div className="notification-empty">
                                            No notifications
                                        </div>
                                    ) : (
                                        notifications.map(
                                            (notification) => (
                                                <button
                                                    key={
                                                        notification.id
                                                    }
                                                    className={`notification-item ${
                                                        notification.is_read
                                                            ? "read"
                                                            : ""
                                                    }`}
                                                    type="button"
                                                    onClick={() =>
                                                        handleNotificationClick(
                                                            notification.id
                                                        )
                                                    }
                                                >
                                                    {!notification.is_read && (
                                                        <span className="notification-dot"/>
                                                    )}

                                                    <div>
                                                        <strong>
                                                            {
                                                                notification.title
                                                            }
                                                        </strong>

                                                        <p>
                                                            {
                                                                notification.message
                                                            }
                                                        </p>

                                                        <span>
                                                            {new Date(
                                                                notification.created_at
                                                            ).toLocaleString()}
                                                        </span>
                                                    </div>
                                                </button>
                                            )
                                        )
                                    )}

                                    {unreadCount > 0 && (
                                        <button
                                            className="notifications-footer"
                                            type="button"
                                            onClick={
                                                handleMarkAllAsRead
                                            }
                                        >
                                            Mark all as read
                                        </button>
                                    )}
                                </div>
                            )}
                        </div>

                        <div className="header-user-info">
                            <strong>{user.email}</strong>
                            <span>{user.role}</span>
                        </div>

                        <button
                            className="logout-button"
                            onClick={handleLogout}
                        >
                            Logout
                        </button>
                    </>
                )}
            </div>
        </header>
    );
}

export default Header;
import { apiRequest } from "./client";

export async function getNotifications() {
    return apiRequest("/api/notifications");
}

export async function getUnreadNotificationsCount() {
    return apiRequest(
        "/api/notifications/unread-count"
    );
}

export async function markNotificationAsRead(
    notificationId
) {
    return apiRequest(
        `/api/notifications/${notificationId}/read`,
        {
            method: "PATCH",
        },
    );
}

export async function markAllNotificationsAsRead() {
    return apiRequest(
        "/api/notifications/read-all",
        {
            method: "PATCH",
        },
    );
}
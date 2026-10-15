import { apiRequest } from "./client";

export async function getLeaveRequests() {
    return apiRequest("/api/leave-requests");
}

export async function getLeaveRequest(leaveRequestId) {
    return apiRequest(`/api/leave-requests/${leaveRequestId}`);
}

export async function updateLeaveRequest(leaveRequestId, leaveRequestData) {
    return apiRequest(`/api/leave-requests/${leaveRequestId}`, {
        method: "PATCH",
        body: JSON.stringify(leaveRequestData),
    });
}

export async function createLeaveRequest(leaveRequestData) {
    return apiRequest("/api/leave-requests", {
        method: "POST",
        body: JSON.stringify(leaveRequestData),
    });
}

export async function deleteLeaveRequest(leaveRequestId) {
    return apiRequest(`/api/leave-requests/${leaveRequestId}`, {
        method: "DELETE",
    });
}
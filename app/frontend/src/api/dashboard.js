import { apiRequest } from "./client";

export async function getDashboard() {
    return apiRequest("/api/dashboard");
}

export async function getMyDashboard() {
    return apiRequest("/api/dashboard/me");
}
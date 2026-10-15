import { apiRequest } from "./client";

export async function login(email, password) {
    return apiRequest(
        "/api/auth/login",
        {
            method: "POST",
            body: JSON.stringify({
                email,
                password,
            }),
            handleUnauthorized: false,
        },
    );
}

export async function getCurrentUser() {
    return apiRequest(
        "/api/auth/me",
    );
}
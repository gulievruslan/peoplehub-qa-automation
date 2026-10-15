const API_URL = "http://127.0.0.1:8000";

function getErrorMessage(data) {
    if (typeof data === "string") {
        return data;
    }

    if (typeof data?.detail === "string") {
        return data.detail;
    }

    if (Array.isArray(data?.detail)) {
        return data.detail
            .map((item) => {
                const location = Array.isArray(item.loc) ? item.loc.join(".") : "";
                const message = item.msg || "Validation error";

                return location ? `${location}: ${message}` : message;
            })
            .join("; ");
    }

    if (typeof data?.message === "string") {
        return data.message;
    }

    return "Request failed";
}

export async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem("access_token");
    const { handleUnauthorized = true, ...fetchOptions } = options;

    const headers = {
        ...fetchOptions.headers,
    };

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    if (fetchOptions.body && !headers["Content-Type"]) {
        headers["Content-Type"] = "application/json";
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...fetchOptions,
        headers,
    });

    if (response.status === 401 && handleUnauthorized) {
        localStorage.removeItem("access_token");
        window.location.href = "/login";

        throw new Error("Session expired");
    }

    const contentType = response.headers.get("content-type");
    const responseText = await response.text();

    let data = null;

    if (responseText) {
        if (contentType?.includes("application/json")) {
            try {
                data = JSON.parse(responseText);
            } catch {
                throw new Error("Invalid JSON response from server");
            }
        } else {
            data = responseText;
        }
    }

    if (!response.ok) {
        throw new Error(getErrorMessage(data));
    }

    return data;
}
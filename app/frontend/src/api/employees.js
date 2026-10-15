import { apiRequest } from "./client";

export async function getEmployees() {
    return apiRequest("/api/employees");
}

export async function getEmployee(employeeId) {
    return apiRequest(
        `/api/employees/${employeeId}`,
    );
}

export async function updateEmployee(
    employeeId,
    employeeData,
) {
    return apiRequest(
        `/api/employees/${employeeId}`,
        {
            method: "PUT",
            body: JSON.stringify(employeeData),
        },
    );
}

export async function createEmployee(employeeData) {
    return apiRequest(
        "/api/employees",
        {
            method: "POST",
            body: JSON.stringify(employeeData),
        },
    );
}

export async function deleteEmployee(employeeId) {
    return apiRequest(
        `/api/employees/${employeeId}`,
        {
            method: "DELETE",
        },
    );
}
import { apiRequest } from "./client";

export async function getDepartments() {
    return apiRequest("/api/departments");
}

export async function createDepartment(
    departmentData,
) {
    return apiRequest(
        "/api/departments",
        {
            method: "POST",
            body: JSON.stringify(departmentData),
        },
    );
}

export async function updateDepartment(
    departmentId,
    departmentData,
) {
    return apiRequest(
        `/api/departments/${departmentId}`,
        {
            method: "PUT",
            body: JSON.stringify(departmentData),
        },
    );
}

export async function deleteDepartment(
    departmentId,
) {
    return apiRequest(
        `/api/departments/${departmentId}`,
        {
            method: "DELETE",
        },
    );
}
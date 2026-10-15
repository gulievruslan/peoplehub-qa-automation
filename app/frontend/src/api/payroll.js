import { apiRequest } from "./client";

export async function getPayrolls() {
    return apiRequest("/api/payroll");
}

export async function getPayrollSummary() {
    return apiRequest("/api/payroll/summary");
}

export async function getPayrollHistory() {
    return apiRequest("/api/payroll/history");
}

export async function getPayrollByEmployee() {
    return apiRequest("/api/payroll/by-employee");
}

export async function getPayroll(payrollId) {
    return apiRequest(
        `/api/payroll/${payrollId}`,
    );
}

export async function createPayroll(
    payrollData,
) {
    return apiRequest(
        "/api/payroll",
        {
            method: "POST",
            body: JSON.stringify(payrollData),
        },
    );
}

export async function updatePayroll(
    payrollId,
    payrollData,
) {
    return apiRequest(
        `/api/payroll/${payrollId}`,
        {
            method: "PATCH",
            body: JSON.stringify(payrollData),
        },
    );
}

export async function deletePayroll(
    payrollId,
) {
    return apiRequest(
        `/api/payroll/${payrollId}`,
        {
            method: "DELETE",
        },
    );
}
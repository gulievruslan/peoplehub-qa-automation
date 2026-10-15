"""API client for PeopleHub leave request endpoints."""
from datetime import datetime
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse
from automation.dto.schema.leave_requests_models import (
    LeaveRequestData,
    LeaveRequestListResponse,
    LeaveRequestStatus,
)


class LeaveRequests(Base):
    """API client for PeopleHub leave request endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the leave requests API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/leave-requests"

    def get_leave_requests(self) -> CustomResponse[LeaveRequestListResponse, InvalidCredentialsResponse]:
        """Get the leave requests list."""
        return self.request(
            method="GET",
            url=self.url,
            response_model=LeaveRequestListResponse,
            response_error_model=InvalidCredentialsResponse,
        )

    def post_leave_request(
        self,
        employee_id: int,
        start_date: str,
        end_date: str,
        reason: str | None = None,
    ) -> CustomResponse[LeaveRequestData, InvalidCredentialsResponse]:
        """Create a leave request.

        Args:
            employee_id: ID of the employee requesting leave.
            start_date: Start date and time of the leave.
            end_date: End date and time of the leave.
            reason: Optional reason for the leave request.
        """
        return self.request(
            method="POST",
            url=self.url,
            json={"employee_id": employee_id, "start_date": start_date, "end_date": end_date, "reason": reason},
            response_model=LeaveRequestData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_leave_request_by_id(
        self,
        leave_request_id: int,
    ) -> CustomResponse[LeaveRequestData, InvalidCredentialsResponse]:
        """Get a leave request by ID.

        Args:
            leave_request_id: ID of the leave request to retrieve.
        """
        return self.request(
            method="GET",
            url=f"{self.url}/{leave_request_id}",
            response_model=LeaveRequestData,
            response_error_model=InvalidCredentialsResponse,
        )

    def update_leave_request(
        self,
        leave_request_id: int,
        start_date: str | None = None,
        end_date: str | None = None,
        reason: str | None = None,
        status: LeaveRequestStatus | None = None,
    ) -> CustomResponse[LeaveRequestData, InvalidCredentialsResponse]:
        """Update a leave request.

        Arguments left as None are not sent in the request.

        Args:
            leave_request_id: ID of the leave request to update.
            start_date: Updated start date and time.
            end_date: Updated end date and time.
            reason: Updated reason for leave.
            status: Updated leave request status.
        """
        return self.request(
            method="PATCH",
            url=f"{self.url}/{leave_request_id}",
            json={"start_date": start_date, "end_date": end_date, "reason": reason, "status": status},
            response_model=LeaveRequestData,
            response_error_model=InvalidCredentialsResponse,
        )

    def delete_leave_request(self, leave_request_id: int) -> CustomResponse:
        """Delete a leave request.

        Args:
            leave_request_id: ID of the leave request to delete.
        """
        return self.request(method="DELETE", url=f"{self.url}/{leave_request_id}")

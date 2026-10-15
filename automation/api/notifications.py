"""API client for PeopleHub notification endpoints."""
from typing import Any

from automation.api.base import Base
from automation.custom.response.custom_response import CustomResponse
from automation.dto.schema.auth_models import InvalidCredentialsResponse
from automation.dto.schema.notifications_models import (
    NotificationData, UnreadCountResponse,
)


class Notifications(Base):
    """API client for PeopleHub notification endpoints."""

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the notifications API client.

        Args:
            **kwargs: Arguments passed to the base API client.
        """
        super().__init__(**kwargs)
        self.url = f"{self.url}/notifications"

    def get_notifications(self) -> CustomResponse[NotificationData, InvalidCredentialsResponse]:
        """Get the notifications list."""
        return self.request(
            method="GET",
            url=self.url,
            response_model=NotificationData,
            response_error_model=InvalidCredentialsResponse,
        )

    def get_unread_count(self) -> CustomResponse[UnreadCountResponse, None]:
        """Get the unread notification count."""
        return self.request(
            method="GET",
            url=f"{self.url}/unread-count",
            response_model=UnreadCountResponse
        )

    def mark_as_read(
        self,
        notification_id: int,
    ) -> CustomResponse[NotificationData, InvalidCredentialsResponse]:
        """Mark a notification as read.

        Args:
            notification_id: ID of the notification to mark as read.
        """
        return self.request(
            method="PATCH",
            url=f"{self.url}/{notification_id}/read",
            response_model=NotificationData,
            response_error_model=InvalidCredentialsResponse,
        )

    def mark_all_as_read(self) -> CustomResponse:
        """Mark all notifications as read."""
        return self.request(method="PATCH", url=f"{self.url}/read-all")

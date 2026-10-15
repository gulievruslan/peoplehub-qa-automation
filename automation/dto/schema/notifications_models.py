"""DTOs for PeopleHub notification API."""
from datetime import datetime

from pydantic import Field, StrictBool, StrictInt, StrictStr

from automation.dto.schema.generic import PeopleHubDTO


class NotificationData(PeopleHubDTO):
    """Response DTO for a single notification."""

    id: StrictInt = Field(description="Notification ID")
    user_id: StrictInt = Field(description="User ID")
    title: StrictStr = Field(description="Notification title")
    message: StrictStr = Field(description="Notification message")
    is_read: StrictBool = Field(description="Whether the notification has been read")
    created_at: datetime = Field(description="Creation timestamp")


class UnreadCountResponse(PeopleHubDTO):
    """Response DTO for the unread notification count."""
    count: StrictInt = Field(description="Number of unread notifications")

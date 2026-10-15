"""Custom date and time utilities."""

from collections import namedtuple
from datetime import date, datetime, timedelta, timezone, tzinfo
from typing import Literal, Self, TypeAlias
from automation.custom.exceptions import customdate_time_exceptions

from automation.custom.logger.project_logger import logger


MonthData = namedtuple("MonthData", ["subject", "abbr"])

_MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

MONTHS = {
    number: MonthData(
        subject=_MONTH_NAMES[number - 1],
        abbr=_MONTH_NAMES[number - 1][:3],
    )
    for number in range(1, 13)
}

DateInput: TypeAlias = (
    datetime | date | tuple[str, str] | Literal["min", "max", "unix_min"] | None
)
TimeSpec: TypeAlias = Literal[
    "auto", "hours", "minutes", "seconds", "milliseconds", "microseconds"
]


class CustomDateTime:
    """Represent a date and time with additional formatting and offset operations."""

    _DATE_FORMAT_TOKEN = "__DATE_DAY__"
    _MONTH_FORMAT_TOKEN = "__DATE_MONTH__"

    def __init__(
        self,
        dt: DateInput = None,
        tz: tzinfo | None = None,
        fmt: str = "%Y-%m-%dT%H:%M:%S.%f",
    ) -> None:
        """Initialize the date and time value.

        Args:
            dt: A datetime, date, (date_string, format) tuple, or a predefined boundary.
                Supported boundaries are "min", "max", and "unix_min".
                None uses the current date and time.
            tz: Time zone used only when the current date and time are requested
                (dt is None). It is ignored for all other input values.
            fmt: Default format used when converting the value to a string.

        Raises:
            CustomDateTimeMaskError: If the supplied date string does not match its format.
            CustomDateTimeWrongInputError: If the input value is unsupported.
        """
        self._fmt = fmt
        self._dt = self._build_datetime(value=dt, tz=tz)

    @staticmethod
    def _build_datetime(value: DateInput, tz: tzinfo | None) -> datetime:
        """Convert supported input values into a datetime object."""
        if isinstance(value, datetime):
            return value

        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time())

        if isinstance(value, tuple):
            if len(value) != 2:
                raise customdate_time_exceptions.CustomDateTimeWrongInputError(
                    "A date tuple must contain a date string and its format."
                )

            try:
                return datetime.strptime(value[0], value[1])
            except ValueError as error:
                raise customdate_time_exceptions.CustomDateTimeMaskError(
                    f"Cannot parse {value[0]!r} with format {value[1]!r}"
                ) from error

        if value == "min":
            return datetime.min.replace(year=1900)

        if value == "max":
            return datetime.max

        if value == "unix_min":
            return datetime(1970, 1, 1)

        if value is None:
            return datetime.now(tz=tz)

        raise customdate_time_exceptions.CustomDateTimeWrongInputError(
            "Unsupported value supplied for the dt argument."
        )

    @property
    def dt(self) -> datetime:
        """Return the underlying datetime object."""
        return self._dt

    @property
    def fmt(self) -> str:
        """Return the current date and time format."""
        return self._fmt

    @fmt.setter
    def fmt(self, value: str) -> None:
        """Set the format used for string conversion.

        Args:
            value: A valid datetime format string.

        Raises:
            TypeError: If the format is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("The date format must be a string.")

        self._fmt = value

    @property
    def quarter(self) -> int:
        """Return the calendar quarter of the current date."""
        return (self._dt.month - 1) // 3 + 1

    @property
    def day(self) -> int:
        """Return the day of the month."""
        return self._dt.day

    @property
    def month(self) -> int:
        """Return the month number."""
        return self._dt.month

    @property
    def year(self) -> int:
        """Return the year."""
        return self._dt.year

    def to_date(self) -> date:
        """Return the date component without the time."""
        return self._dt.date()

    def as_string(self) -> str:
        """Format the current value using the configured format."""
        return self._dt.strftime(self._fmt)

    def as_string_text_month(
        self,
        type_: Literal["subject", "abbr"],
        is_lower: bool = True,
        is_trailing_zero: bool = False,
    ) -> str:
        """Format the date using a textual month name.

        Args:
            type_: Month representation: "subject" or "abbr".
            is_lower: Whether to convert the month name to lowercase.
            is_trailing_zero: Whether to preserve the leading zero in the day number.

        Returns:
            The formatted date with a textual month name.

        Raises:
            ValueError: If the requested month representation is unsupported.
        """
        if type_ not in MonthData._fields:
            raise ValueError(f"Unsupported month representation: {type_}")

        month_value = getattr(MONTHS[self._dt.month], type_)
        month_value = month_value.lower() if is_lower else month_value

        fmt = self._fmt.replace("%m", self._MONTH_FORMAT_TOKEN)

        if not is_trailing_zero:
            fmt = fmt.replace("%d", self._DATE_FORMAT_TOKEN)

        result = self._dt.strftime(fmt)
        result = result.replace(self._MONTH_FORMAT_TOKEN, month_value)

        if not is_trailing_zero:
            result = result.replace(self._DATE_FORMAT_TOKEN, str(self._dt.day))

        return result

    def as_isoformat(self, sep: str = "T", timespec: TimeSpec = "auto") -> str:
        """Return the date and time in ISO 8601 format.

        Args:
            sep: Separator between the date and time components.
            timespec: Precision of the time component.

        Returns:
            The ISO 8601 representation of the current value.
        """
        return self._dt.isoformat(sep=sep, timespec=timespec)

    @staticmethod
    def _shift_to_weekday(value: datetime) -> datetime:
        """Move a Saturday or Sunday to the following Monday."""
        weekday = value.isoweekday()

        if weekday == 6:
            return value + timedelta(days=2)

        if weekday == 7:
            return value + timedelta(days=1)

        return value

    @staticmethod
    def _shift_to_saturday(value: datetime) -> datetime:
        """Move the date to Saturday of the same week."""
        return value + timedelta(days=6 - value.isoweekday())

    def _calculate_offset(
        self,
        *,
        to_the_future: bool,
        utc: bool,
        working_day: bool,
        holiday: bool,
        seconds: int,
        minutes: int,
        hours: int,
        days: int,
        weeks: int,
    ) -> datetime:
        """Calculate the shifted datetime without modifying the instance.

        Raises:
            ValueError: If both working_day and holiday are requested.
        """
        if working_day and holiday:
            raise ValueError("The working_day and holiday flags cannot be combined.")

        base_datetime = (
            datetime.now(timezone.utc).replace(tzinfo=None) if utc else self._dt
        )

        offset = timedelta(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks,
        )

        result = base_datetime + offset if to_the_future else base_datetime - offset

        if working_day:
            result = self._shift_to_weekday(value=result)

        if holiday:
            result = self._shift_to_saturday(value=result)

        return result

    def set_offset(
        self,
        *,
        to_the_future: bool = True,
        utc: bool = False,
        working_day: bool = False,
        holiday: bool = False,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
    ) -> Self:
        """Apply a time offset and update the current value.

        Args:
            to_the_future: Move forward when True, otherwise move backward.
            utc: Use the current naive UTC time as the starting point instead of
                the stored value. The stored value is discarded.
            working_day: Move a weekend result to the following Monday.
            holiday: Move the result to Saturday of the same week.
                Cannot be combined with working_day.
            seconds: Number of seconds to shift.
            minutes: Number of minutes to shift.
            hours: Number of hours to shift.
            days: Number of days to shift.
            weeks: Number of weeks to shift.

        Returns:
            The same instance with the updated date and time.

        Raises:
            ValueError: If both working_day and holiday are requested.
        """
        self._dt = self._calculate_offset(
            to_the_future=to_the_future,
            utc=utc,
            working_day=working_day,
            holiday=holiday,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks,
        )
        logger.debug("Date and time updated: {}", self.as_string())

        return self

    def get_offset_string(
        self,
        *,
        to_the_future: bool = True,
        utc: bool = False,
        working_day: bool = False,
        holiday: bool = False,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
        weeks: int = 0,
    ) -> str:
        """Return the shifted value as a string without modifying the instance.

        Args:
            to_the_future: Move forward when True, otherwise move backward.
            utc: Use the current naive UTC time as the starting point instead of
                the stored value.
            working_day: Move a weekend result to the following Monday.
            holiday: Move the result to Saturday of the same week.
                Cannot be combined with working_day.
            seconds: Number of seconds to shift.
            minutes: Number of minutes to shift.
            hours: Number of hours to shift.
            days: Number of days to shift.
            weeks: Number of weeks to shift.

        Returns:
            The shifted date and time formatted as a string.

        Raises:
            ValueError: If both working_day and holiday are requested.
        """
        shifted = self._calculate_offset(
            to_the_future=to_the_future,
            utc=utc,
            working_day=working_day,
            holiday=holiday,
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            days=days,
            weeks=weeks,
        )
        return shifted.strftime(self._fmt)

    def __str__(self) -> str:
        """Return the formatted date and time."""
        return self.as_string()

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the instance."""
        return f"{type(self).__name__}(dt={self._dt!r}, fmt={self._fmt!r})"


def main() -> None:
    """Show basic usage of CustomDateTime."""
    sample = CustomDateTime(dt=("15.03.2026T10:00:00", "%d.%m.%YT%H:%M:%S"))

    print(sample.get_offset_string(days=1, working_day=True))  # does not mutate
    print(sample.set_offset(weeks=1, holiday=True).as_string())  # mutates
    print(sample.as_string_text_month(type_="subject", is_lower=False))


if __name__ == "__main__":
    main()
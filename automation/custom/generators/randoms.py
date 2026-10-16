"""Random data generator"""

import string
from collections.abc import Sequence
from enum import Enum
from random import randint, sample
from typing import Any, Literal, overload

from mimesis.locales import Locale
from mimesis.providers import Datetime, Person
from mimesis.random import Random

from automation.custom.generators.log_result_to_allure import log_result_to_allure
from automation.custom.logger.project_logger import logger


class AlphabetEnum(Enum):
    """Enumeration of alphabets.

    Attributes:
        LATIN: English (Latin) alphabet.
        PUNCTUATION: Punctuation marks.
        LATIN_DIGITS: English (Latin) alphabet and digits.
    """

    LATIN = string.ascii_lowercase
    PUNCTUATION = string.punctuation
    LATIN_DIGITS = string.ascii_lowercase + string.digits


@log_result_to_allure(name="Generator. Get random number")
def get_random_number(
    start: int = 1,
    end: int = 999999,
    length: int | None = None,
    needs_allure: bool = True,
) -> int:
    """Generate a random number within a specified range or with a specified length.

    Args:
        start: The lower bound of the range.
        end: The upper bound of the range.
        length: The number of digits.
        needs_allure: Whether to log the result to Allure.
            - True: Log the result to Allure.
            - False: Do not log the result to Allure.
    """
    return randint(10 ** (length - 1), (10 ** length) - 1) if length else randint(start, end)


@log_result_to_allure(name="Generator. Get random string")
def get_random_string(
    alphabet: AlphabetEnum | str = AlphabetEnum.LATIN,
    length: int = 10,
    needs_allure: bool = True,
) -> str:
    """Generate a random string.

    Args:
        alphabet: The alphabet to use.
        length: The length of the string.
        needs_allure: Whether to log the result to Allure.
            - True: Log the result to Allure.
            - False: Do not log the result to Allure.
    """
    return Random()._generate_string(
        str_seq=alphabet.value if isinstance(alphabet, AlphabetEnum) else alphabet,
        length=length,
    )


@log_result_to_allure(name="Generator. Get random phone number")
def get_random_phone(mask: str = "+7(###)###-##-##", needs_allure: bool = True) -> str:
    """Generate a random phone number in the specified format.

    Args:
        mask: The phone number format.
        needs_allure: Whether to log the result to Allure.
            - True: Log the result to Allure.
            - False: Do not log the result to Allure.
    """
    return Person(locale=Locale.RU).telephone(mask=mask)


@log_result_to_allure(name="Generator. Get random date")
def get_random_date(
    mask: str = "%d.%m.%Y",
    start: int = 2000,
    end: int = Datetime._CURRENT_YEAR - 1,
    needs_allure: bool = True,
) -> str:
    """Generate a random date in the specified format.

    Args:
        mask: The date format.
        start: The inclusive lower bound for the year.
        end: The inclusive upper bound for the year.
        needs_allure: Whether to log the result to Allure.
            - True: Log the result to Allure.
            - False: Do not log the result to Allure.
    """
    return Datetime(locale=Locale.RU).date(start=start, end=end).strftime(format=mask)


@log_result_to_allure(name="Generator. Get random email")
def get_random_email(
    domains: tuple[str, ...] = ("mail.ru", "gmail.com", "yandex.ru"),
    unique: bool = False,
    needs_allure: bool = True,
) -> str:
    """Generate a random email address.

    Args:
        domains: The list of domains to use.
        unique: Whether to generate a unique email address.
        needs_allure: Whether to log the result to Allure.
            - True: Log the result to Allure.
            - False: Do not log the result to Allure.
    """
    return Person(locale=Locale.RU).email(domains=domains, unique=unique)


@overload
def get_random[T](sequence: Sequence[T], count: Literal[1], needs_allure: bool = True) -> T: ...


@overload
def get_random[T](sequence: Sequence[T], count: int, needs_allure: bool = True) -> T | list[T]: ...


@log_result_to_allure("Get a random value or sample from a sequence")
def get_random[T](sequence: Sequence[T], count: int = 1, needs_allure: bool = True, **kwargs: Any) -> T | list[T]:
    """Get a random value or sample from the provided sequence.
    Args:
        sequence: Any sequence from which to select a random element or sample.
        count: The number of elements to select. Defaults to 1.
        needs_allure: Whether to log the result to Allure.
            - True: Log the result to Allure.
            - False: Do not log the result to Allure.

    Returns:
        result: A random element or a sample of elements from the sequence.
    """
    logger.debug(
        f"Selecting {count} random elements from the sequence\n"
        f"Sequence:\n\t{sequence}",
    )

    try:
        result = sample(population=sequence, k=count)

    except ValueError as exception:
        logger.error(f"Sample size ({count}) is smaller than the sequence length ({len(sequence)})")
        raise exception

    except TypeError:
        logger.debug("The provided object is not a sequence")
        raise

    logger.debug(f"Selected sample: {result}")

    return result[0] if count == 1 else result
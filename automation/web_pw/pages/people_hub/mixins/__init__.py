"""Public interface for mixins that extend the functionality of other classes."""

from automation.web_pw.pages.people_hub.mixins.base_actions_mixin import BaseActionsMixin
from automation.web_pw.pages.people_hub.mixins.base_checks_mixin import BaseChecksMixin
from automation.web_pw.pages.people_hub.mixins.browser_actions_mixin import BrowserActionsMixin
from automation.web_pw.pages.people_hub.mixins.elements_checks_mixin import ChecksMixin
from automation.web_pw.pages.people_hub.mixins.waiter_actions_mixin import WaiterActionsMixin

__all__ = (
    "BaseActionsMixin",
    "BaseChecksMixin",
    "BrowserActionsMixin",
    "ChecksMixin",
    "WaiterActionsMixin",
)
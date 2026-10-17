"""The module contains classes for PeopleHub Allure annotations."""
from allure import epic, feature
from pytest import mark


@epic("PeopleHub")
class PeopleHub:
    """PeopleHub service markup."""


@feature("Backend API")
@mark.api
@mark.people_hub
class PeopleHubApi(PeopleHub):
    """PeopleHub API test markup."""


@feature("Frontend Web")
@mark.web
@mark.playwright
@mark.people_hub_web
class PeopleHubWeb(PeopleHub):
    """PeopleHub Web test markup."""
"""Модуль содержит класс для хранения констант разметки сервисов в allure_custom"""
from allure import epic
from pytest import mark


@epic('PeopleHub')
class PeopleHub:
    """PeopleHub service markup"""
    pass


@mark.api
@mark.people_hub
class PeopleHubApi(PeopleHub):
    """People Hub service markup"""
    pass


@mark.web
@mark.playwright
@mark.people_hub_web
class PeopleHubWeb(PeopleHub):
    """People Hub service markup"""
    pass

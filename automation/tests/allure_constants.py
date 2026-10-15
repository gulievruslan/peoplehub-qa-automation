"""Модуль содержит класс для хранения констант разметки сервисов в allure"""
from allure import epic, feature
from pytest import mark


@mark.people_hub
@epic('PeopleHub')
class PeopleHub:
    """PeopleHub service markup"""
    pass


@mark.api
class PeopleHubApi(PeopleHub):
    """People Hub service markup"""
    pass


@mark.web
@mark.playwright
class PeopleHubWeb(PeopleHub):
    """People Hub service markup"""
    pass

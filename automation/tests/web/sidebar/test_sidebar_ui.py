from allure import story
from pytest import mark

from automation.config.users import ADMIN
from automation.custom.custom_typing import Fixture
from automation.custom.typed_decorators import typed_qase_id, typed_title
from automation.tests.allure_constants import PeopleHubWeb
from automation.tests.web.enums import SidebarMenuButtonNames
from automation.web_pw.pages.people_hub.people_hub_web.components.sidebar import SidebarComponent


@story('Sidebar')
@mark.sidebar_ui
class TestSidebarUI(PeopleHubWeb):

    @typed_qase_id(qase_id=139)
    @typed_title(value='Navigate between main application sections')
    @mark.parametrize("pw_open_page", [(ADMIN, SidebarComponent)], indirect=True)
    def test_navigate_application(self, pw_open_page: Fixture[SidebarComponent]):
        menu_items = (
            ("leave-requests", SidebarMenuButtonNames.LEAVE_REQUESTS),
            (SidebarMenuButtonNames.EMPLOYEES.lower(), SidebarMenuButtonNames.EMPLOYEES),
            (SidebarMenuButtonNames.DEPARTMENTS.lower(), SidebarMenuButtonNames.DEPARTMENTS),
            (SidebarMenuButtonNames.DASHBOARD.lower(), SidebarMenuButtonNames.DASHBOARD),
        )

        pw_open_page.check_sidebar_elements_displaying()

        pw_open_page.check_sidebar_element_is_active(
            href_element=SidebarMenuButtonNames.DASHBOARD.lower(),
            text=SidebarMenuButtonNames.DASHBOARD,
        )

        for href_element, text in menu_items:
            pw_open_page.click_sidebar_element(
                href_element=href_element,
                text=text,
            )
            pw_open_page.check_sidebar_element_is_active(href_element=href_element, text=text)

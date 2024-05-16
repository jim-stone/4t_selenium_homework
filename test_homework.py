import os
import time

from dotenv import load_dotenv
from pages import HomePage

load_dotenv()


def test_can_login(logged_in):
    assert HomePage(logged_in).get_current_user_email() == os.getenv('ADM_MAIL')


def test_can_add_project(chrome_browser, logged_in):
    home_page = HomePage(browser=chrome_browser)
    projects_page = home_page.navigate_to_admin_panel()
    add_project_page = projects_page.start_add_project()
    projects_page_updated, project_name = add_project_page.fill_project_data()
    search_result = projects_page_updated.search_project(project_name)
    assert project_name in search_result

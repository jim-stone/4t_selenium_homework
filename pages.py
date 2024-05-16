from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from faker import Faker

fake = Faker()
class AbstractBasePage:
    def __init__(self, browser):
        self.browser = browser
        self.wait = WebDriverWait(driver=self.browser, timeout=10)


class LoginPage(AbstractBasePage):
    url = 'http://demo.testarena.pl/zaloguj'
    input_login = (By.CSS_SELECTOR, '#email')
    input_password = (By.CSS_SELECTOR, '#password')
    button_login = (By.CSS_SELECTOR, '#login')

    def open(self):
        self.browser.get(self.url)
        return self

    def login(self, login, password):

        self.browser.find_element(*self.input_login).send_keys(login)
        self.browser.find_element(*self.input_password).send_keys(password)
        self.browser.find_element(*self.button_login).click()


class AddProjectPage (AbstractBasePage):
    input_name = (By.CSS_SELECTOR, '#name')
    input_prefix = (By.CSS_SELECTOR, '#prefix')
    input_description = (By.CSS_SELECTOR, '#description')
    button_save = (By.CSS_SELECTOR, '#save')
    link_projects = (By.CSS_SELECTOR, 'a.activeMenu')

    def __init__(self, browser):
        super().__init__(browser)
        self.name = None
        self.prefix = None
        self.description = None

    def fill_project_data(self):
        self.wait.until(EC.all_of(
            EC.visibility_of_element_located(self.input_name),
            EC.visibility_of_element_located(self.input_prefix),
            EC.visibility_of_element_located(self.input_description),
            EC.visibility_of_element_located(self.button_save)
        ))
        self.prefix = fake.cryptocurrency_code() + fake.bothify('??#??#')
        self.name = fake.catch_phrase()
        self.description = fake.text(500)
        self.browser.find_element(*self.input_prefix).send_keys(self.prefix)
        self.browser.find_element(*self.input_name).send_keys(self.name)
        self.browser.find_element(*self.input_description).send_keys(self.description)
        self.browser.find_element(*self.button_save).click()
        self.browser.find_element(*self.link_projects).click()
        return ProjectsPage(self.browser), self.name


class ProjectsPage(AbstractBasePage):
    # selektor zwraca 2 elementy, w metodzie wybieramy pierwszy z tej kolekcji
    add_project_link = (By.CSS_SELECTOR, "a.button_link")
    search_input = (By.CSS_SELECTOR, "#search")
    search_button = (By.CSS_SELECTOR, "#j_searchButton")
    search_result = (By.CSS_SELECTOR, "td a")

    def start_add_project(self):
        self.wait.until(EC.visibility_of_all_elements_located(self.add_project_link))
        self.browser.find_elements(*self.add_project_link)[0].click()
        return AddProjectPage(self.browser)

    def search_project(self, project_name):
        self.wait.until(EC.all_of(
                EC.visibility_of_element_located(self.search_input),
                EC.visibility_of_element_located(self.search_button)
            ))
        self.browser.find_element(*self.search_input).send_keys(project_name)
        self.browser.find_element(*self.search_button).click()
        self.wait.until(
            EC.presence_of_all_elements_located(self.search_result)
        )
        elements = self.browser.find_elements(*self.search_result)
        return [e.text for e in elements]

class HomePage (AbstractBasePage):
    user_email = (By.CSS_SELECTOR, ".user-info small")
    admin_link = (By.CSS_SELECTOR, "a[title=Administracja]")

    def get_current_user_email(self):
        return self.browser.find_element(*self.user_email).text

    def navigate_to_admin_panel(self):
        self.wait.until(EC.visibility_of_element_located(self.admin_link))
        self.browser.find_element(*self.admin_link).click()
        return ProjectsPage(self.browser)

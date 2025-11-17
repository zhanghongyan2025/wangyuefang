from playwright.sync_api import Page
from tests.utils.page_utils import *

from playwright.sync_api import sync_playwright, Page
from tests.utils.page_utils import *
from playwright.sync_api import expect

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.get_by_role("textbox", name="账号")
        self.password = page.get_by_role("textbox", name="密码")
        self.login_button = page.get_by_role("button", name="登 录")
        self.error_elements = self.page.locator('[class*="el-form-item__error"]')

    def navigate(self, fd_base_url: str):
        self.page.goto(f"{fd_base_url}/login")

    def fill_username(self, login_username: str, test_fields: str = None):
        fill_textbox(self.page, "账号", login_username)
        if test_fields == "login_username":
            self.username.blur()

    def fill_password(self, login_password: str, test_fields: str = None):
        fill_textbox(self.page, "密码", login_password)
        if test_fields == "login_password":
            self.password.blur()

    def fill_credentials(self, login_username: str, login_password: str, test_fields: str = None):
        fill_textbox(self.page, "账号", login_username)
        fill_textbox(self.page, "密码", login_password)
        if test_fields == "login_password":
            self.password.blur()

    def click_login_button(self):
        self.login_button.click()

    def login_username_error(self, message: str) -> bool:
        """检查账号输入框是否显示指定的错误提示"""
        return  get_element_corresponding_error_tip(self.username,'../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def login_password_error(self, message: str) -> bool:
        """检查密码输入框是否显示指定的错误提示"""
        return  get_element_corresponding_error_tip(self.password,'../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def  login_error(self, message: str) -> bool:
         is_matched, actual_text = check_alert_text(self.page, message)
         return is_matched
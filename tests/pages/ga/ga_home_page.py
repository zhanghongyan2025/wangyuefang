import logging

from tests.utils.page_utils import *
from  tests.utils.validator import *
from playwright.sync_api import Page

class GAHomePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_other_page(self, target_page_name: str):
        try:
            self.page.locator(f'//a[text()="{target_page_name}"]').click()
        except Exception as e:
            raise e


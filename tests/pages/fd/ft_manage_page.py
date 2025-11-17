from tests.utils.page_utils import *
from  tests.utils.validator import *
from playwright.sync_api import Page

class FTManagePage:
    def __init__(self, page: Page):
        self.page = page

        # prefix = "法定"
        # # # 页面元素定位
        # # 页面元素定位
        # self.username_input = get_label_corresponding_input(self.page,  "用户名")
        # self.password_input = get_label_corresponding_input(self.page,  "密码")
        # self.password_conform_input = get_label_corresponding_input(self.page,  "确认密码")
        # self.phone_input = get_label_corresponding_input(self.page,  "联系电话")
        # self.verify_code_input = get_label_corresponding_input(self.page,  "短信验证码")
        # self.verify_code_button = self.page.get_by_role("button", name="获取验证码")
        # self.fd = self.page.locator(f'label:has-text("个人")')
        # self.enterprise = self.page.locator(f'label:has-text("企业")')
        # self.person_in_charge_input = get_label_corresponding_input(self.page,  "负责人姓名")
        # self.person_in_charge_ID_input = get_label_corresponding_input(self.page,  "负责人身份证号")
        # self.person_in_charge_tel_input = get_label_corresponding_input(self.page,  "负责人联系电话")
        #
        # self.legal_person_in_charge_input = get_label_corresponding_input(self.page, "法定负责人姓名")
        # self.legal_person_in_charge_ID_input = get_label_corresponding_input(self.page, "法定负责人身份证号")
        # self.legal_person_in_charge_tel_input = get_label_corresponding_input(self.page, "法定负责人联系电话")
        #
        # self.enterprise_name_input = get_label_corresponding_input(self.page,  "企业名称")
        # self.USCC_input = get_label_corresponding_input(self.page, "统一社会信用代码")
        # self.register_button = self.page.get_by_text("注 册",exact=True)
        # self.cancel_button = self.page.get_by_role("button", name="取消")
        # self.error_messages = self.page.locator('[class*="error"]')

    def navigate_to_other_manage_page(self, target_page_name: str):
        try:
            self.page.get_by_role("menuitem", name=target_page_name).click()
        except Exception as e:
            raise e


import logging

from tests.utils.page_utils import *
from  tests.utils.validator import *
from playwright.sync_api import Page

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.tip_without_registed_room = "请备案民宿及房间信息。"
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

    def navigate_to_house_manage_page(self):
        try:
            self.page.get_by_role("menuitem", name="房屋管理").click()
        except Exception as e:
            raise e

    def tip_without_registed_room_dialog(self):
        try:
            wait_dialog_with_expected_message(self.page,  self.tip_without_registed_room)
        except Exception as e:
            raise e

    def tip_without_registed_room_dialog_option(self, operation: str):
        """
        根据操作类型处理未备案房间的提示弹窗，并验证弹窗是否消失
        :param operation: 操作类型，支持"关闭"、"close"、"备案民宿"
        """
        try:
            # 先确认弹窗已显示
            tip_without_registed_room_dialog()

            # 记录弹窗中的关键文本选择器，用于后续验证消失状态
            dialog_selector = f'text="{self.tip_without_registed_room}"'

            if operation == "关闭" or operation.lower() == "close":
                # 点击关闭按钮
                close_button = self.page.get_by_role("button", name=operation, exact=True)
                close_button.click()

                # 验证弹窗消失 - 等待关键文本从DOM中移除
                self.page.wait_for_selector(dialog_selector, state='detached', timeout=5000)
                logging.info(f"验证成功：'{operation}'操作后弹窗已消失")

            elif operation == "备案民宿":
                # 点击备案民宿按钮
                register_button = self.page.get_by_role("button", name="备案民宿", exact=True)
                register_button.click()

                # 验证跳转后的页面URL
                self.page.wait_for_url("http://192.168.40.61:3333/fangwu_fangdong/minsu", timeout=10000)

                # 同时验证原弹窗已消失
                self.page.wait_for_selector(dialog_selector, state='detached', timeout=5000)
                print("验证成功：跳转后原弹窗已消失")

            else:
                raise ValueError(f"不支持的操作类型：{operation}，支持的操作有：关闭、close、备案民宿")

        except Exception as e:
            raise e

# page.get_by_role("button", name="关闭").click(button="right")
#     page.get_by_role("button", name="备案民宿").click(button="right")
#     page.get_by_role("button", name="Close").click(button="right")

from tests.utils.page_utils import *
from  tests.utils.validator import *
from playwright.sync_api import Page
from conf.logging_config import logger

class RegisterPage:
    def __init__(self, page: Page):
        self.page = page

        prefix = "法定"
        # 页面元素定位
        self.username = get_label_corresponding_input(self.page,  "用户名")
        self.password = get_label_corresponding_input(self.page,  "密码")
        self.password_conform= get_label_corresponding_input(self.page,  "确认密码")
        self.phone = get_label_corresponding_input(self.page,  "联系电话")
        self.verify_code = get_label_corresponding_input(self.page,  "短信验证码")
        self.verify_code_button = self.page.get_by_role("button", name="获取验证码")
        self.fd_type = "个人"
        self.fd = self.page.locator(f'label:has-text("个人")')
        self.enterprise = self.page.locator(f'label[role="radio"]:has-text("企业")')
        self.person_in_charge = get_label_corresponding_input(self.page,  "负责人姓名")
        self.person_in_charge_ID= get_label_corresponding_input(self.page,  "负责人身份证号")
        self.person_in_charge_tel = get_label_corresponding_input(self.page,  "负责人联系电话")

        self.legal_person_in_charge = get_label_corresponding_input(self.page, "法定负责人姓名")
        self.legal_person_in_charge_ID= get_label_corresponding_input(self.page, "法定负责人身份证号")
        self.legal_person_in_charge_tel = get_label_corresponding_input(self.page, "法定负责人联系电话")

        self.enterprise_name = get_label_corresponding_input(self.page,  "企业名称")
        self.USCC = get_label_corresponding_input(self.page, "统一社会信用代码")
        self.register_button = self.page.get_by_text("注 册",exact=True)
        self.cancel_button = self.page.get_by_role("button", name="取消")
        self.error_messages = self.page.locator('[class*="error"]')

    def navigate(self, fd_base_url):
        try:
            self.page.goto(f"{fd_base_url}/login")
            self.page.get_by_text("房东注册").click()
        except Exception as e:
            raise e

    def select_fd_type(self, fd_type = "个人"):
        """选择房东类型（个人或企业）"""
        try:
            if fd_type == "个人":
                self.fd.click()
                self.fd_type = "个人"
            elif fd_type == "企业":
                self.enterprise.click()
                self.fd_type = "企业"
            else:
                raise ValueError(f"Invalid fd_type: {fd_type}. Allowed values are '个人' or '企业'.")
        except Exception as e:
            raise e

    def fill_basic_info(self, username: str = "", password: str = "",  confirm_password: str | None = None, phone_number: str = "",
                        person_in_charge: str = "", person_in_charge_ID: str = "", person_in_charge_tel: str = "",
                        verify_code: str | None = None, send_verification_code:bool=True):
        """填写基础注册信息"""
        try:
            # 添加调试信息
            # logger.info(f"send_verification_code值: {send_verification_code}, 类型: {type(send_verification_code)}")
            self.username.fill(username)
            self.password.fill(password)
            self.password_conform.fill(confirm_password)
            self.phone.fill(phone_number)
            if  send_verification_code:
                self.send_verification_code(phone_number, send_verification_code)
            else:
                self.verify_code.fill(verify_code)

            if self.fd_type == "个人":
                self.person_in_charge.fill(person_in_charge)
                self.person_in_charge_ID.fill(person_in_charge_ID)
                self.person_in_charge_tel.fill(person_in_charge_tel)
            elif self.fd_type == "企业":
                self.legal_person_in_charge.fill(person_in_charge)
                self.legal_person_in_charge_ID.fill(person_in_charge_ID)
                self.legal_person_in_charge_tel.fill(person_in_charge_tel)
            else:
                raise ValueError(f"Invalid fd_type: {self.fd_type}. Allowed values are '个人' or '企业'.")
        except Exception as e:
            raise e

    def fill_enterprise_info(self, enterprise_name: str, USCC: str):
        try:
            scroll_to_bottom(self.page)
            self.enterprise_name.fill(enterprise_name)
            self.USCC.fill(USCC)
        except Exception as e:
            raise e

    def send_verification_code(self, phone_number: str, send_verification_code:bool) -> None:
        """发送短信验证码"""
        try:
            stripped_phone = phone_number.strip()

            # 情况4: 手机号不为空且测试字段集合为空
            if stripped_phone and send_verification_code:
                self.verify_code_button.click()
                # 如果未提供验证码，则从日志中提取
                verify_code = extract_verification_code_live(
                    "192.168.40.61",
                    "root",
                    "dell_123456",
                    "22",
                    "/opt/tomcat8.5.84-wyf-fd-3333/logs/catalina.out",
                    stripped_phone
                )

                result, actual_text = check_alert_text(self.page, "验证码发送成功")
                if not result:
                    # 记录错误信息
                    error_msg = f"验证码发送失败，未显示预期提示。实际提示: {actual_text if actual_text else '无'}"
                    logger.error(error_msg)

                # # 如果未提供验证码，则从日志中提取
                # verify_code = extract_verification_code_live(
                #     "192.168.40.61",
                #     "root",
                #     "dell_123456",
                #     "22",
                #     "/opt/tomcat8.5.84-wyf-fd-3333/logs/catalina.out",
                #     stripped_phone
                # )

                # 填充验证码（无论是否从日志获取）
                self.verify_code.fill(verify_code)

        except Exception as e:
            logger.error(f"发送验证码过程中出错: {str(e)}")
            raise

    def submit_registration(self):
        """提交注册表单"""
        try:
            scroll_to_bottom(self.page)
            self.register_button.click()
        except Exception as e:
            raise e

    def username_alert_error(self, message: str) -> bool:
        result, _ = check_alert_text(self.page, message)
        return result

    def get_verify_code_button_text(self):
        """获取验证码按钮的文本内容"""
        return self.page.locator("button:has-text('获取验证码')").text_content().strip()

    def is_verify_code_button_enabled(self):
        """检查验证码按钮是否启用"""
        return not self.page.locator("button:has-text('获取验证码')").is_disabled()

    def get_verify_code_button_class(self):
        """获取验证码按钮的class属性"""
        return self.page.locator("button:has-text('获取验证码')").get_attribute("class")

    def get_verify_code_button_attribute(self, attribute_name):
        """获取验证码按钮的指定属性值"""
        return self.page.locator("button:has-text('获取验证码')").get_attribute(attribute_name)

    def get_register_success_dialog(self, success_text):
        """
        验证注册成功提示信息是否正确显示
        此方法会检查页面上弹出的提示框，确认其文本内容与预期的注册成功信息一致

        Args:
            success_text (str): 预期显示的注册成功提示文本
        """
        return check_dialog_text(self.page, success_text)  # 调用检查对话框文本的工具函数

    def get_error_tip(self, target_label, expected_text):
        try:
            get_label_corresponding_error_tip(self.page, target_label, expected_text)
        except Exception as e:
            raise e

    def username_error(self, message: str) -> bool:
        """检查账号输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.username, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def password_error(self, message: str) -> bool:
        """检查密码输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.password, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def password_conform_error(self, message: str) -> bool:
        """检查确认密码输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.password_conform, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def phone_number_error(self, message: str) -> bool:
        """检查联系电话输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.phone, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def phone_number_alert_error(self, message: str) -> bool:
        """检查联系电话输入框是否显示指定的错误提示"""
        result, _ = check_alert_text(self.page, message)
        return result

    def verify_code_error(self, message: str) -> bool:
        """检查验证码输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.verify_code,'../following-sibling::button/following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def verify_code_button_error(self, message: str) -> bool:
        """检查联系电话输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.phone,'../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def verify_code_alert_error(self, message: str) -> bool:
        result, _ = check_alert_text(self.page, message)
        return result

    def person_in_charge_error(self, message: str) -> bool:
        """检查负责人姓名输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.person_in_charge, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def person_in_charge_alert_error(self, message: str) -> bool:
        result, _ = check_alert_text(self.page, message)
        return result

    def person_in_charge_ID_error(self, message: str) -> bool:
        """检查负责人身份证号输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.person_in_charge_ID, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def person_in_charge_tel_error(self, message: str) -> bool:
        """检查负责人联系电话输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.person_in_charge_tel, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def legal_person_in_charge_error(self, message: str) -> bool:
        """检查法定负责人姓名输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.legal_person_in_charge, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def legal_person_in_charge_ID_error(self, message: str) -> bool:
        """检查法定负责人身份证号输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.legal_person_in_charge_ID, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def legal_person_in_charge_tel_error(self, message: str) -> bool:
        """检查法定负责人联系电话输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.legal_person_in_charge_tel, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def enterprise_name_error(self, message: str) -> bool:
        """检查企业名称输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.enterprise_name, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def USCC_error(self, message: str) -> bool:
        """检查统一社会信用代码输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.USCC, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def confirm_password_error(self, message: str) -> bool:
        """检查统一社会信用代码输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(self.password_conform, '../following-sibling::div[contains(@class, "el-form-item__error")]', message)

    def wait_send_verify_code_tip_disappear(self, timeout: int = 5000) -> bool:

        return wait_alert_text_disappear(self.page, "验证码发送成功")

    def click_sure_button_and_verify_redirect(self, fd_base_url, expected_path: str = "/login"):
        """
        检查并点击对话框中的"确定"按钮，验证是否跳转到指定页面

        参数:
            expected_path: 期望跳转的路径，默认为登录页面

        返回:
            Locator: "确定"按钮的定位器对象

        异常:
            AssertionError: 按钮不存在、不可点击、点击失败或未跳转到指定页面
        """
        try:
            # 等待对话框出现
            dialog = wait_dialog_with_expected_message(self.page, "")

            # 定位并点击"确定"按钮
            confirm_button = dialog.query_selector('button:has-text("确定")')
            assert confirm_button, "未找到'确定'按钮"

            # 点击按钮并等待导航完成
            with self.page.expect_navigation(timeout=5000):
                confirm_button.click()

            # 验证跳转URL
            current_url = self.page.url
            expected_url = f"{fd_base_url}{expected_path}"

            if not current_url.startswith(expected_url):
                logger.error(f"❌ 验证失败: 未跳转到预期页面，期望: {expected_url}，实际: {current_url}")
                raise AssertionError(f"未跳转到预期页面，期望: {expected_url}，实际: {current_url}")

            logger.info(f"✅ 成功跳转到: {current_url}")
            return confirm_button

        except Exception as e:
            logger.error(f"❌ 验证失败: {str(e)}")
            raise

    def close_dialog_and_verify_redirect(self, fd_base_url, expected_path: str = "/login"):
        """
        关闭对话框并验证是否跳转到指定页面

        参数:
            fd_base_url: 应用的基础URL
            expected_path: 期望跳转的路径，默认为登录页面

        返回:
            ElementHandle: 关闭按钮的ElementHandle对象

        异常:
            AssertionError: 关闭按钮不存在、不可点击、点击失败或未跳转到指定页面
        """
        try:
            # 等待对话框出现（不验证消息内容）
            dialog = wait_dialog_with_expected_message(self.page, "")

            # 通过dialog定位关闭按钮（使用button的aria-label属性）
            close_button = dialog.query_selector('button[aria-label="Close"]')

            # 验证关闭按钮是否存在
            if not close_button:
                logger.error("❌ 验证失败: 未找到关闭按钮")
                raise AssertionError("未找到关闭按钮")

            # 使用ElementHandle的方法验证按钮可见性
            start_time = time.time()
            while time.time() - start_time < 2:  # 2秒超时
                if close_button.is_visible():
                    break
                time.sleep(0.1)
            else:
                logger.error("❌ 验证失败: 关闭按钮在2秒内未显示")
                raise AssertionError("关闭按钮在2秒内未显示")

            # 验证关闭按钮是否可点击
            if not close_button.is_enabled():
                logger.error("❌ 验证失败: 关闭按钮不可点击")
                raise AssertionError("关闭按钮不可点击")

            # 点击关闭按钮并等待导航完成
            with self.page.expect_navigation(timeout=5000):
                close_button.click()

            # 验证跳转URL
            current_url = self.page.url
            expected_url = f"{fd_base_url}{expected_path}"

            if not current_url.startswith(expected_url):
                logger.error(f"❌ 验证失败: 未跳转到预期页面，期望: {expected_url}，实际: {current_url}")
                raise AssertionError(f"未跳转到预期页面，期望: {expected_url}，实际: {current_url}")

            logger.info(f"✅ 成功跳转到: {current_url}")
            return close_button

        except AssertionError as ae:
            logger.error(f"❌ 验证失败: {str(ae)}")
            raise
        except TimeoutError:
            logger.error("❌ 验证失败: 等待页面跳转超时")
            raise AssertionError("等待页面跳转超时")
        except Exception as e:
            logger.error(f"❌ 验证失败: 关闭对话框或验证跳转时发生异常: {str(e)}")
            raise AssertionError(f"关闭对话框或验证跳转异常: {str(e)}")

import re
from playwright.sync_api import Playwright, sync_playwright, expect

#
# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://192.168.40.61:3333/register")
#     register_page = RegisterPage(page)
#     register_info ={'username': 'enterprise_phone_number_duplicate', 'password': 'ValidP@ss123', 'confirm_password': 'ValidP@ss123',
#                     'phone_number': '13990987657', 'verify_code': '123456', 'person_in_charge': '个人负责人',
#                     'person_in_charge_ID': '110101199001011234', 'person_in_charge_tel': '13987654321'}
#     register_page.fill_basic_info(send_verification_code=True, **register_info)
#     register_page.submit_registration()
#     register_page.person_in_charge_alert_error("联系电话已被注册!")
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
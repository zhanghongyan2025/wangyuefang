import re
import time
import pytest
from playwright.sync_api import expect
from conf.logging_config import logger
from tests.utils.form_validation_utils import FormValidationUtils
from tests.utils.page_utils import check_page_title
from tests.pages.fd.login_page import LoginPage
from tests.utils.validation_utils import check_login_error_messages


# ------------------------------
# 测试类：覆盖登录全场景
# ------------------------------
@pytest.mark.login
class TestLogin:
    """登录测试类，覆盖空字段、格式错误、无效凭据、登录成功等场景"""

    # ------------------------------
    # 场景1：空字段验证（必测基础场景）
    # ------------------------------
    empty_field_cases = [
        # (场景标识, 用户名, 密码, 预期错误提示字典)
        (
            "username_empty",
            "",
            "123456",
            {"login_username": "请输入您的账号"}
        ),  # 用户名空
        (
            "password_empty",
            "test_user",
            "",
            {"login_password": "请输入您的密码"}
        ),  # 密码空
        (
            "both_empty",
            "",
            "",
            {  # 两者都空
                "login_username": "请输入您的账号",
                "login_password": "请输入您的密码"
            }
        )
    ]
    empty_field_ids = [case[0] for case in empty_field_cases]

    @pytest.mark.parametrize(
        "scenario, username, password, expected_errors",
        empty_field_cases,
        ids=empty_field_ids
    )
    def test_empty_field_validation(
            self,
            page,
            fd_base_url,
            scenario,
            username,
            password,
            expected_errors
    ):
        """测试用户名/密码为空时的错误"""
        login_page = LoginPage(page)
        login_page.navigate(fd_base_url)

        # 填充表单（空字段按测试用例传入，非空字段用有效格式）
        login_page.fill_username(username)
        login_page.fill_password(password)

        # 触发验证（点击登录按钮）
        login_page.click_login_button()
        time.sleep(1)  # 等待错误提示渲染

        logger.info(f"📌 场景1：执行空字段测试场景：{scenario}")
        check_login_error_messages(login_page, scenario, expected_errors)

        # 额外验证：登录失败后仍停留在登录页
        expect(page).to_have_url(re.compile(rf"{re.escape(fd_base_url)}/login"))

    # ------------------------------
    # 场景2：无效凭据验证（用户不存在/密码错误）
    # ------------------------------
    invalid_credential_cases = [
        (
            "user_not_found",
            "non_existent_user",
            "123456",
            {"login_button": "用户不存在或密码错误"}
        ),
        (
            "wrong_password",
            "existing_user",
            "wrong_pass",
            {"login_button": "用户不存在或密码错误"}
        )
    ]
    invalid_credential_ids = [case[0] for case in invalid_credential_cases]

    @pytest.mark.parametrize(
        "scenario, username, password, expected_errors",
        invalid_credential_cases,
        ids=invalid_credential_ids
    )
    def test_invalid_credential_validation(
            self,
            page,
            fd_base_url,
            scenario,
            username,
            password,
            expected_errors
    ):
        """测试用户名不存在或密码错误时"""
        login_page = LoginPage(page)
        login_page.navigate(fd_base_url)

        # 填充表单（用户名/密码不匹配）
        login_page.fill_username(username)
        login_page.fill_password(password)

        # 触发验证
        login_page.click_login_button()
        time.sleep(1)  # 等待后端返回错误

        logger.info(f"📌 场景2：执行无效凭据测试场景：{scenario}")
        check_login_error_messages(login_page, scenario, expected_errors)

    # ------------------------------
    # 场景3：登录成功场景（正向用例）
    # ------------------------------
    success_cases = [
        (
            "normal_login",
            "hongyan20256",
            "Aa123123!",
            "/fangdonghome/home",
            "网约房智慧安全监管平台"
        )  # 正常登录
    ]
    success_ids = [case[0] for case in success_cases]

    @pytest.mark.parametrize(
        "scenario, username, password, expected_path, expected_title",
        success_cases,
        ids=success_ids
    )
    def test_login_success(
            self,
            page,
            fd_base_url,
            scenario,
            username,
            password,
            expected_path,
            expected_title
    ):
        """测试使用正确凭据登录成功后的跳转和状态"""
        # 拼接完整的预期 URL（fd_base_url + 路径）
        expected_url = f"{fd_base_url}{expected_path}"
        login_page = LoginPage(page)
        login_page.navigate(fd_base_url)

        # 填充正确凭据
        login_page.fill_username(username)
        login_page.fill_password(password)

        # 触发登录
        login_page.click_login_button()
        page.wait_for_url(expected_url)

        logger.info(f"📌 场景3：执行登录成功测试场景：{scenario}")
        # 验证跳转正确
        check_page_title(page, expected_title)

    # ------------------------------
    # 场景4：无效凭据验证（用户存在但密码错误（密码简单），输入错误超过五次）
    # ------------------------------
    invalid_simple_password_5_times_password_cases = [
        (
            "simple_password_max_wrong_input_login",
            "existing_user_456",
            "123456",
            "/fangdonghome/home",
            "网约房智慧安全监管平台",
            {"login_button": "用户不存在或密码错误"}
        )  # 用户存在，密码错误
    ]
    invalid_credential_ids = [case[0] for case in invalid_simple_password_5_times_password_cases]

    @pytest.mark.parametrize(
        "scenario, username, password,  expected_path, expected_title, expected_errors",
        invalid_simple_password_5_times_password_cases,
        ids=invalid_credential_ids
    )
    def test_invalid_simple_password_5_times_validation(
            self,
            page,
            fd_base_url,
            scenario,
            username,
            password,
            expected_path,
            expected_title,
            expected_errors
    ):
        """用户存在但密码错误，输入错误超过五次，输入正确密码后还能登录"""
        # 拼接完整的预期 URL（fd_base_url + 路径）
        expected_url = f"{fd_base_url}{expected_path}"
        login_page = LoginPage(page)
        login_page.navigate(fd_base_url)

        # 填充表单（用户名/密码不匹配）
        login_page.fill_username(username)
        login_page.fill_password(password)

        # 触发验证
        for _ in range(8):
            login_page.click_login_button()
            time.sleep(3)  # 每次点击后等待1秒
            check_login_error_messages(login_page, scenario, expected_errors)

        logger.info(f"📌 场景4：用户存在但简单密码错误，输入错误超过五次：{scenario}")
        login_page.fill_password("ValidP@ss456")
        login_page.click_login_button()
        time.sleep(10)
        page.wait_for_url(expected_url)


    # ------------------------------
    # 场景5：无效凭据验证（用户存在但密码错误，输入错误超过五次）
    # ------------------------------
    invalid_complex_password_5_times_password_cases = [
        (
        "max_wrong_input_login",
        "existing_user_456",
        "ValidP@ss456&",
        {"login_button": "密码输入错误5次，帐户锁定10分钟"}
    )# 用户存在，密码错误
    ]
    invalid_credential_ids = [case[0] for case in invalid_complex_password_5_times_password_cases]

    @pytest.mark.parametrize(
        "scenario, username, password, expected_errors",
        invalid_complex_password_5_times_password_cases,
        ids=invalid_credential_ids
    )
    def test_invalid_password_5_times_validation(
            self,
            page,
            fd_base_url,
            scenario,
            username,
            password,
            expected_errors
    ):
        """密码输入错误5次，帐户锁定10分钟"""
        login_page = LoginPage(page)
        login_page.navigate(fd_base_url)

        # 填充表单（用户名/密码不匹配）
        login_page.fill_username(username)
        login_page.fill_password(password)

        # 触发验证
        for _ in range(8):
            login_page.click_login_button()
            time.sleep(3)  # 每次点击后等待1秒

        logger.info(f"📌 场景5：用户存在但密码错误，输入错误超过五次：{scenario}")
        login_page.fill_password("ValidP@ss456")
        check_login_error_messages(login_page, scenario, expected_errors)
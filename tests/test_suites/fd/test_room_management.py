import re
import time
import pytest
from conf.config import *
from datetime import datetime
from conf.logging_config import logger
from tests.conftest import page
from tests.pages.fd import filing_room_page
from tests.pages.fd.add_new_minsu import AddNewMinsuPage
from tests.pages.fd.ft_manage_page import FTManagePage
from tests.pages.fd.home_page import HomePage
from tests.pages.fd.minsu_management_page import MinsuManagementPage
from tests.pages.fd.filing_room_page import FilingRoomPage
from tests.pages.fd.room_management_page import RoomManagementPage
from tests.pages.ga.ga_filing_management_page import GAFilingManagementPage
from tests.pages.ga.ga_fw_manage_page import GAFWManagementPage
from tests.pages.ga.ga_home_page import GAHomePage

from tests.utils.page_utils import  checkTipDialog
from tests.pages.fd.login_page import LoginPage


# ------------------------------
# 通用Fixture：复用前置操作（修改为function作用域）
# ------------------------------
@pytest.fixture(scope="function")
def room_management_setup(page, fd_base_url, fd_test_user):
    """
    房间注册测试的前置操作Fixture，其主要功能是完成用户登录并导航到房间注册页面。

    参数:
    page: 页面对象，用于操作浏览器页面。
    fd_base_url: 测试的基础URL。
    fd_test_user: 包含用户名和密码的测试用户信息。

    返回:
    RoomManagementPage 对象，用于后续的房间管理页面操作。
    """
    # 登录操作
    login_page = LoginPage(page)
    login_page.navigate(fd_base_url)
    login_page.fill_credentials(fd_test_user["username"], fd_test_user["password"])
    login_page.click_login_button()

    # 验证登录是否成功，通过检查页面标题来判断
    time.sleep(2)
    assert page.title() == "网约房智慧安全监管平台"

    home_page = HomePage(page)
    home_page.navigate_to_house_manage_page()
    ft_manage_page = FTManagePage(page)
    ft_manage_page.navigate_to_other_manage_page("房间管理")
    return RoomManagementPage(page)


# ------------------------------
# 工具函数：注册页面错误提示验证
# ------------------------------
def check_room_management_error_messages(room_management_page, field, expected_tip):
    """验证注册页面多个字段的错误提示信息是否符合预期

    Args:
        room_management_page: 房间管理页面对象
        expected_tip: 预期错误
    """
    error_method = getattr(room_management_page, f"{field}_error")
    # 调用方法时传入预期错误文本作为参数
    is_match = error_method(expected_tip)
    return is_match

def check_room_management_alert_error_messages(room_management_page, field, expected_tip):
    """验证注册页面多个字段的弹窗错误提示是否符合预期

    Args:
        room_management_page: 房间管理页面对象
        expected_tip: 预期错误
    """
    error_method = getattr(room_management_page, f"{field}_alert_error")
    # 调用方法时传入预期错误文本作为参数
    is_match = error_method(expected_tip)
    return is_match


@pytest.mark.register
class TestRoomManage:
    """新增房间管理测试类"""

    # 场景1：房间操作 - 使用公共参数构建测试用例
    # 统一operation为字符串类型，空操作使用空字符串
    room_operation_cases = [
        (
            "view_normal_room",
            {**COMMON_ROOM_PARAMS, "ms_name": "手持机民宿","room_name": "view normal room"},
            ""  # 空字符串表示无操作
        ),
        (
            "disable_normal_room",
            {**COMMON_ROOM_PARAMS, "ms_name": "手持机民宿", "room_name": "disable normal room",},
            "禁用"
        ),
        (
            "restore_disabled_room",
            {**COMMON_ROOM_PARAMS,"ms_name": "手持机民宿", "room_name": "restore disabled room"},
            "恢复"
        ),
        (
            "log_off_room",
            {**COMMON_ROOM_PARAMS, "ms_name": "手持机民宿","room_name": "log_off_room"},
            "注销"
        ),
    ]
    room_operation_ids = [case[0] for case in room_operation_cases]

    @pytest.mark.parametrize(
        "scenario, room_params, operation",
        room_operation_cases,
        ids=room_operation_ids
    )
    def test_room_operation_room(
            self,
            scenario,
            room_params,
            operation,
            room_management_setup,
            page):
        """
        测试房间操作以及状态集合是否符合预期
        1.正常房间查看的状态以及操作集合
        2.房间禁用后的状态以及操作集合
        3.房间恢复以后的状态以及操作集合
        4.房间注销后的状态以及操作集合
        """
        # 直接使用fixture返回的对象，无需手动调用
        room_management_page = room_management_setup
        room_name = room_params["room_name"]

        # 进入房间填写页面
        room_management_page.go_to_filling_room_page()
        page.wait_for_load_state("load")
        filling_room_page = FilingRoomPage(page)

        # 填充房间信息
        filling_room_page.filing_room(
            test_fields="all",
            property_certificate=JPEG_FIRE_SAFETY_CERTIFICATE,
            fire_safety_certificate=JPEG_FIRE_SAFETY_CERTIFICATE,
            public_security_registration_form=JPEG_PUBLIC_SECURITY_CERTIFICATE,
            bedroom_files=BEDROOM_FILES,
            living_room_files=LIVING_ROOM_FILES,
            kitchen_files=KITCHEN_FILES,
            bathroom_files=BATHROOM_FILES,
            **room_params
        )

        # 提交表单并验证结果
        filling_room_page.submit_form()
        assert filling_room_page.check_register_result()
        time.sleep(5)

        # 查询创建的房间
        room_management_page.query_room(room_name)

        # 验证添加房间状态和操作集合
        logger.info(f"📌 房间管理场景：查看房间状态以及操作集合 [{scenario}]")
        # 验证新添加的房间是否状态为正常
        assert room_management_page.check_room_status("正常")
        time.sleep(1)

        # 执行相应操作 - 优化逻辑：仅当有操作时执行
        if operation:
            # 对于恢复场景，需要先执行禁用操作
            if scenario == "restore_disabled_room":
                room_management_page.room_operation("禁用", room_name)
                # 验证禁用后的状态
                assert room_management_page.check_room_status("禁用")
                time.sleep(3)

            # 执行当前操作并验证
            assert room_management_page.room_operation(operation, room_name)
            logger.info(f"查看{operation}之后房间状态是否符合预期")
            expected_status = room_management_page.get_room_expected_status(operation)
            assert room_management_page.check_room_status(expected_status)
            logger.info(f"查看{operation}之后操作是否符合预期")
            expected_operations = room_management_page.get_room_expected_operations(expected_status)
            assert room_management_page.check_room_operations(expected_operations)

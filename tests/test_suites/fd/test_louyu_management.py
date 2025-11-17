import re
import time
import pytest
from playwright.sync_api import expect
from conf.logging_config import logger
from tests.pages.fd.ft_manage_page import FTManagePage
from tests.pages.fd.home_page import HomePage
from tests.pages.fd.louyu_management import louYuManagementPage
from tests.pages.fd.login_page import LoginPage
from tests.utils.page_utils import checkTipDialog, get_table_cell_or_button, get_label_corresponding_input, \
    check_label_corresponding_input_value, is_query_reset_successful
from tests.utils.validation_utils import check_louyu_management_alert_error_messages, \
    check_louyu_management_error_messages, check_register_alert_error_messages, assert_filed_messages


# ------------------------------
# 测试类：楼宇管理功能测试
# ------------------------------
@pytest.mark.register
class TestLouyuManagement:
    """新增楼宇功能测试类"""

    # ------------------------------
    # 场景1：楼宇名称
    # ------------------------------
    louyu_name_cases = [
        # (场景标识, 各字段值, 预期错误)
        (
            "name_empty",
            {
                "louyu_name": "",
            },
            {
                "louyu_name": "楼宇名称不能为空",
            }
        ),
        (
            "name_min_length",
            {
                "louyu_name": "1",
            },
            {
                "louyu_name": "新增成功",
            }
        ),
        (
            "name_max_length",
            {
                "louyu_name": "123456789012345678901234567890",
            },
            {
                "louyu_name": "新增成功",
            }
        ),
        (
            "name_extend_max_length",
            {
                "louyu_name": "1234567890123456789012345678901",
            },
            {
                "louyu_name": "最多30个字符",
            }
        ),
        (
            "name_already_exists",
            {
                "louyu_name": "一栋一单元",
            },
            {
                "louyu_name": "楼宇名称已存在",
            }
        ),

    ]
    louyu_empty_ids = [case[0] for case in louyu_name_cases]

    @pytest.mark.parametrize(
        "scenario, louyu_info, expected_errors",
        louyu_name_cases,
        ids=louyu_empty_ids
    )
    def test_louyu_name(
            self,
            scenario,
            louyu_info,
            expected_errors,
            louyu_management_setup  # 将fixture作为参数传入，pytest会自动处理其依赖
    , page):
        """
        测试楼宇名称字段验证逻辑
        1.楼宇名称为空
        2.楼宇名称为最小长度
        3.楼宇名称为最大长度
        4.楼宇名称超过最大长度
        5.楼宇名称已存在
        """

        # 直接使用fixture返回的对象，无需手动调用
        louyu_management_page = louyu_management_setup
        # 点击提交按钮

        louyu_management_page.add_louyu(**louyu_info)

        # 验证错误提示
        logger.info(f"📌 楼宇新增场景：楼宇名称字段测试 [{scenario}]")
        check_error_func = check_louyu_management_error_messages
        if scenario == "name_already_exists":
            check_error_func = check_register_alert_error_messages
        assert_filed_messages(
            page=louyu_management_page,  # 注册页面对象
            scenario=scenario,  # 场景标识（如 "password_too_short"）
            expected_errors=expected_errors,  # 预期的成功/错误信息字典
            check_success_func=lambda page, tip: page.louyu_operation_success_alert(tip),
            check_error_func=check_error_func
        )

    # ------------------------------
    # 场景2：修改楼宇
    # ------------------------------

    louyu_modify_cases = [
        # (场景标识, 各字段值, 预期错误)
        (
            "modify_empty",
            {
                "louyu_name": "1",
                "modified_louyu_name": ""
            },
            {
                "louyu_name": "楼宇名称不能为空",
            }
        ),
        (
            "modify_without_change",
            {
                "louyu_name": "1",
                "modified_louyu_name": "1"
            },
            {
                "louyu_name": "修改成功",
            }
        ),

        (
            "modify_to_max_lengh",
            {
                "louyu_name": "1",
                "modified_louyu_name": "123456789012345678901234567899"
            },
            {
                "louyu_name": "修改成功",
            }
        ),

        (
            "modify_extend_max_lengh",
            {
                "louyu_name": "123456789012345678901234567899",
                "modified_louyu_name": "1234567890123456789012345678999"
            },
            {
                "louyu_name": "最多30个字符",
            }
        ),

        (
            "modify_to_original",
            {
                "louyu_name": "123456789012345678901234567899",
                "modified_louyu_name": "1"
            },
            {
                "louyu_name": "修改成功",
            }
        ),

        (
            "modify_already_exists",
            {
                "louyu_name": "1",
                "modified_louyu_name": "一栋一单元"
            },
            {
                "louyu_name": "楼宇名称已存在",
            }
        ),
        # 下面有有效房间
        (
            "modify_with_room_empty",
            {
                "louyu_name": "一栋一单元",
                "modified_louyu_name": ""
            },
            {
                "louyu_name": "楼宇名称不能为空",
            }
        ),

        (
            "modify_with_room_without_change",
            {
                "louyu_name": "一栋一单元",
                "modified_louyu_name": "一栋一单元"
            },
            {
                "louyu_name": "修改成功",
            }
        ),

        (
            "modify_with_room_max_length",
            {
                "louyu_name": "一栋一单元",
                "modified_louyu_name": "123456789012345678901234567888"
            },
            {
                "louyu_name": "修改成功",
            }
        ),

        (
            "modify_with_room_extend_max_lenght",
            {
                "louyu_name": "123456789012345678901234567888",
                "modified_louyu_name": "1234567890123456789012345678888"
            },
            {
                "louyu_name": "最多30个字符",
            }
        ),

        (
            "modify_with_room_already_exists",
            {
                "louyu_name": "123456789012345678901234567888",
                "modified_louyu_name": "1"
            },
            {
                "louyu_name": "楼宇名称已存在",
            }
        ),

        (
            "modify_with_room_to_origin",
            {
                "louyu_name": "123456789012345678901234567888",
                "modified_louyu_name": "一栋一单元"
            },
            {
                "louyu_name": "修改成功",
            }
        ),
    ]
    louyu_empty_ids = [case[0] for case in louyu_modify_cases]

    @pytest.mark.parametrize(
        "scenario, louyu_info, expected_errors",
        louyu_modify_cases,
        ids=louyu_empty_ids
    )
    def test_louyu_modify(
            self,
            scenario,
            louyu_info,
            expected_errors,
            louyu_management_setup  # 将fixture作为参数传入，pytest会自动处理其依赖
    ):
        """
        测试楼宇名称字段修改验证逻辑
        1.楼宇（名下没有房间）名称修改为空
        2.楼宇（名下没有房间）名称不修改
        3.楼宇（名下没有房间）名称修改为最大长度
        4.楼宇（名下没有房间）名称修改为超过最大长度
        5.楼宇（名下没有房间）名称修改为原来的值
        6.楼宇（名下没有房间）名称修改为已存在的楼宇名称
        7.楼宇（名下有房间）名称修改为空
        8.楼宇（名下有房间）名称不修改
        9.楼宇（名下有房间）名称修改为最大长度
        10.楼宇（名下有房间）名称修改为超过最大长度
        11.楼宇（名下没有房间）名称修改为已存在的楼宇名称
        """
        # 直接使用fixture返回的对象，无需手动调用
        louyu_management_page = louyu_management_setup

        # 点击提交按钮
        louyu_management_page.modified_louyu(louyu_info["louyu_name"], louyu_info["modified_louyu_name"])
        time.sleep(1)
        # 验证错误提示
        logger.info(f"📌 楼宇名称修改场景：楼宇名称修改测试 [{scenario}]")
        check_error_func = check_louyu_management_error_messages
        if scenario.endswith("_already_exists") :
            check_error_func = check_louyu_management_alert_error_messages
        assert_filed_messages(
            page=louyu_management_page,  # 注册页面对象
            scenario=scenario,  # 场景标识（如 "password_too_short"）
            expected_errors=expected_errors,  # 预期的成功/错误信息字典
            check_success_func=lambda page, tip: page.louyu_operation_success_alert(tip),
            check_error_func=check_error_func
        )
        time.sleep(1)

    # ------------------------------
    # 场景3：删除楼宇
    # ------------------------------

    louyu_delete_cases = [
        # (场景标识, 各字段值, 预期错误)
        (
            "delete_without_room",
            {
                "louyu_name": "1",
            },
            {
                "louyu_name": "删除成功",
            }
        ),
        (
            "delete_with_room",
            {
                "louyu_name": "一栋一单元",
            },
            {
                "louyu_name": "楼宇下存在有效房间,删除失败!",
            }
        ),
    ]
    louyu_delete_ids = [case[0] for case in louyu_delete_cases]

    @pytest.mark.parametrize(
        "scenario, louyu_info, expected_errors",
        louyu_delete_cases,
        ids=louyu_delete_ids
    )
    def test_louyu_delete(
            self,
            scenario,
            louyu_info,
            expected_errors,
            louyu_management_setup  # 将fixture作为参数传入，pytest会自动处理其依赖
    ):
        """
        测试楼宇名称字段修改验证逻辑
        1.楼宇（名下没有房间）删除
        2.楼宇（名下有房间）删除
        """
        # 直接使用fixture返回的对象，无需手动调用
        louyu_management_page = louyu_management_setup
        louyu_management_page.louyu_delete(louyu_info["louyu_name"])
        # 验证错误提示
        logger.info(f"📌 楼宇删除场景：楼宇删除测试 [{scenario}]")

        assert_filed_messages(
            page=louyu_management_page,  # 注册页面对象
            scenario=scenario,  # 场景标识（如 "password_too_short"）
            expected_errors=expected_errors,  # 预期的成功/错误信息字典
            check_success_func=lambda page, tip: page.louyu_operation_success_alert(tip),
            check_error_func=check_louyu_management_alert_error_messages
        )

    # ------------------------------
    # 场景4：重置按钮
    # ------------------------------
    def test_louyu_query_reset(
            self,
            louyu_management_setup  # 将fixture作为参数传入，pytest会自动处理其依赖
    ):
        """测试楼宇查询重置输入框为空"""
        # 直接使用fixture返回的对象，无需手动调用
        louyu_management_page = louyu_management_setup

        louyu_management_page.query_louyu("一栋一单元")
        time.sleep(1)

        search_types=["楼宇名称"]
        assert is_query_reset_successful(louyu_management_page.page, search_types) , \
            f"❌  场景[重置按钮]验证失败"
        logger.info(
            f"✅ 场景[重置按钮] 验证通过:")

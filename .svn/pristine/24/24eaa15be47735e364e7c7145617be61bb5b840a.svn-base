# utils/validation_utils.py
"""所有错误提示验证工具函数"""
from tests.utils.form_validation_utils import FormValidationUtils
from tests.utils.page_utils import checkTipDialog, check_dialog_text


def check_louyu_management_error_messages(louyu_management_page, field, expected_tip):
    """验证楼宇多个字段的错误提示信息是否符合预期

    Args:
        louyu_management_page: 楼宇管理页面对象
        expected_errors: 预期错误字典，格式为{字段名: 预期提示文本}
    """

    error_method = getattr(louyu_management_page, f"{field}_error")
    # 调用方法时传入预期错误文本作为参数
    is_match = error_method(expected_tip)
    return is_match

def check_louyu_management_alert_error_messages(louyu_management_page, field, expected_tip):
    """验证楼宇页面多个字段的弹窗错误提示是否符合预期

    Args:
        louyu_management_page: 楼宇管理页面对象
        expected_errors: 预期错误字典，格式为{字段名: 预期提示文本}
    """
    error_method = getattr(louyu_management_page, f"{field}_alert_error")
    # 调用方法时传入预期错误文本作为参数
    is_match = error_method(expected_tip)
    return is_match

def check_room_management_error_messages(room_management_page, field, expected_tip):
    """验证房间管理页面字段错误提示"""
    error_method = getattr(room_management_page, f"{field}_error")
    return error_method(expected_tip)

def check_room_management_alert_error_messages(room_management_page, field, expected_tip):
    """验证房间管理页面弹窗错误提示"""
    error_method = getattr(room_management_page, f"{field}_alert_error")
    return error_method(expected_tip)

def check_minsu_management_error_messages(minsu_management_page, field, expected_tip):
    """验证民宿管理页面字段错误提示"""
    error_method = getattr(minsu_management_page, f"{field}_error")
    return error_method(expected_tip)

def check_minsu_management_alert_error_messages(minsu_management_page, field, expected_tip):
    """验证民宿管理页面弹窗错误提示"""
    error_method = getattr(minsu_management_page, f"{field}_alert_error")
    return error_method(expected_tip)

def check_register_error_messages(register_page, field, expected_tip):
    """验证注册页面字段错误提示"""
    error_method = getattr(register_page, f"{field}_error")
    return error_method(expected_tip)

def check_register_alert_error_messages(register_page, field, expected_tip):
    """验证注册页面弹窗错误提示"""
    error_method = getattr(register_page, f"{field}_alert_error")
    return error_method(expected_tip)
def check_add_new_minsu_error_messages(add_new_minsu_page, field, expected_tip):
    """验证添加民宿页面多个字段的错误提示信息是否符合预期

    Args:
        add_new_minsu_page: 添加民宿页面对象
        expected_errors: 预期错误字典，格式为{字段名: 预期提示文本}
    """
    error_method = getattr(add_new_minsu_page, f"{field}_error")
    # 调用方法时传入预期错误文本作为参数
    is_match = error_method(expected_tip)
    return is_match

def check_add_new_minsu_alert_error_messages(add_new_minsu_page, field, expected_tip):
    """验证添加民宿页面多个字段的弹窗错误提示是否符合预期

    Args:
        add_new_minsu_page: 添加民宿页面对象
        expected_errors: 预期错误字典，格式为{字段名: 预期提示文本}
    """
    error_method = getattr(add_new_minsu_page, f"{field}_alert_error")
    # 调用方法时传入预期错误文本作为参数
    is_match = error_method(expected_tip)
    return is_match

def check_login_error_messages(login_page, scenario, expected_errors):
    """验证登录页面错误提示"""
    for field, expected_tip in expected_errors.items():
        error_method_name = FormValidationUtils.get_error_selector("login", field)
        error_check_method = getattr(login_page, error_method_name)
        assert error_check_method(expected_tip), (
            f"❌  场景[{scenario}], 字段 [{field}] 错误提示不符合预期 - "
            f"预期: {expected_tip}"
        )

def assert_filed_messages(
    page,
    scenario,
    expected_errors,
    check_success_func=None,  # 允许为None（无需验证成功信息）
    check_error_func=None     # 允许为None（无需验证错误信息）
):
    """
    统一验证场景的成功提示或错误提示
    允许check_success_func或check_error_func为None，但禁止两者同时为None
    """
    # 参数校验：禁止两个函数同时为None
    if check_success_func is None and check_error_func is None:
        raise ValueError("❌ check_success_func和check_error_func不能同时为None，至少需要一个验证函数")

    for field, expected_tip in expected_errors.items():
        # 处理成功提示验证（仅当提供了成功验证函数时）
        if "成功" in expected_tip:
            if check_success_func is None:
                raise ValueError(
                    f"❌ 场景[{scenario}]存在成功提示，但未提供check_success_func"
                )
            assert check_success_func(page, expected_tip), (
                f"❌ 场景[{scenario}], 字段 [{field}] 成功提示不匹配 - "
                f"预期: {expected_tip}, 实际未匹配"
            )
        # 处理错误提示验证（仅当提供了错误验证函数时）
        else:
            if check_error_func is None:
                raise ValueError(
                    f"❌ 场景[{scenario}]存在错误提示，但未提供check_error_func"
                )
            assert check_error_func(page, field, expected_tip), (
                f"❌ 场景[{scenario}], 字段 [{field}] 错误提示不匹配 - "
                f"预期: {expected_tip}, 实际未匹配"
            )

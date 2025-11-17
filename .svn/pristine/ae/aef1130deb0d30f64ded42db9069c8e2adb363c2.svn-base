import re
import time
from zoneinfo import ZoneInfo

import pytest
from conf.config import *
from datetime import datetime
from conf.logging_config import logger
from tests.conftest import page
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
from tests.utils.validation_utils import check_minsu_management_alert_error_messages


# ------------------------------
# 测试类：个人/企业房东注册功能测试
# ------------------------------
class TestConfig:
    """自定义配置类，存储共享数据"""
    minsu_pending_confirmation = "民宿_提交_备案"

@pytest.mark.register
class TestMinsuManage:
    # """新增民宿管理测试类"""
    #
    # 场景1：无任何房间的民宿，状态操作集合,备案房间验证以及删除操作
    without_room_cases = [
        (
            "without_room",

            {
                **COMMON_minsu_PARAMS,
                "minsu_name": "minsu_without_room",
            },
            {
                "delete":"删除成功"
            }
        )
    ]
    without_room_ids = [case[0] for case in without_room_cases]

    @pytest.mark.parametrize(
        "scenario, minsu_fields,expected_errors",
        without_room_cases,
        ids=without_room_ids
    )
    def test_without_room(
            self,
            scenario,
            minsu_fields,
            expected_errors,
            minsu_management_setup,
            page):
        """
        无任何房间的民宿，状态操作集合,备案房间验证以及删除操作
        """
        # 直接使用fixture返回的对象，无需手动调用
        minsu_management_page = minsu_management_setup
        minsu_management_page.go_to_add_minsu_page()
        page.wait_for_load_state("load")
        add_new_minsu_page =  AddNewMinsuPage(page)

        # 1. 新增民宿
        add_new_minsu_page.add_new_minsu(**minsu_fields)
        page.wait_for_load_state("load")
        # 检查房间数量和房间状态
        minsu_management_page.query_minsu(minsu_fields["minsu_name"])
        assert minsu_management_page.check_room_number(0)
        assert minsu_management_page.check_filing_status("未提交")

        #判断民宿显示的操作集合是否正确
        room_number = minsu_management_page.get_room_number()
        filing_status = minsu_management_page.get_filing_status()
        operations, disabled = minsu_management_page.get_room_expected_operations(room_number, filing_status)
        assert minsu_management_page.check_minsu_operations(operations, disabled )
        #民宿删除操作
        minsu_management_page.minsu_delete(minsu_fields["minsu_name"])
        for field, expected_tip in expected_errors.items():
            assert   check_minsu_management_alert_error_messages(minsu_management_page,  field, expected_tip), \
                    (
                        f"❌  场景[{scenario}], 字段 [{field}] 错误提示不匹配 - "
                        f"预期: {expected_tip}, 实际未匹配"
                    )


    # # 场景2：一个房间的民宿，状态操作集合,备案房间验证以及删除操作
    one_room_cases = [
        (
            "one_room",
            {
                **COMMON_minsu_PARAMS,
                "minsu_name": "minsu_with_room",  # 30个字符

            },
            {
                **COMMON_ROOM_PARAMS,
                "ms_name": "minsu_with_room",
                "room_name": "民宿页面备案民宿_1",

            },
            {
                "delete": "民宿下存在有效房间,删除失败!"
            }
        ),

    ]
    one_room_ids = [case[0] for case in one_room_cases]

    @pytest.mark.parametrize(
        "scenario,  minsu_fields, room_fields, expected_errors",
        one_room_cases,
        ids=one_room_ids
    )
    def test_one_room(
            self,
            scenario,
            minsu_fields,
            room_fields,
            expected_errors,
            minsu_management_setup,  # 将fixture作为参数传入，pytest会自动处理其依赖
            page):
        """
        一个房间的民宿，状态操作集合,备案房间验证以及删除(先注销房间再删除民宿)操作
        """
        # 直接使用fixture返回的对象，无需手动调用
        minsu_management_page = minsu_management_setup
        minsu_management_page.go_to_add_minsu_page()
        page.wait_for_load_state("load")
        add_new_minsu_page = AddNewMinsuPage(page)
        step_flag = ""

        # 1. 新增民宿
        add_new_minsu_page.add_new_minsu(**minsu_fields)
        page.wait_for_load_state("load")
        # 2. 备案房间
        time.sleep(2)
        minsu_management_page.minsu_operation("备案房间",minsu_fields["minsu_name"])
        filing_room_page = FilingRoomPage(page)
        filing_room_page.filing_room(test_fields ="all",
                                     property_certificate=JPEG_FIRE_SAFETY_CERTIFICATE,
                                     fire_safety_certificate= JPEG_FIRE_SAFETY_CERTIFICATE,
                                     public_security_registration_form= JPEG_PUBLIC_SECURITY_CERTIFICATE,
                                     bedroom_files= BEDROOM_FILES,
                                     living_room_files=LIVING_ROOM_FILES,
                                     kitchen_files=KITCHEN_FILES,
                                     bathroom_files=BATHROOM_FILES,
                                     **room_fields)
        filing_room_page.submit_form()
        page.wait_for_load_state("load")

        # 检查房间数量和房间状态
        minsu_management_page.query_minsu(minsu_fields["minsu_name"])
        step_flag="查看房间数量"
        actual_room_num = minsu_management_page.check_room_number(1)
        assert actual_room_num, \
            f"❌ [{scenario}] 步骤「{step_flag}」失败：房间数量应为1，实际为「{minsu_management_page.get_room_number()}」"

        step_flag = "查看房间状态"
        actual_status = minsu_management_page.check_filing_status("未提交")
        assert actual_status, \
            f"❌ [{scenario}] 步骤「{step_flag}」失败：备案状态应为「未提交」，实际为「{minsu_management_page.get_filing_status()}」"
        logger.info(f"✅ [{scenario}] 步骤「{step_flag}」成功：房间数量1，状态「未提交」")

        # 判断民宿显示的操作集合是否正确
        step_flag = "校验操作集合"
        logger.info(f"📌 [{scenario}] 开始执行步骤：{step_flag}")
        # 原代码保留：获取房间数量和状态
        room_number = minsu_management_page.get_room_number()
        filing_status = minsu_management_page.get_filing_status()
        operations, disabled_operations = minsu_management_page.get_room_expected_operations(room_number=room_number,
                                                                                    filing_status=filing_status)
        logger.info(f"📌 执行[{scenario}]场景的操作前检查：可用操作={operations}，禁用操作={disabled_operations}")
        # 校验操作集合
        assert minsu_management_page.check_minsu_operations(
            operations=operations,
            disabled_operations=disabled_operations
        ), f"❌ [{scenario}] 步骤「{step_flag}」失败：操作集合校验不通过\n" \
           f"预期可用操作: {operations}\n" \
           f"预期禁用操作: {disabled_operations}\n" \
           f"实际操作集合: {minsu_management_page.get_actual_operations()}"  # 假设存在获取实际操作的方法
        logger.info(f"✅ [{scenario}] 步骤「{step_flag}」成功：操作集合符合预期（可用: {operations}, 禁用: {disabled_operations}）")
        # -------------------------- 新增：操作集合校验成功日志 --------------------------
        logger.info(f"✅ [{scenario}] 步骤「{step_flag}」成功：操作集合符合预期")

        # 民宿删除操作
        # -------------------------- 新增：步骤标记+弹窗关闭处理 --------------------------
        step_flag = "校验民宿删除限制"
        logger.info(f"📌 [{scenario}] 开始执行步骤：{step_flag}")
        # 执行删除操作
        minsu_management_page.minsu_delete(minsu_fields["minsu_name"])
        # 校验删除提示
        for field, expected_tip in expected_errors.items():
            # -------------------------- 新增：断言增强+失败详情 --------------------------
            is_match = check_minsu_management_alert_error_messages(minsu_management_page, field, expected_tip)
            assert is_match, \
                (
                    f"❌ [{scenario}] 步骤「{step_flag}」失败 - "
                    f"字段 [{field}] 错误提示不匹配：预期「{expected_tip}」，实际未匹配"
                )

        logger.info(f"✅ [{scenario}] 步骤「{step_flag}」成功：删除限制提示符合预期")

        #先将该民宿名下的房间删除，就可以删除该民宿
        step_flag = "注销房间+删除民宿"
        logger.info(f"📌 [{scenario}] 开始执行步骤：{step_flag}")
        minsu_management_page.go_to_room_list()
        time.sleep(5)
        room_management_page = RoomManagementPage(page)
        room_management_page.room_operation("注销", room_fields["room_name"])
        # 返回民宿管理页面
        page.get_by_role("menuitem", name="民宿管理").click()
        time.sleep(5)
        minsu_management_page.minsu_delete(minsu_fields["minsu_name"])
        is_match = check_minsu_management_alert_error_messages(minsu_management_page, field, "删除成功")
        assert is_match, \
            (
                f"❌ [{scenario}] 步骤「{step_flag}」失败 - "
                f"字段 [{field}] 错误提示不匹配：预期「删除成功」，实际未匹配"
            )


    # 场景3：提交备案
    submit_filing_room_cases = [
        (
            " submit_filing_room_room",
            {
                **COMMON_minsu_PARAMS,
                "minsu_name": "民宿_提交_备案",  # 30个字符
            },
            {
                **COMMON_ROOM_PARAMS,
                "ms_name": "民宿_提交_备案",
                "room_name": "民宿页面备案民宿_提交",

            },
            {
                "delete": "民宿下存在有效房间,删除失败!"
            }
        )
    ]
    # 测试用例ID列表
    submit_filing_room_ids = [case[0] for case in submit_filing_room_cases]

    @pytest.mark.parametrize(
        "scenario, minsu_fields, room_fields, expected_errors",
        submit_filing_room_cases,
        ids=submit_filing_room_ids
    )
    def test_submit_filing(
            self,
            scenario,
            minsu_fields,
            room_fields,
            expected_errors,
            minsu_management_setup,  # 将fixture作为参数传入，pytest会自动处理其依赖
            page
    ):
        """
        民宿提交备案，以及备案后验证民宿状态以及民宿操作集合
        """
        # 直接使用fixture返回的对象，无需手动调用
        minsu_management_page = minsu_management_setup
        minsu_management_page.go_to_add_minsu_page()
        page.wait_for_load_state("load")
        add_new_minsu_page = AddNewMinsuPage(page)
        step_flag = ""

        # 1. 新增民宿
        add_new_minsu_page.add_new_minsu(**minsu_fields)

        page.wait_for_load_state("load")

        # 2. 备案房间
        time.sleep(2)
        minsu_management_page.query_minsu(minsu_fields["minsu_name"])
        time.sleep(2)
        minsu_management_page.minsu_operation("备案房间", minsu_fields["minsu_name"])
        filing_room_page = FilingRoomPage(page)
        filing_room_page.filing_room(test_fields="all",
                                     property_certificate=JPEG_FIRE_SAFETY_CERTIFICATE,
                                     fire_safety_certificate=JPEG_FIRE_SAFETY_CERTIFICATE,
                                     public_security_registration_form=JPEG_PUBLIC_SECURITY_CERTIFICATE,
                                     bedroom_files=BEDROOM_FILES,
                                     living_room_files=LIVING_ROOM_FILES,
                                     kitchen_files=KITCHEN_FILES,
                                     bathroom_files=BATHROOM_FILES,
                                     **room_fields)
        filing_room_page.submit_form()
        page.wait_for_load_state("load")

        # 提交备案
        assert minsu_management_page.minsu_submit(minsu_fields["minsu_name"])

        # 提交备案后检查房间数量和房间状态
        # 检查房间数量和房间状态
        minsu_management_page.query_minsu(minsu_fields["minsu_name"])
        step_flag = "查看房间数量"
        actual_room_num = minsu_management_page.check_room_number(1)
        assert actual_room_num, \
            f"❌ [{scenario}] 步骤「{step_flag}」失败：房间数量应为1，实际为「{minsu_management_page.get_room_number()}」"

        step_flag = "查看房间状态"
        actual_status = minsu_management_page.check_filing_status("待确认")
        assert actual_status, \
            f"❌ [{scenario}] 步骤「{step_flag}」失败：备案状态应为「待确认」，实际为「{minsu_management_page.get_filing_status()}」"
        logger.info(f"✅ [{scenario}] 步骤「{step_flag}」成功：房间数量1，状态「待确认」")


        # 判断民宿显示的操作集合是否正确
        step_flag = "校验操作集合"
        logger.info(f"📌 [{scenario}] 开始执行步骤：{step_flag}")
        # 获取房间数量和状态
        room_number = minsu_management_page.get_room_number()
        filing_status = minsu_management_page.get_filing_status()
        operations, disabled_operations = minsu_management_page.get_room_expected_operations(room_number=room_number,
                                                                                    filing_status=filing_status)
        logger.info(f"📌 执行[{scenario}]场景的操作前检查：可用操作={operations}，禁用操作={disabled_operations}")
        # 校验操作集合
        assert minsu_management_page.check_minsu_operations(
            operations=operations,
            disabled_operations=disabled_operations
        ), f"❌ [{scenario}] 步骤「{step_flag}」失败：操作集合校验不通过\n" \
           f"预期可用操作: {operations}\n" \
           f"预期禁用操作: {disabled_operations}\n" \
           f"实际操作集合: {minsu_management_page.get_actual_operations()}"  # 假设存在获取实际操作的方法
        logger.info(
            f"✅ [{scenario}] 步骤「{step_flag}」成功：操作集合符合预期（可用: {operations}, 禁用: {disabled_operations}）")
        TestConfig.minsu_pending_confirmation = minsu_fields["minsu_name"]
        logger.info(f"待确认民宿为: {TestConfig.minsu_pending_confirmation}")
        time.sleep(300)

    def test_filing_approval(self,
                             ga_filing_management_setup
                             ):
        """
        公安端对提交备案的民宿通过
        """
        ga_filing_management_page = ga_filing_management_setup
        time.sleep(5)
        logger.info(f"待确认民宿为: {TestConfig.minsu_pending_confirmation}")
        ga_filing_management_page.query_minsu_tr(TestConfig.minsu_pending_confirmation)

        assert ga_filing_management_page.filing_operation("确认","金庸")
        time.sleep(300)

  # 场景4：确认

    def test_approved_filing(
            self,
            minsu_management_setup,  # 将fixture作为参数传入，pytest会自动处理其依赖
            page
    ):
        """备案房间通过后状态集合以及操作集合验证"""
        minsu_management_page = minsu_management_setup
        page.wait_for_load_state("load")
        step_flag = ""

        # 提交备案后检查房间数量和房间状态
        # 检查房间数量和房间状态

        minsu_management_page.query_minsu(TestConfig.minsu_pending_confirmation)
        step_flag = "查看房间数量"
        actual_room_num = minsu_management_page.check_room_number(1)
        assert actual_room_num, \
            f"❌ [备案通过后] 步骤「{step_flag}」失败：房间数量应为1，实际为「{minsu_management_page.get_room_number()}」"

        step_flag = "查看房间状态"
        actual_status = minsu_management_page.check_filing_status("已确认")
        assert actual_status, \
            f"❌ [备案通过后] 步骤「{step_flag}」失败：备案状态应为「已确认」，实际为「{minsu_management_page.get_filing_status()}」"
        logger.info(f"✅ [备案通过后] 步骤「{step_flag}」成功：房间数量1，状态「已确认」")


        # 判断民宿显示的操作集合是否正确
        step_flag = "校验操作集合"
        logger.info(f"📌 [备案通过后] 开始执行步骤：{step_flag}")
        # 获取房间数量和状态
        room_number = minsu_management_page.get_room_number()
        filing_status = minsu_management_page.get_filing_status()
        operations, disabled_operations = minsu_management_page.get_room_expected_operations(room_number=room_number,
                                                                                    filing_status=filing_status)
        logger.info(f"📌 执行[备案通过后]场景的操作前检查：可用操作={operations}，禁用操作={disabled_operations}")
        # 校验操作集合
        assert minsu_management_page.check_minsu_operations(
            operations=operations,
            disabled_operations=disabled_operations
        ), f"❌ [备案通过后] 步骤「{step_flag}」失败：操作集合校验不通过\n" \
           f"预期可用操作: {operations}\n" \
           f"预期禁用操作: {disabled_operations}\n"
        logger.info(
            f"✅ [备案通过后] 步骤「{step_flag}」成功：操作集合符合预期（可用: {operations}, 禁用: {disabled_operations}）")


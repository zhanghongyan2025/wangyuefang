import re
import time
from re import search

from playwright.sync_api import Playwright, sync_playwright, expect
from tests.utils.page_utils import upload_file, get_label_corresponding_element
from tests.utils.page_utils import *
from playwright.async_api import Playwright

from conf.logging_config import logger
from tests.utils.page_utils import *
from tests.utils.validator import *
from playwright.sync_api import Page, sync_playwright

import re
import os
import time
import logging


class louYuManagementPage:
    """房间管理页面自动化测试类，用于处理与房间管理相关的UI操作和验证"""

    def __init__(self, page: Page):
        """
        初始化RoomManagePage类

        Args:
            page (Page): Playwright的Page对象，用于操作浏览器页面
        """
        self.page = page
        self.add_Ly_button = self.page.get_by_role("button", name="新增楼宇")
        self.expand_query_button = self.page.get_by_role("button", name="自定义查询")
        self.query_input = self.page.locator('//input[@placeholder="请输入楼宇名称"]')
        self.query_button = self.page.get_by_role("button", name="搜索")
        self.reset_button = self.page.get_by_role("button", name="重置")
        self.ly_list = self.page.locator("tbody")


    def add_louyu(self, louyu_name: str):

      # 等待并点击新增楼宇按钮，增加重试机制
      self.add_Ly_button.click()
      time.sleep(1)
      self.page.locator('div[aria-label="新增楼宇"] input[placeholder="请输入楼宇名称"]').fill(louyu_name)
      self.page.get_by_role("button", name="确 定").click()

    def query_louyu(self, louyu_name: str) -> int or None:
        """
        查询楼宇所在行的索引（下标）

        Args:
            louyu_name (str): 要查询的楼宇名称

        Returns:
            int: 找到的楼宇所在行的索引（从1开始计数）
            None: 未找到楼宇时返回None
        """
        result = None
        if louyu_name:
            # query_target_name返回匹配行的索引（从1开始计数）
            result = query_target_name_index(self.page, "楼宇", louyu_name)

        # 直接返回查询结果（int类型的行索引或None）
        return result

    def louyu_delete(self, louyu_name: str) -> bool:
        """
        基于query_louyu获取的行索引，执行楼宇删除操作
        Args:
            louyu_name (str): 待删除的楼宇名称
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        TARGET_COLUMN = 2  # 操作按钮所在列（与原逻辑一致，无需修改）

        try:
            logger.info(f"开始执行楼宇删除操作，目标楼宇: '{louyu_name or 'N/A'}'")

            # 1. 调用query_louyu获取楼宇行索引（核心：动态获取行号，无需手动传target_row）
            louyu_row_index = self.query_louyu(louyu_name)
            if louyu_row_index is None:
                logger.error(f"待删除的楼宇[{louyu_name}]不存在，终止删除操作")
                return False
            logger.info(f"查询确认：楼宇[{louyu_name}]存在，位于第 {louyu_row_index} 行")

            # 2. 转换为表格定位的“0基索引”（query_louyu返回1基行号，定位需减1）
            target_row = louyu_row_index - 1
            logger.info(
                f"正在查找第 {louyu_row_index} 行（定位索引：{target_row}），第 {TARGET_COLUMN + 1} 列的 '删除' 按钮...")

            # 3. 根据动态获取的target_row定位删除按钮
            delete_button = get_table_cell_or_button(self.page, target_row, TARGET_COLUMN, "删除")
            if not delete_button:
                logger.error(f"未找到楼宇[{louyu_name}]（第{louyu_row_index}行）的'删除'按钮")
                return False

            # 4. 点击删除按钮并等待弹窗
            delete_button.click()
            logger.info(f"楼宇[{louyu_name}]的'删除'按钮点击成功，等待确认弹窗...")
            time.sleep(2)

            # 5. 处理删除确认弹窗
            confirm_message = f'是否确认删除"{louyu_name}"楼宇吗？'
            logger.info(f"正在确认删除对话框: '{confirm_message}'")

            confirm_btn = checkTipDialog(self.page, confirm_message, "确定", "取消", "confirm")
            if not confirm_btn:
                logger.error(f"未找到删除确认对话框中的'确定'按钮")
                return False
            confirm_btn.click()
            logger.info(f"已确认删除楼宇[{louyu_name}]")

            # 6. 验证删除结果（通过操作提示判断是否成功）
            if operation_alert_error(self.page, "删除成功"):
                logger.info(f"✅ 楼宇[{louyu_name}]删除成功")

            else:
                logger.error(f"❌ 楼宇[{louyu_name}]删除失败，未捕获到'删除成功'提示")
                return False

        except Exception as e:
            logger.error(f"❌ 楼宇[{louyu_name}]删除发生错误：{str(e)}", exc_info=True)
            return False

    def modified_louyu(self, original_louyu_name: str, target_louyu_name: str) -> bool:
        """
        执行楼宇修改操作（新增前置查询校验）
        Args:
            original_louyu_name (str): 待修改的原楼宇名称（用于前置查询确认）
            target_louyu_name (str): 修改后的目标楼宇名称
        Returns:
            bool: 修改操作触发成功返回True，失败返回False
        """
        TARGET_COLUMN = 2
        try:
            logger.info(f"开始执行楼宇修改：原名称[{original_louyu_name}] → 目标名称[{target_louyu_name}]")
            time.sleep(2)

            # 1. 调用query_louyu获取楼宇行索引（核心：动态获取行号，无需手动传target_row）
            louyu_row_index = self.query_louyu(original_louyu_name)
            if louyu_row_index is None:
                logger.error(f"待修改的楼宇[{original_louyu_name}]不存在，终止修改操作")
                return False
            else:
                logger.info(f"查询确认：楼宇[{original_louyu_name}]存在，位于第 {louyu_row_index} 行")

                # 3. 根据动态获取的target_row定位删除按钮
                target_row = louyu_row_index - 1
                modify_button = get_table_cell_or_button(self.page, target_row, TARGET_COLUMN, "修改")
                modify_button.click()
                time.sleep(1)
                # 2. 校验“修改楼宇”弹窗是否存在（避免弹窗未触发导致操作失败）
                modify_dialog = self.page.get_by_role("dialog", name="修改楼宇")
                if not modify_dialog.is_visible(timeout=5000):
                    logger.error(f"未找到'修改楼宇'弹窗，请先触发修改按钮")
                    return False
                logger.info(f"确认'修改楼宇'弹窗已显示，开始输入新名称")

                # 3. 执行修改操作（保留原填充和点击逻辑，增加输入合法性日志）
                name_input = modify_dialog.get_by_placeholder("请输入楼宇名称")
                name_input.fill(target_louyu_name)
                logger.info(f"已在弹窗输入新楼宇名称：{target_louyu_name}")

                confirm_btn = self.page.get_by_role("button", name="确 定")
                if not confirm_btn.is_visible():
                    logger.error(f"'修改楼宇'弹窗中的'确 定'按钮不可见")
                    return False
                confirm_btn.click()
                logger.info(f"已点击'确 定'按钮，等待修改结果")
                return True

        except Exception as e:
            logger.error(f"楼宇修改操作发生错误：{str(e)}", exc_info=True)
            return False

    def louyu_name_error(self, expected_text):
        return get_element_corresponding_error_tip(
            self.page.get_by_text("楼宇名称", exact=True), '../..//div[contains(@class, "el-form-item__error")]', expected_text
        )

    def  louyu_operation_error(self, expected_text):
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched

    def louyu_operation_success_alert(self, expected_text):
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched

    def louyu_name_alert_error(self, expected_text):
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched

    # def operation_alert_error(self, expected_text):
    #     is_matched, actual_text = check_alert_text(self.page, expected_text)
    #     return is_matched


# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://192.168.40.61:3333/login_fd?redirect=%2Ffangwu_fangdong%2Ffangjian%2Fadd")
#     file_path = '../data/evidence_files/1.png'
#     # 登录逻辑
#     page.get_by_role("textbox", name="账号").fill("fenghuang_123")
#     page.get_by_role("textbox", name="密码").fill("Aa123123!")
#     page.get_by_role("button", name="登 录").click()
#
#     # 导航到民宿管理页面
#     page.get_by_role("menuitem", name="房屋管理").click()
#     page.get_by_role("link", name="楼宇管理").click()
#
#     louyu_management_page = louYuManagementPage(page)
#     target_louyu = louyu_management_page.query_louyu("1")
#     if target_louyu is not None:
#         louyu_management_page.louyu_operation("1", "删除")
#         checkTipDialog(page, '是否确认删除"1"楼宇吗？', "确定", "取消", "confirm").click()
#
#     # lou_yu_manage_page.add_louyu(**louyu_info)
#     # lou_yu_manage_page.louyu_option("1","删除")
#     # checkTipDialog(page, '是否确认删除"1"楼宇吗？',"确定", "取消","confirm").click()
#     # lou_yu_manage_page.page.get_by_role("menuitem", name="房间管理").click()
#     # detail_button = get_table_cell_or_button(lou_yu_manage_page.page, 0, 7, "详情")
#     # detail_button.click()
#     # check_label_corresponding_input_value(lou_yu_manage_page.page, "楼宇", "123456789012345678901234567888")
#     # lou_yu_manage_page.query_louyu("一栋一单元")
#     # time.sleep(2)
#     # reset_btn=lou_yu_manage_page.page.locator('button:has(span:text("重置"))')
#     # reset_btn.wait_for(state="visible", timeout=5000)
#
#     # search_types=["楼宇名称"]
#     # is_search_reset_successful(
#     #     lou_yu_manage_page.page,search_types
#     # )
#
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
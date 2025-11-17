import time
from playwright.sync_api import Page, expect

from tests.pages.fd.filing_room_page import FilingRoomPage
from tests.utils.page_utils import *
from tests.pages.fd.add_new_minsu import AddNewMinsuPage
from playwright.sync_api import Page, expect, Playwright, sync_playwright

class RoomManagementPage:
    def __init__(self, page: Page):
        self.page = page

        # 查询区域折叠/展开按钮
        self.expand_query_button = self.page.get_by_role("button", name="自定义查询")
        self.collapse_query_button = self.page.get_by_role("button", name="收起查询")

        # 搜索区域元素
        self.minsu_name_search_input = self.page.get_by_role("textbox", name="请选择民宿名称")
        self.room_name_search_input = self.page.get_by_role("textbox", name="请输入房间名称")
        self.room_status_search_input = self.page.get_by_role("textbox", name="请选择房间状态")
        self.search_button = self.page.get_by_role("button", name="搜索")
        self.reset_button = self.page.get_by_role("button", name="重置")

        # 功能按钮
        self.add_minsu_button = self.page.get_by_role("button", name="备案房间")

    def query_room(self, room_name: str) -> bool:

        result = False
        if room_name is not None:
            result = query_target_name_tr(self.page, "房间", room_name)
            # 检查结果是否为None，非None则返回True，否则返回False
        return result is not None

    def go_to_filling_room_page(self):
        """点击备案房间按钮，进入新增页面并验证URL跳转"""
        try:
            # 获取当前页面URL用于拼接新增页面地址
            current_url = self.page.url.rstrip('/')  # 移除可能存在的尾部斜杠
            add_minsu_url = f"{current_url}/add"  # 拼接生成新增页面URL
            self.page.wait_for_timeout(2000)
            # 点击新增民宿按钮
            self.add_minsu_button.click()

            # 验证是否跳转到正确的新增页面
            # expect(self.page).to_have_url(add_minsu_url)

            # 返回新增民宿页面操作对象
            return FilingRoomPage(self.page)

        except Exception as e:
            # 发生异常时尝试返回原页面
            if self.page.url != current_url:
                self.page.go_back()
            raise e

    def get_room_status(self, row_index: int = 0) -> str:
        """
        获取指定行房间的备案状态
        Args:
            row_index: 房间所在行索引（默认第1行，索引0）
        Returns:
            str: 备案状态文本，如果获取失败返回空字符串
        """
        try:
            # 获取指定行的备案状态单元格（第7列，索引6）
            status_cell = get_table_cell_or_button(self.page, row_index, 6)
            if status_cell is None:
                logger.warning(f"未找到第{row_index + 1}行房间的状态单元格")
                return ""

            # 提取并清洗状态文本
            status_text = status_cell.text_content(timeout=2000).strip()
            return status_text if status_text else ""
        except TimeoutError:
            logger.error(f"提取第{row_index + 1}行房间备案状态超时")
            return ""
        except Exception as e:
            logger.error(f"获取备案状态发生错误：{str(e)}")
            return ""

    def get_room_expected_status(self, operation: str) -> str:
        """
        获取特定操作之后房间对应的预期状态
        Args:
            operation: 房间操作，支持"禁用"、"恢复"、"注销"
        Returns:
            str: 操作后的预期状态文本，如果操作不支持则返回空字符串
        """
        # 定义操作与预期状态的映射关系
        operation_status_map = {
            "禁用": "禁用",
            "恢复": "正常",
            "注销": "注销"
        }

        # 返回与操作对应的状态，如果操作不在映射表中则返回空字符串
        return operation_status_map.get(operation, "")

    def check_room_status(self, expect_status: str) -> bool:
        """
        校验目标房间的状态是否与预期一致
        （针对包含多个button元素的单元格进行处理）

        Args:
            expect_status: 预期的房间状态，如["正常", "禁用", "注销"]等

        Returns:
            bool: 所有预期状态存在且符合预期返回True；否则返回False
        """
        try:

            # 1. 获取状态单元格元素
            status_cell = get_table_cell_or_button(self.page, 0, 6)
            if not status_cell:
                logger.error("❌ 未获取到状态cell")
                return False

            # 2. 提取文本内容
            actual_status = status_cell.text_content().strip()
            if actual_status:
                logger.debug(f"发现状态: {actual_status}")

            # 4. 检查预期操作是否都存在

            if actual_status != expect_status:
                logger.error(f"❌ 缺少预期状态: {expect_status}")
                logger.info(f"实际存在的状态: {actual_status}")
                return False

            logger.info(f"✅ 预期状态存在: {actual_status}")
            return True
        except Exception as e:
            logger.error(f"❌ 状态检查过程中发生错误: {str(e)}")
            return False

    def room_operation(self,  operation: str, room_name: str=None,) -> bool:
        """
        对目标房间进行操作
        （注：默认通过 get_table_cell_or_button(0,7) 获取单元格，需确保该函数返回第1行第8列的备案状态单元格）

        Args:
            operation: 房间操作，修改详情禁用注销等

        Returns:
            bool: 操作成功 True；获取失败 False
        """
        # 1. 定义常量，避免魔法数字和硬编码字符串，提高可读性和可维护性
        TARGET_ROW = 0
        TARGET_COLUMN = 7
        VALID_OPERATIONS = {"详情", "禁用", "恢复", "注销"}

        # 2. 参数校验，确保操作合法
        if operation not in VALID_OPERATIONS:
            logger.error(f"无效的房间操作: '{operation}'。合法操作包括: {VALID_OPERATIONS}")
            return False

        try:
            logger.info(f"开始执行房间操作: '{operation}'，目标房间: '{room_name or 'N/A'}'")

            # 3. 尝试获取并点击操作按钮
            logger.info(f"正在查找第 {TARGET_ROW + 1} 行，第 {TARGET_COLUMN + 1} 列的 '{operation}' 按钮...")
            operation_button = get_table_cell_or_button(self.page, TARGET_ROW, TARGET_COLUMN, operation)

            if not operation_button:
                logger.error(f"获取 '{operation}' 按钮失败。")
                return False

            operation_button.click()
            logger.info(f"'{operation}' 按钮点击成功，等待页面响应...")
            time.sleep(2)  # 等待页面加载或弹窗出现

            # 4. 根据不同操作执行后续逻辑
            if operation == "详情":
                # 校验房间名称
                if not room_name:
                    logger.warning("执行'详情'操作时，建议提供room_name以进行验证。")
                    return False

                actual_room_name = get_label_corresponding_input(self.page, "房间名称").input_value()
                logger.info(f"获取到的实际房间名称为: '{actual_room_name}'")

                if actual_room_name == room_name:
                    logger.info(f"房间名称校验成功: '{actual_room_name}' == '{room_name}'")
                    return True
                else:
                    logger.error(f"房间名称校验失败: '{actual_room_name}' != '{room_name}'")
                    return False

            elif operation in ["禁用", "恢复", "注销"]:
                # 处理需要确认的操作
                confirm_message = f'是否确认{operation}房间名称为"{room_name}"的数据项？'
                logger.info(f"正在确认对话框: '{confirm_message}'")

                # 假设 checkTipDialog 会返回确认按钮并点击
                checkTipDialog(self.page, confirm_message, "确定", "取消", "confirm").click()
                logger.info(f"已确认 '{operation}' 操作。")

                return operation_alert_error(self.page,f"{operation}成功")

        except Exception as e:
            logger.error(f"房间{operation}发生错误：{str(e)}")
            return False

    def get_room_expected_operations(self, room_status: str) -> list[str]:
        """
        返回目标状态房间的操作集合

        Args:
            room_status: 房间状态

        Returns:
            list: 该状态对应的所有操作集合
        """
        operations_map = {
            "注销": ["详情"],
            "正常": ["修改", "禁用", "注销", "详情"],
            "禁用": ["修改", "恢复", "注销", "详情"]
        }
        # 返回对应的操作集合，如果状态不存在则返回空列表
        return operations_map.get(room_status, [])

    def check_room_operations(self, expected_operations: list) -> bool:
        """
               查看房间对应操作是否与预期相符

               Args:
                   expected_operations: 期望操作集合
               Returns:
                   bool: 所有预期操作集合存在且符合预期返回True；否则返回False

               Raises:
                   ValueError: 当房间数量为负数或备案状态无效时抛出
               """
        try:
            # 1. 获取包含所有操作按钮的单元格元素
            operations_container = get_table_cell_or_button(self.page, 0, 7)
            if not operations_container:
                logger.error("❌ 未获取到操作按钮容器")
                return False

            # 2. 从容器中获取所有button元素
            buttons = operations_container.locator("button.el-button").all()
            if not buttons:
                logger.error("❌ 未在容器中找到任何按钮")
                return False

            # 3. 提取所有按钮的文本内容和状态
            actual_operations = []
            for button in buttons:
                op_text = button.text_content().strip()

                if op_text:
                    logger.debug(f"发现操作按钮: {op_text}")
                    actual_operations.append(op_text)

            # 4. 检查预期操作是否都存在
            missing_operations = [op for op in expected_operations if op not in actual_operations]
            if missing_operations:
                logger.error(f"❌ 缺少预期操作: {missing_operations}")
                logger.info(f"实际存在的操作: {actual_operations}")
                return False

            logger.info(f"✅ 所有预期操作都存在: {expected_operations}")
            return True
        except Exception as e:
            logger.error(f"  操作检查过程中发生错误: {str(e)}")
            return False

    # def operation_alert_error(self, expected_text):
    #     is_matched, actual_text = check_alert_text(self.page, expected_text)
    #     return is_matched



# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://192.168.40.61:3333/login_fd?redirect=%2Ffangwu_fangdong%2Fminsu")
#     page.get_by_role("textbox", name="账号").fill("fenghuang_123")
#     page.get_by_role("textbox", name="密码").fill("Aa123123!")
#     page.get_by_role("button", name="登 录").click()
#     page.get_by_role("menuitem", name="房屋管理").click()
#     page.get_by_role("link", name="民宿管理").click()
#     minsu_management_page = MinsuManagementPage(page)
#     # # minsu_mangement_page.minsu_operation("备案房间","测试民宿")
#     # minsu_mangement_page.minsu_operation("删除", "测试民宿")
#     minsu_management_page.query_minsu("民宿_房间_0_09080100")
#     room_number = minsu_management_page.get_room_number()
#     filing_status = minsu_management_page.get_filing_status()
#     minsu_management_page.minsu_delete("民宿_房间_0_09080100")
#
#     # minsu_mangement_page.check_room_number(int(5))
#     # minsu_mangement_page.check_filing_status("已确认")
#     # minsu_mangement_page.minsu_operation("备案房间","手持机民宿")
#     # room_register_page = RoomRegisterPage(page)
#     # room_register_page.register_room(
#     #     property_certificate=JPG_PROPERTY_CERTIFICATE,
#     #     fire_safety_certificate=JPG_PROPERTY_CERTIFICATE,
#     #     bedroom_files=BATHROOM_FILES,
#     #     living_room_files=LIVING_ROOM_FILES,
#     #     kitchen_files=KITCHEN_FILES,
#     #     bathroom_files=KITCHEN_FILES,
#     #     ms_name="手持机民宿",
#     #     test_fields="",
#     #     **ROOM_PARAMS)
#     # time.sleep(1)
#     # room_register_page.submit_form()
#     # minsu_mangement_page.check_room_number(int(6))
#     # minsu_mangement_page.check_filing_status("未提交")
#     # minsu_mangement_page.minsu_operation("提交", "手持机民宿")
#     # target_minsu="手持机民宿"
#     # # 在变量前后添加转义的双引号 \"
#     # expected_text = f"\"{target_minsu}\"提交后不能修改民宿备案及相关房间，确定要提交备案吗？"
#     # checkTipDialog(minsu_mangement_page.page, expected_text,"确定","取消", "confirm").click()
#     # minsu_mangement_page.check_filing_status("待确认")
#
#     # context.close()
#     # browser.close()
#
# with sync_playwright() as playwright:
#     run(playwright)


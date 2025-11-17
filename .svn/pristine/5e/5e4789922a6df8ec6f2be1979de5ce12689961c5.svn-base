import time

from playwright.sync_api import Page, expect
from tests.utils.page_utils import *
from tests.pages.fd.add_new_minsu import AddNewMinsuPage
from playwright.sync_api import Page, expect, Playwright, sync_playwright

class MinsuManagementPage:
    def __init__(self, page: Page):
        self.page = page

        # 查询区域折叠/展开按钮
        self.expand_query_button = self.page.get_by_role("button", name="自定义查询")
        self.collapse_query_button = self.page.get_by_role("button", name="收起查询")

        # 搜索区域元素
        self.minsu_name_search_input = self.page.get_by_role("textbox", name="请输入民宿名称")
        self.administrative_area_search_input = self.page.get_by_role("textbox", name="请选择行政区划")
        self.person_in_charge_input = self.page.get_by_role("textbox", name="请输入负责人姓名")
        self.search_button = self.page.get_by_role("button", name="搜索")
        self.reset_button = self.page.get_by_role("button", name="重置")

        # 功能按钮
        self.add_minsu_button = self.page.get_by_role("button", name=" 新增民宿")

    def query_minsu(self, minsu_name: str) -> int or None:
        """
        查询民宿所在行的索引（下标）

        Args:
            minsu_name (str): 要查询的民宿名称

        Returns:
            int: 找到的民宿所在行的索引（从1开始计数）
            None: 未找到民宿时返回None
        """
        result = None
        if minsu_name:
            # query_target_name返回匹配行的索引（从1开始计数）
            result = query_target_name_index(self.page, "民宿", minsu_name)

        # 直接返回查询结果（int类型的行索引或None）
        return result

    def go_to_add_minsu_page(self):
        """点击新增民宿按钮，进入新增页面并验证URL跳转"""
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
            return AddNewMinsuPage(self.page)

        except Exception as e:
            # 发生异常时尝试返回原页面
            if self.page.url != current_url:
                self.page.go_back()
            raise e

    def go_to_room_list(self):
        """
        导航到房间列表页面（仅包含点击操作）

        Returns:
            bool: 导航操作完成返回True，发生错误返回False
        """
        try:

            # 假设房间数量在第0行第8列（索引从0开始）
            room_num_cell = get_table_cell_or_button(self.page, 0, 7)

            room_num_cell.locator("//span").click(timeout=3000)
            self.page.wait_for_load_state("networkidle", timeout=30000)

            logger.info("✅ 已成功导航到房间列表页面")

        except Exception as e:
            logger.error(f"❌ 导航到房间列表页面失败：{str(e)}")

    def get_room_number(self) -> int:
        """
        获取当前列表中的房间总数
        Returns:
            int: 房间数量，如果获取失败返回0
        """
        try:
            # 尝试通过表格特定单元格获取房间数量
            # 假设房间数量在第0行第8列（索引从0开始）
            room_num_text = get_table_cell_or_button(self.page, 0, 7).text_content().strip()

            # 提取数字部分
            import re
            match = re.search(r'\d+', room_num_text)
            if match:
                return int(match.group())

            # 如果第一个位置获取失败，尝试其他可能的行索引
            # 例如尝试第1行
            room_num_text =get_table_cell_or_button(self.page, 0, 8).strip()
            match = re.search(r'\d+', room_num_text)
            if match:
                return int(match.group())

            # 如果表格中没有直接显示总数，尝试统计行数作为房间数量
            row_count = 0
            # 循环获取行，直到获取失败
            while True:
                try:
                    # 尝试获取当前行，验证行是否存在
                    get_table_cell_or_button(self.page, row_count, 0)
                    row_count += 1
                except:
                    break

            return row_count

        except Exception as e:
            logger.error(f"获取房间数量失败: {str(e)}")
            return 0

    def check_room_number(self, expected_number: int) -> bool:
        """
        校验房间数量是否与预期一致
        Args:
            expected_number: 预期的房间数量
        Returns:
            bool: 数量一致返回True，否则返回False
        """
        actual_number = self.get_room_number()
        try:
            if actual_number == expected_number:
                logger.info(f"✅ 房间数量校验通过：实际「{actual_number}」= 预期「{expected_number}」")
                return True
            else:
                logger.error(f"❌ 房间数量校验失败：实际「{actual_number}」≠ 预期「{expected_number}」")
                return False
        except Exception as e:
            logger.error(f"房间数量校验发生错误：{str(e)}")
            return False

    def get_filing_status(self, row_index: int = 0) -> str:
        """
        获取指定行房间的备案状态
        Args:
            row_index: 房间所在行索引（默认第1行，索引0）
        Returns:
            str: 备案状态文本，如果获取失败返回空字符串
        """
        try:
            # 获取指定行的备案状态单元格（第7列，索引6）
            status_cell = get_table_cell_or_button(self.page, row_index, 8)
            if status_cell is None:
                logger.warning(f"未找到第{row_index + 1}行房间的备案状态单元格")
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

    def check_filing_status(self, expected_status: str, row_index: int = 0) -> bool:
        """
        校验指定行房间的备案状态是否与预期一致
        Args:
            expected_status: 预期的备案状态（如"已确认"、"未提交"）
            row_index: 房间所在行索引（默认第1行，索引0）
        Returns:
            bool: 状态一致返回True，否则返回False
        """
        actual_status = self.get_filing_status(row_index)

        if not actual_status:
            logger.error(f"❌ 备案状态校验失败：无法获取第{row_index + 1}行房间的状态")
            return False

        if actual_status == expected_status:
            logger.info(f"✅ 备案状态校验通过：实际「{actual_status}」= 预期「{expected_status}」")
            return True
        else:
            logger.error(f"❌ 备案状态校验失败：实际「{actual_status}」≠ 预期「{expected_status}」")
            return False

    def minsu_operation(self,  operation: str, minsu_name: str=None,) -> bool:
        """
        校验目标民宿的备案状态是否与预期一致
        （注：默认通过 get_table_cell_or_button(0,8) 获取单元格，需确保该函数返回第1行第9列的备案状态单元格）

        Args:
            operation: 民宿操作，修改删除等

        Returns:
            bool: 操作成功 True；获取失败 False
        """
        status_text = None  # 初始化状态文本变量，避免未定义报错
        try:
            # 1. 尝试获取备案状态对应的表格单元格（第1行第9列：索引0行、8列）
            operation_button = get_table_cell_or_button(self.page, 0, 9, operation)

            # 2. 校验单元格是否获取成功
            if operation_button is None:
                return False

            operation_button.click()
            time.sleep(2)
            # 4. 如果是备案房间操作，检查并填写民宿名称
            if operation == "备案房间":
                if not minsu_name:
                    logger.error("❌ 执行备案房间操作时，必须提供minsu_name参数")
                    return False

                # 假设页面上民宿标签对应的输入框有特定选择器，这里需要根据实际情况调整
                minsu_input = get_label_corresponding_input(self.page, "民宿名称")

                # 检查输入框是否存在
                if not minsu_input.is_visible():
                    logger.error("❌ 未找到民宿名称输入框")
                    return False

                # 获取当前输入框的值
                current_name = minsu_input.input_value()

                # 校验输入框内容是否与预期一致
                if current_name != minsu_name:
                    logger.error(f"⚠️ 民宿名称不匹配，预期: {minsu_name}, 实际: {current_name}")
                    return False
                else:
                    logger.info(f"✅ 民宿名称验证通过: {minsu_name}")

            # 其他操作的处理逻辑可以在这里添加

            return True

        except Exception as e:
            logger.error(f"民宿{operation}发生错误：{str(e)}")
            return False

    def minsu_submit(self,  minsu_name: str)-> bool:
        searchedTr = query_target_name_tr(self.page, "民宿", minsu_name)

        if not searchedTr:
            logger.info(f" 未找到名为'{minsu_name}'的民宿行元素")
            return False

        try:
            # 更精确的XPath定位，基于实际HTML结构
            # 定位到包含按钮的td，再找到对应操作的按钮
            operation_button = searchedTr.locator(
                f"xpath=.//td[10]//button[span[text()='提交']]"
            )

            operation_button.wait_for(state="visible", timeout=5000)
            operation_button.click()
            checkTipDialog(
                page=self.page,
                expected_text=f'"{minsu_name}"提交后不能修改民宿备案及相关房间，确定要提交备案吗？',
                confirm_text="确定",
                cancel_text="取消",
                operation="confirm"
            ).click()
            logger.info(f"成功点击'{minsu_name}'行的提交按钮")
            time.sleep(1)
            return True

        except Exception as e:
            logger.error(f"点击'{minsu_name}'行的'提交'按钮失败: {str(e)}")
            # 调试信息：输出当前tr的html内容帮助分析问题
            logger.debug(f"当前行HTML: {searchedTr.inner_html()}")

    # def minsu_delete(self,  minsu_name: str):
    #     searchedTr = query_target_name(self.page, "民宿", minsu_name)
    #
    #     if not searchedTr:
    #         logger.info(f" 未找到名为'{minsu_name}'的民宿行元素")
    #         return
    #
    #     try:
    #         # 更精确的XPath定位，基于实际HTML结构
    #         # 定位到包含按钮的td，再找到对应操作的按钮
    #         operation_button = searchedTr.locator(
    #             f"xpath=.//td[10]//button[span[text()='删除']]"
    #         )
    #
    #         operation_button.wait_for(state="visible", timeout=5000)
    #         operation_button.click()
    #         checkTipDialog(
    #             page=self.page,
    #             expected_text=f'是否确认删除民宿名称为"{minsu_name}"的数据项？',
    #             confirm_text="确定",
    #             cancel_text="取消",
    #             operation="confirm"
    #         ).click()
    #         logger.info(f"成功点击'{minsu_name}'行的删除按钮")
    #         time.sleep(1)
    #
    #     except Exception as e:
    #         logger.error(f"点击'{minsu_name}'行的'删除'按钮失败: {str(e)}")
    #         # 调试信息：输出当前tr的html内容帮助分析问题
    #         logger.debug(f"当前行HTML: {searchedTr.inner_html()}")

    def minsu_delete(self, minsu_name: str) -> bool:
        """
        基于query_民宿获取的行索引，执行民宿删除操作
        Args:
            minsu_name (str): 待删除的民宿名称
        Returns:
            bool: 删除成功返回True，失败返回False
        """
        TARGET_COLUMN = 9 # 操作按钮所在列

        try:
            logger.info(f"开始执行民宿删除操作，目标民宿: '{minsu_name or 'N/A'}'")

            # 1. 调用query_minsu获取民宿行索引（核心：动态获取行号，无需手动传target_row）
            minsu_row_index = self.query_minsu(minsu_name)
            if minsu_row_index is None:
                logger.error(f"待删除的民宿[{minsu_name}]不存在，终止删除操作")
                return False
            logger.info(f"查询确认：民宿[{minsu_name}]存在，位于第 {minsu_row_index} 行")

            # 2. 转换为表格定位的“0基索引”（query_louyu返回1基行号，定位需减1）
            target_row = minsu_row_index - 1
            logger.info(
                f"正在查找第 {minsu_row_index} 行（定位索引：{target_row}），第 {TARGET_COLUMN + 1} 列的 '删除' 按钮...")

            # 3. 根据动态获取的target_row定位删除按钮
            delete_button = get_table_cell_or_button(self.page, target_row, TARGET_COLUMN, "删除")
            if not delete_button:
                logger.error(f"未找到民宿[{minsu_name}]（第{minsu_row_index}行）的'删除'按钮")
                return False

            # 4. 点击删除按钮并等待弹窗
            delete_button.click()
            logger.info(f"民宿[{minsu_name}]的'删除'按钮点击成功，等待确认弹窗...")
            time.sleep(2)

            # 5. 处理删除确认弹窗
            confirm_message = f'是否确认删除民宿名称为"{minsu_name}"的数据项？'
            logger.info(f"正在确认删除对话框: '{confirm_message}'")

            confirm_btn = checkTipDialog(self.page, confirm_message, "确定", "取消", "confirm")
            if not confirm_btn:
                logger.error(f"未找到删除确认对话框中的'确定'按钮")
                return False
            confirm_btn.click()
            logger.info(f"已确认删除民宿[{minsu_name}]")

            # 6. 验证删除结果（通过操作提示判断是否成功）
            if operation_alert_error(self.page, "删除成功"):
                logger.info(f"✅ 民宿[{minsu_name}]删除成功")

            else:
                logger.error(f"❌ 民宿[{minsu_name}]删除失败，未捕获到'删除成功'提示")
                return False

        except Exception as e:
            logger.error(f"❌ 民宿[{minsu_name}]删除发生错误：{str(e)}", exc_info=True)
            return False

    def get_room_expected_operations(self, room_number: int, filing_status: str) -> tuple[list[str], list[str]]:
        """
        根据房间数量和备案状态，返回对应的操作集合及禁用的操作

        Args:
            room_number: 房间数量
            filing_status: 备案状态，可选值包括"未提交"、"待确认"、"确认"

        Returns:
            tuple: 包含两个列表的元组，第一个列表是操作集合，第二个列表是禁用的操作

        Raises:
            ValueError: 当房间数量为负数或备案状态无效时抛出
        """
        operations = []
        disabled = []

        if room_number < 0:
            raise ValueError(f"房间数量不能为负数: {room_number}")

        if room_number == 0:
            if filing_status == "未提交":
                operations = ["备案房间", "提交", "修改", "详情", "删除"]
                disabled = ["提交"]
            else:
                raise ValueError(f"房间数量为0时，备案状态必须为'未提交'，实际为'{filing_status}'")

        elif room_number > 0:
            if filing_status == "待确认":
                operations = ["详情"]
                disabled = []
            elif filing_status == "已确认":
                operations = ["备案房间","详情", "删除"]
                disabled = []
            elif filing_status == "未提交":
                operations = ["备案房间", "提交", "修改", "详情", "删除"]  # 根据需求调整操作集合
                disabled = []
            else:
                raise ValueError(
                    f"房间数量大于0时，备案状态必须为'待确认'、'已确认'或'未提交'，实际为'{filing_status}'"
                )

        return operations, disabled

    def check_minsu_operations(self, operations: list,
                               disabled_operations: list = None) -> bool:
        """
        校验目标民宿的操作按钮是否与预期一致，包括存在性和禁用状态
        （针对包含多个button元素的单元格进行处理）

        Args:
            operations: 预期的民宿操作列表，如["备案房间", "修改"]等
            minsu_name: 民宿名称，备案房间操作时必填
            disabled_operations: 预期应处于禁用状态的操作列表，如["提交"]

        Returns:
            bool: 所有预期操作都存在且禁用状态符合预期返回True；否则返回False
        """
        try:
            # 初始化禁用操作列表（默认空列表）
            disabled_operations = disabled_operations or []

            # 1. 获取包含所有操作按钮的单元格元素
            operations_container = get_table_cell_or_button(self.page, 0, 9)
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
            operation_status = {}  # 存储操作的禁用状态：{操作名: 是否禁用}
            for button in buttons:
                op_text = button.text_content().strip()
                is_disabled = button.get_attribute("disabled") is not None

                if op_text:
                    status = "禁用" if is_disabled else "可用"
                    logger.debug(f"发现操作按钮: {op_text} ({status})")
                    actual_operations.append(op_text)
                    operation_status[op_text] = is_disabled

            # 4. 检查预期操作是否都存在
            missing_operations = [op for op in operations if op not in actual_operations]
            if missing_operations:
                logger.error(f"❌ 缺少预期操作: {missing_operations}")
                logger.info(f"实际存在的操作: {actual_operations}")
                return False

            # 5. 检查禁用状态是否符合预期
            invalid_disabled = []
            for op in disabled_operations:
                # 先检查操作是否存在
                if op not in operation_status:
                    logger.error(f"❌ 要检查的禁用操作 '{op}' 不存在")
                    return False

                # 检查是否处于禁用状态
                if not operation_status[op]:
                    invalid_disabled.append(op)

            if invalid_disabled:
                logger.error(f"❌ 以下操作未按预期禁用: {invalid_disabled}")
                return False

            logger.info(f"✅ 所有预期操作都存在: {operations}")
            if disabled_operations:
                logger.info(f"✅ 所有预期禁用操作状态正确: {disabled_operations}")

            return True
        except Exception as e:
            logger.error(f"❌ 操作检查过程中发生错误: {str(e)}")
            return False

    def delete_alert_error(self, expected_text):
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched

    def submit_alert_error(self, expected_text):
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched


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


import time

from playwright.sync_api import Page, expect
from tests.utils.page_utils import *
from tests.pages.fd.add_new_minsu import AddNewMinsuPage
from playwright.sync_api import Page, expect, Playwright, sync_playwright

class GAFilingManagementPage:
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

    def query_minsu_tr(self, minsu_name: str) -> bool:

        result = False
        if minsu_name is not None:
            result = query_target_name_tr(self.page, "民宿", minsu_name)
            # 检查结果是否为None，非None则返回True，否则返回False
        return result is not None

    def filing_operation(self,  operation: str, confirming_person_name: str=None, approval:bool=True) -> bool:
        """
        校验目标民宿的备案状态是否与预期一致
        （注：默认通过 get_table_cell_or_button(0,8) 获取单元格，需确保该函数返回第1行第9列的备案状态单元格）

        Args:
            operation: 民宿备案操作，确认详情等

        Returns:
            bool: 操作成功 True；获取失败 False
        """
        status_text = None  # 初始化状态文本变量，避免未定义报错
        try:
            # 1. 尝试获取备案状态对应的表格单元格（第1行第9列：索引0行、8列）
            operation_button = get_table_cell_or_button(self.page, 0, 8, operation)

            # 2. 校验单元格是否获取成功
            if operation_button is None:
                return False

            operation_button.click()
            time.sleep(2)
            # 4. 如果是备案房间操作，检查并填写民宿名称
            confirming_person_name_input = get_label_corresponding_input(self.page, "确认人姓名")
            confirming_person_name_input.fill(confirming_person_name)
            if approval:
                target_option = "通过"
            else:
                target_option = "不通过"
            select_radio_button(self.page, "确认结果", target_option)
            submit_button = self.page.get_by_role("button", name="提 交")
            submit_button.click()

            return True

        except Exception as e:
            logger.error(f"民宿{operation}发生错误：{str(e)}")
            return False

    def filling_alert_error(self, expected_text):
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


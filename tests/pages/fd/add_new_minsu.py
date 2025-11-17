from playwright.sync_api import Page, expect, Playwright, sync_playwright
import os
from playwright.sync_api import Page, expect

from tests.utils.page_utils import *

class AddNewMinsuPage:
    def __init__(self, page: Page):
        self.page = page
        self.page.wait_for_timeout(2000)

        # 新增民宿表单元素
        self.minsu_name = get_label_corresponding_input(self.page, "民宿名称")
        self.administrative_area = get_label_corresponding_input(self.page, "行政区划")
        self.detailed_address = get_label_corresponding_input(self.page, "详细地址")
        self.save_button = self.page.get_by_role("button", name="保 存")
        self.back_button = self.page.get_by_role("button", name="返回")


        # 证件照上传元素
        self.id_card_front_upload = get_label_corresponding_element(
            self.page,
            "负责人证件照(正面)",
            'following-sibling::div//input[@type="file"]'
        )

        self.id_card_front_image = get_label_corresponding_element(
            self.page,
            "负责人证件照(正面)",
            'following-sibling::div//img'
        )

        self.id_card_front_image_delete_icon = get_label_corresponding_element(
            self.page,
            "负责人证件照(正面)",
            'following-sibling::div//i[@class="el-icon-delete"]'
        )

        self.id_card_back_upload = get_label_corresponding_element(
            self.page,
            "负责人证件照(反面)",
            'following-sibling::div//input[@type="file"]'
        )

        self.id_card_back_image = get_label_corresponding_element(
            self.page,
            "负责人证件照(反面)",
            'following-sibling::div//img'
        )

        self.id_card_back_image_delete_icon = get_label_corresponding_element(
            self.page,
            "负责人证件照(反面)",
            'following-sibling::div//i[@class="el-icon-delete"]'
        )

    def fill_minsu_basic_info(self, minsu_name: str, detail_address: str, province: str = None, city: str = None,
                              district: str = None, street: str=None):
        """
        填写民宿基本信息
        :param minsu_name: 民宿名称
        :param detail_address: 详细地址
        :param province: 省份名称，如"福建省"
        :param city: 城市名称，如"福州市"
        :param district: 区县名称，如"鼓楼区"
        :param street: 街道名称,如"鼓东街道"
        """
        try:
            # 填写民宿名称
            self.minsu_name.fill(minsu_name)
            self.administrative_area.click()
            self.select_location(province, city, district, street)
            self.detailed_address.fill(detail_address)

        except Exception as e:
            raise e

    def select_location(self, province: str, city: str, district: str, street: str):
        """
        依次定位并选择省、市、区、街道（同步版本）

        参数:
            page: Playwright的Page对象
            province: 省份名称
            city: 城市名称
            district: 区/县名称
            street: 街道名称
        """
        # 要处理的位置参数列表
        locations = [
            ("省份", province),
            ("城市", city),
            ("区/县", district),
            ("街道", street)
        ]

        for loc_type, loc_name in locations:
            if not loc_name:  # 跳过空值参数
                print(f"{loc_type}参数为空，跳过处理")
                continue

            print(f"开始处理{loc_type}: {loc_name}")
            time.sleep(1)  # 等待1秒

            # 获取所有列表项并等待加载完成
            items = self.page.locator('.rg-results .rg-item')
            all_items = items.all()

            # 遍历查找目标位置
            found = False
            for item in all_items:
                text = item.text_content()
                if text and text.strip() == loc_name:
                    print(f"找到{loc_type}元素: {loc_name}")
                    item.click()  # 找到后点击该元素
                    found = True
                    break

            if not found:
                print(f"未找到{loc_type}元素: {loc_name}")

    def upload_id_card_images(self, front_image_path: str, back_image_path: str):
        """
        上传负责人证件照
        :param front_image_path: 正面照片路径
        :param back_image_path: 反面照片路径
        """
        try:
            # 验证文件存在
            # if not os.path.exists(front_image_path):
            #     raise FileNotFoundError(f"正面照片文件不存在: {front_image_path}")
            # if not os.path.exists(back_image_path):
            #     raise FileNotFoundError(f"反面照片文件不存在: {back_image_path}")

            # 上传正面照片 - 先检查是否已有照片，有则删除
            if self.id_card_front_image.count()>0 and self.id_card_front_image.count()>0:
                self.page.wait_for_timeout(500)
                get_label_corresponding_element(
                    self.page,
                    "负责人证件照(正面)",
                    'following-sibling::div//span[@class="el-upload-list__item-actions"]'
                ).hover()

                self.id_card_front_image_delete_icon.click(force=True)
                self.page.wait_for_timeout(1000)  # 等待删除完成

            # 检查上传控件存在后再上传
            if self.id_card_front_upload and os.path.exists(front_image_path):
                self.id_card_front_upload.set_input_files(front_image_path)
                self.page.wait_for_timeout(2000)  # 等待上传完成


            # 上传反面照片 - 先检查是否已有照片，有则删除
            if self.id_card_back_image.count() > 0 and self.id_card_back_image.count() > 0:
                self.page.wait_for_timeout(500)
                get_label_corresponding_element(
                    self.page,
                    "负责人证件照(反面)",
                    'following-sibling::div//span[@class="el-upload-list__item-actions"]'
                ).hover()
                self.id_card_back_image_delete_icon.click()
                self.page.wait_for_timeout(1000)  # 等待删除完成

            # 检查上传控件存在后再上传
            if self.id_card_back_upload.count() > 0 and os.path.exists(back_image_path):
                self.id_card_back_upload.set_input_files(back_image_path)
                self.page.wait_for_timeout(2000)  # 等待上传完成

        except Exception as e:
            raise e

    def upload_front_id_card_image(self, front_image_path: str):
        """
        上传负责人证件照
        :param front_image_path: 正面照片路径
        """
        try:
            # 验证文件存在
            # if not os.path.exists(front_image_path):
            #     raise FileNotFoundError(f"正面照片文件不存在: {front_image_path}")
            # if not os.path.exists(back_image_path):
            #     raise FileNotFoundError(f"反面照片文件不存在: {back_image_path}")

            # 上传正面照片 - 先检查是否已有照片，有则删除
            if self.id_card_front_image.count() > 0 and self.id_card_front_image.count() > 0:
                self.page.wait_for_timeout(500)
                get_label_corresponding_element(
                    self.page,
                    "负责人证件照(正面)",
                    'following-sibling::div//span[@class="el-upload-list__item-actions"]'
                ).hover()

                self.id_card_front_image_delete_icon.click(force=True)
                self.page.wait_for_timeout(1000)  # 等待删除完成

            # 检查上传控件存在后再上传
            if self.id_card_front_upload and os.path.exists(front_image_path):
                self.id_card_front_upload.set_input_files(front_image_path)
                wait_for_loading_disappear(self.page)


        except Exception as e:
            raise e

    def upload_back_id_card_image(self, back_image_path: str):
        """
        上传负责人证件照
        :param back_image_path: 反面照片路径
        """
        try:
            # 验证文件存在
            # if not os.path.exists(front_image_path):
            #     raise FileNotFoundError(f"正面照片文件不存在: {front_image_path}")
            # if not os.path.exists(back_image_path):
            #     raise FileNotFoundError(f"反面照片文件不存在: {back_image_path}")


            # 上传反面照片 - 先检查是否已有照片，有则删除
            if self.id_card_back_image.count() > 0 and self.id_card_back_image.count() > 0:
                logger.info("照片存在，需要先删除")
                get_label_corresponding_element(
                    self.page,
                    "负责人证件照(反面)",
                    'following-sibling::div//span[@class="el-upload-list__item-actions"]'
                ).hover()
                self.id_card_back_image_delete_icon.click()
                self.page.wait_for_timeout(1000)  # 等待删除完成

            # 检查上传控件存在后再上传
            if self.id_card_back_upload.count() > 0 and os.path.exists(back_image_path):
                self.id_card_back_upload.set_input_files(back_image_path)
                wait_for_loading_disappear(self.page)

        except Exception as e:
            raise e

    def save_minsu_info(self):
        """保存民宿信息"""
        try:
            self.save_button.click()
            # 等待保存完成，可以根据实际情况调整等待逻辑
        except Exception as e:
            raise e

    def add_new_minsu(self, minsu_name: str, detail_address: str, province: str, city: str, district: str, street: str, front_image: str, back_image: str):
        """
        完整的新增民宿流程
        :param minsu_name: 民宿名称
        :param detail_address: 详细地址
        :param area_path: 行政区划路径
        :param front_image: 负责人证件照正面路径
        :param back_image: 负责人证件照反面路径
        """
        try:
            # 填写基本信息
            self.fill_minsu_basic_info(minsu_name, detail_address, province, city, district, street)

            # 上传证件照
            self.upload_id_card_images(front_image, back_image)

            # 保存信息
            self.save_minsu_info()

        except Exception as e:
            raise e

    def minsu_name_error(self, message: str) -> bool:
            return get_element_corresponding_error_tip(self.minsu_name,
                                                       '../following-sibling::div[contains(@class, "el-form-item__error")]',
                                                       message)
    def administrative_area_error(self, message: str) -> bool:
            return get_element_corresponding_error_tip(self.administrative_area,
                                                       '../../../following-sibling::div[contains(@class, "el-form-item__error")]',
                                                       message)
    def detail_address_error(self, message: str) -> bool:
            return get_element_corresponding_error_tip(self.detailed_address,
                                                       '../following-sibling::div[contains(@class, "el-form-item__error")]',
                                                       message)
    def front_image_error(self, message: str) -> bool:
        is_visible = self.page.get_by_text(message, exact=True).is_visible()

        if is_visible:
            logger.info(f" ✅ 成功验证提示词 [{message}] 正确 ")
        else:
            logger.info(f" ❌ 未找到预期提示词 [{message}]")

        return is_visible

    def back_image_error(self, message: str) -> bool:
        is_visible = self.page.get_by_text(message, exact=True).is_visible()

        if is_visible:
            logger.info(f" ✅ 成功验证提示词 [{message}] 正确 ")
        else:
            logger.info(f" ❌ 未找到预期提示词 [{message}]")

        return is_visible

    def add_success_alert_error(self, message: str) -> bool:
        is_matched, actual_text = check_alert_text(self.page, message)

        return is_matched

    def add_ID_card_failed_alert_error(self, message: str) -> bool:
        is_matched, actual_text = check_alert_text(self.page, message)
        return is_matched

    def add_ID_card_front_image_success_error(self) -> bool:

        id_card_front_image = get_label_corresponding_element(
            self.page,
            "负责人证件照(正面)",
            'following-sibling::div//img'
        )
        if id_card_front_image.count()>0:
            logger.info("负责人证件照(正面)上传成功")
        else:
            logger.info("负责人证件照(正面)上传失败")
        return id_card_front_image.count() > 0

    def add_ID_card_back_image_success_error(self) -> bool:
        id_card_back_image = get_label_corresponding_element(
            self.page,
            "负责人证件照(反面)",
            'following-sibling::div//img'
        )
        if id_card_back_image.count()>0:
            logger.info("负责人证件照(反面)上传成功")
        else:
            logger.info("负责人证件照(反面)上传失败")
        return id_card_back_image.count() > 0

    def add_ID_card_images_success_error(self) -> bool:
        id_card_front_image = get_label_corresponding_element(
            self.page,
            "负责人证件照(正面)",
            'following-sibling::div//img'
        )

        id_card_back_image = get_label_corresponding_element(
            self.page,
            "负责人证件照(反面)",
            'following-sibling::div//img'
        )
        return id_card_front_image.count() > 0 and id_card_back_image.count() > 0

    def add_new_minsu_success_alert(self, expected_text):
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched
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
#     page.get_by_role("link", name="民宿管理").click()
#     page.get_by_role("button", name=" 新增民宿").click()
#     add_new_minsu_page = AddNewMinsuPage(page)
#     add_new_minsu_page.upload_front_id_card_image("F:/code/wyf_fd/tests/data/evidence_files/lease.exe")
#     assert add_new_minsu_page.add_ID_card_failed_alert_error("文件格式不正确, 请上传jpg/jpeg/png图片格式文件!")
#     # target_minsu = query_target_name(page, "民宿", "这是一个刚好三十个字符的民宿名称用于测试长度限制")
#     # if target_minsu is not None:
#     #     target_operation(page, "民宿", "这是一个刚好三十个字符的民宿名称用于测试长度限制", "10", "删除")
#     # fields = {     "front_image":"../data/evidence_files/lease.exe",
#     #                "back_image":"../data/evidence_files/lease.png",
#     #         }
#     #
#     # page.get_by_role("button", name=" 新增民宿").click()
#     #
#     # add_new_minsu_page = AddNewMinsuPage(page)
#     # add_new_minsu_page.upload_front_id_card_image(fields["front_image"])
#     # assert  add_new_minsu_page.add_ID_card_failed_alert_error("文件格式不正确, 请上传jpg/jpeg/png图片格式文件!")
#
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)
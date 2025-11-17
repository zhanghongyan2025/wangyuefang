
from tests.utils.file_utils import get_image_files
from tests.utils.page_utils import *
from tests.utils.validator import *
from playwright.sync_api import Page, sync_playwright
from tests.utils.form_validation_utils import FormValidationUtils

import re
import os
import time
import logging


class FilingRoomPage:
    """
    房间管理页面自动化测试类，用于处理与房间管理相关的UI操作和验证
    """

    def __init__(self, page: Page):
        """
        初始化RoomManagePage类

        Args:
            page (Page): Playwright的Page对象，用于操作浏览器页面
        """
        self.page = page
        self.room_name = get_label_corresponding_input(self.page, "房间名称")
        self.ms_name = get_label_corresponding_input(self.page, "民宿名称")
        self.ly_name = get_label_corresponding_input(self.page, "楼宇")
        self.floor = get_label_corresponding_input(self.page, "楼层")
        self.room_type = get_label_corresponding_input(self.page, "房间类型")

        elements_input = get_label_corresponding_elements(
            self.page, "房间户型", "following-sibling::div//input"
        )

        if len(elements_input) >= 4:
            (
                self.bedroom_number,
                self.living_room_number,
                self.kitchen_number,
                self.bathroom_number,
            ) = elements_input[:4]
        else:
            # 或者抛出异常
            raise ValueError("获取的房间户型元素数量不足")

        self.area = get_label_corresponding_input(self.page, "房型面积(㎡)")
        self.bed_number = get_label_corresponding_input(self.page, "床数量")
        self.max_occupancy = get_label_corresponding_input(self.page, "最大住人数")

    def upload_files_to_inputs(
        self, bedroom_files, livingroom_files, kitchen_files, bathroom_files
    ):
        """
        上传文件到不同房间类型的输入框

        Args:
            bedroom_files (str): 卧室文件目录
            livingroom_files (str): 客厅文件目录
            kitchen_files (str): 厨房文件目录
            bathroom_files (str): 浴室文件目录

        Returns:
            dict: 上传结果，包含每个房间类型的预期和实际上传数量
        """
        label_types = {
            "bedroom": {"directory": bedroom_files, "uploaded": 0, "expected": 0},
            "livingroom": {"directory": livingroom_files, "uploaded": 0, "expected": 0},
            "kitchen": {"directory": kitchen_files, "uploaded": 0, "expected": 0},
            "bathroom": {"directory": bathroom_files, "uploaded": 0, "expected": 0},
        }

        for label_type in label_types:
            directory = label_types[label_type]["directory"]
            files = get_image_files(directory)
            labels = self.page.query_selector_all(f'label[for^="{label_type}-"]')
            expected = calculate_expected_inputs(labels)
            label_types[label_type]["expected"] = expected

            for index, label in enumerate(labels):
                if index >= len(files):
                    break
                file_input = find_file_input(label)
                if file_input is None:
                    logger.warning(f"未找到 {label_type} 第 {index + 1} 个标签对应的文件输入框")
                    continue
                file_path = os.path.join(directory, files[index])
                try:
                    file_input.set_input_files(file_path)
                    time.sleep(1)
                    label_types[label_type]["uploaded"] += 1
                    logger.info(f"成功为 {label_type} 上传文件: {file_path}")
                except Exception as e:
                    logger.error(f"上传 {file_path} 失败: {str(e)}")

        upload_results = validate_upload_results(label_types)
        return upload_results

    def validate_file_inputs(self, bedroom_number, livingroom_number, kitchen_number, bathroom_number):
        """
        验证不同房间类型的文件输入框数量是否符合预期

        Args:
            bedroom_number (str): 预期的卧室文件输入框数量
            livingroom_number (str): 预期的客厅文件输入框数量
            kitchen_number (str): 预期的厨房文件输入框数量
            bathroom_number (str): 预期的浴室文件输入框数量

        Returns:
            dict: 验证结果，包含每个房间类型的预期和实际输入框数量
        """
        label_types = {
            "bedroom": {"param": bedroom_number, "count": 0},
            "livingroom": {"param": livingroom_number, "count": 0},
            "kitchen": {"param": kitchen_number, "count": 0},
            "bathroom": {"param": bathroom_number, "count": 0}
        }

        for label_type in label_types:
            labels = self.page.query_selector_all(f'label[for^="{label_type}-"]')
            for label in labels:
                file_input = find_file_input(label)
                if file_input is not None:
                    label_types[label_type]["count"] += 1

        validation_results = validate_count_results(label_types)
        return validation_results

    def is_radio_selected(page: Page, label_text: str, target_option: str) -> bool:
        """
        在指定标签下遍历单选按钮，根据文本内容匹配目标选项并返回选中状态

        :param page: Playwright 页面对象
        :param label_text: 父级标签文本（如"便器"）
        :param target_option: 目标选项文本（如"智能马桶"）
        :return: 目标选项的选中状态
        :raises ValueError: 未找到匹配的选项
        """
        try:
            # 获取所有相关的单选按钮元素
            radio_labels = get_label_corresponding_elements(page, label_text, 'following-sibling::div//label')

            # 检查是否存在匹配的选项
            matched_btn = None
            for btn in radio_labels:
                btn_text = btn.text_content().strip()
                if target_option in btn_text:
                    matched_btn = btn
                    break

            if not matched_btn:
                available_options = [btn.text_content().strip() for btn in radio_labels]
                raise ValueError(f"未找到选项：{target_option}，可用选项为：{available_options}")

            # 获取实际的 input 元素
            input_element = matched_btn.locator('input[type="radio"]')
            if not input_element.count():
                raise RuntimeError(f"无法在标签元素中找到对应的单选按钮输入框: {target_option}")

            # 返回选中状态并记录日志
            is_checked = input_element.is_checked()
            if is_checked:
                logger.info(f" ✅  [{target_option}]已选中")
            else:
                logger.info(f" ❌  [{target_option}]未被选中")
            return is_checked

        except Exception as e:
            logger.error(f"检查/选择单选按钮 {target_option} 时出错: {str(e)}")
            raise

    def filing_room(
        self,
        room_name: str,
        property_type: str,
        ms_name: str,
        ly_name: str,
        floor: str,
        room_type: str,
        bedroom_number: str,
        living_room_number: str,
        kitchen_number: str,
        bathroom_number: str,
        area: str,
        bed_number: str,
        max_occupancy: str,
        property_certificate: str,

        bedroom_files: str,
        living_room_files: str,
        kitchen_files: str,
        bathroom_files: str,
        parking: str,
        balcony: str,
        window: str,
        tv: str,
        projector: str,
        washing_machine: str,
        clothes_steamer: str,
        water_heater: str,
        hair_dryer: str,
        fridge: str,
        stove: str,
        toilet: str,
        fire_safety_certificate: str = None,
        public_security_registration_form: str = None,
        test_fields: str = None,
    ):
        """
        注册新房间的完整流程

        Args:
            room_name (str): 房间名称
            property_type (str): 房产类型（租赁/自有/共有）
            ms_name (str): 民宿名称
            ly_name (str): 楼宇名称
            floor (str): 楼层名称
            room_type (str): 房间类型
            bedroom_number (str): 卧室数量
            living_room_number (str): 客厅数量
            kitchen_number (str): 厨房数量
            bathroom_number (str): 浴室数量
            area (str): 房型面积
            bed_number (str): 床数量
            max_occupancy (str): 最大住人数
            property_certificate (str): 证明文件路径
            fire_safety_certificate (str): 消防证明文件路径
            bedroom_files (str): 卧室图片文件目录
            living_room_files (str): 客厅图片文件目录
            kitchen_files (str): 厨房图片文件目录
            bathroom_files (str): 浴室图片文件目录
            parking (str): 车位选项
            balcony (str): 阳台选项
            window (str): 窗户选项
            tv (str): 电视机选项
            projector (str): 投影仪选项
            washing_machine (str): 洗衣机选项
            clothes_steamer (str): 挂烫机选项
            water_heater (str): 热水器选项
            hair_dryer (str): 吹风机选项
            fridge (str): 冰箱选项
            stove (str): 炉灶选项
            toilet (str): 便器选项
            test_fields (str): 测试字段，用逗号分隔
        """
        # 调用 fill_room_info 并保持参数一致性
        self.fill_room_info(
            room_name=room_name,
            ms_name=ms_name,
            ly_name=ly_name,
            floor=floor,
            room_type=room_type,
            bedroom_number=bedroom_number,
            living_room_number=living_room_number,
            kitchen_number=kitchen_number,
            bathroom_number=bathroom_number,
            area=area,
            bed_number=bed_number,
            max_occupancy=max_occupancy,
            property_type=property_type,
            parking=parking,
            balcony=balcony,
            window=window,
            tv=tv,
            projector=projector,
            washing_machine=washing_machine,
            clothes_steamer=clothes_steamer,
            water_heater=water_heater,
            hair_dryer=hair_dryer,
            fridge=fridge,
            stove=stove,
            toilet=toilet,
            test_fields=test_fields,
        )

        self.upload_property_certificate(property_type, property_certificate, test_fields=test_fields)
        self.upload_fire_safety_certificate(fire_safety_certificate, test_fields=test_fields)
        self.upload_public_security_registration_form(public_security_registration_form, test_fields=test_fields)

        self.validate_file_inputs(bedroom_number, living_room_number, kitchen_number, bathroom_number)
        self.upload_files_to_inputs(bedroom_files, living_room_files, kitchen_files, bathroom_files)

    def check_register_result(self):
        # 验证结果
        is_matched, actual_text = check_alert_text(self.page, "新增成功")

        if is_matched:
            logger.info("验证结果：成功，房间新增成功")
            return is_matched
        else:
            logger.info("验证结果：失败")
            logger.error(f"房间新增失败,原因是 {actual_text}")
            return False
            raise AssertionError(f"房间新增失败")

    def fill_room_info(
        self,
        room_name: str,
        ms_name: str,
        ly_name: str,
        floor: str,
        room_type: str,
        bedroom_number: str,
        living_room_number: str,
        kitchen_number: str,
        bathroom_number: str,
        area: str,
        bed_number: str,
        max_occupancy: str,
        parking: str,
        balcony: str,
        window: str,
        tv: str,
        projector: str,
        washing_machine: str,
        clothes_steamer: str,
        water_heater: str,
        hair_dryer: str,
        fridge: str,
        stove: str,
        toilet: str,
        property_type: str = "自有",
        test_fields: str = None,
    ):
        """
        填写房间基本信息表单（增强版）

        Args:
            room_name (str): 房间名称
            ms_name (str): 民宿名称
            ly_name (str): 楼宇名称
            floor (str): 楼层名称
            room_type (str): 房间类型
            bedroom_number (str): 卧室数量
            living_room_number (str): 客厅数量
            kitchen_number (str): 厨房数量
            bathroom_number (str): 浴室数量
            area (str): 房型面积
            bed_number (str): 床数量
            max_occupancy (str): 最大住人数
            parking (str): 车位选项
            balcony (str): 阳台选项
            window (str): 窗户选项
            tv (str): 电视机选项
            projector (str): 投影仪选项
            washing_machine (str): 洗衣机选项
            clothes_steamer (str): 挂烫机选项
            water_heater (str): 热水器选项
            hair_dryer (str): 吹风机选项
            fridge (str): 冰箱选项
            stove (str): 炉灶选项
            toilet (str): 便器选项
            property_type (str, optional): 房产类型，默认为"自有"
            test_fields (str): 测试字段，用逗号分隔

        Returns:
            bool: 如果所有字段都成功填写，返回True；如果test_fields中存在某个字段且值为空，返回False
        """
        # 字段配置字典
        field_config = {
            # 基本信息字段
            "room_name": (lambda: self.room_name, lambda v: self.room_name.fill(v)),
            "property_type": (None, lambda v: select_radio(self.page, "产权类型", v)),
            "ms_name": (None, lambda v: select_option_by_input_element(self.page, self.ms_name, v)),
            "ly_name": (None, lambda v: select_option_by_input_element(self.page, self.ly_name, v)),
            "floor": (None, lambda v: select_option_by_input_element(self.page, self.floor, v)),
            "room_type": (None, lambda v: select_option_by_input_element(self.page, self.room_type, v)),
            "bedroom_number": (
                lambda: self.bedroom_number,
                lambda v: (self.bedroom_number.fill(v), simulate_blur(self.bedroom_number))[0],
            ),
            "living_room_number": (
                lambda: self.living_room_number,
                lambda v: (self.living_room_number.fill(v), simulate_blur(self.living_room_number))[0],
            ),
            "kitchen_number": (
                lambda: self.kitchen_number,
                lambda v: (self.kitchen_number.fill(v), simulate_blur(self.kitchen_number))[0],
            ),
            "bathroom_number": (
                lambda: self.bathroom_number,
                lambda v: (self.bathroom_number.fill(v), simulate_blur(self.bathroom_number))[0],
            ),
            "area": (
                lambda: self.area,
                lambda v: set_selector_input_by_input_element(
                    self.area,
                    "../../*[contains(@class, 'increase')]",
                    v,
                ),
            ),
            "bed_number": (
                lambda: self.bed_number,
                lambda v: set_selector_input_by_input_element(
                    self.bed_number,
                    "../../*[contains(@class, 'increase')]",
                    v,
                ),
            ),
            "max_occupancy": (
                lambda: self.max_occupancy,
                lambda v: set_selector_input_by_input_element(
                    self.max_occupancy,
                    "../../*[contains(@class, 'increase')]",
                    v,
                ),
            ),
            # 设施字段
            "parking": (None, lambda v: select_radio(self.page, "是否有车位", v)),
            "balcony": (None, lambda v: select_radio(self.page, "是否有阳台", v)),
            "window": (None, lambda v: select_radio(self.page, "是否有窗户", v)),
            "tv": (None, lambda v: select_radio(self.page, "电视机", v)),
            "projector": (None, lambda v: select_radio(self.page, "投影仪", v)),
            "washing_machine": (None, lambda v: select_radio(self.page, "洗衣机", v)),
            "clothes_steamer": (None, lambda v: select_radio(self.page, "挂烫机", v)),
            "water_heater": (None, lambda v: select_radio(self.page, "热水器", v)),
            "hair_dryer": (None, lambda v: select_radio(self.page, "吹风机", v)),
            "fridge": (None, lambda v: select_radio(self.page, "冰箱", v)),
            "stove": (None, lambda v: select_radio(self.page, "炉灶", v)),
            "toilet": (None, lambda v: select_radio(self.page, "便器", v)),
        }

        # 获取所有字段的默认值
        all_fields = locals()
        # 移除self和test_fields，因为它们不是表单字段
        all_fields.pop("self")
        all_fields.pop("test_fields")

        # 处理每个字段
        if all_fields is not None:
            for field_name, value in list(all_fields.items()):
                # 检查字段是否在配置中
                if field_name in field_config:
                    element_getter, setter = field_config[field_name]

                    # 独立判断每个字段是否需要处理
                    if test_fields is not None :
                        if value or field_name in test_fields:
                            # 如果字段在测试集合中，验证值是否为空
                            if field_name in test_fields:
                                if value is None or value == "":
                                    return False

                        # 执行设置操作.
                        setter(value)

        return True

    def upload_property_certificate(self, property_type, property_certificate, test_fields=None):
        """
        上传房产证明文件

        Args:
            property_type (str): 房产类型
            property_certificate (str): 房产证明文件路径
            test_fields (str): 测试字段，用逗号分隔
        """
        # 确定房产证明类型
        if property_type == "租赁":
            proof_type = "租赁证明"
        elif property_type == "自有":
            proof_type = "产权证明"
        elif property_type == "共有":
            proof_type = "共有产权证明"
        else:
            raise ValueError(f"不支持的property_type: {property_type}")

        # 处理房产证明文件
        file_exists = os.path.exists(property_certificate)

        if not file_exists:
            log_msg = f"房产证明文件不存在: {property_certificate}"
            if test_fields is not None and "property_certificate" in test_fields:
                logger.warning(log_msg)
                # 允许上传空文件的逻辑
                if "property_certificate" in test_fields:
                    logger.info(f"测试模式：允许上传空文件 - {proof_type}")
                    scroll_to_keywords_view(self.page, proof_type)
                    file_input = get_label_corresponding_element(
                        self.page,
                        proof_type,
                        'following-sibling::div//input[@type="file"]',
                    )
                    file_input.set_input_files([])  # 上传空文件
                    logger.info(f"已上传空的{proof_type}")
                    return
            else:
                logger.error(log_msg)
                raise FileNotFoundError(log_msg)

        # 文件存在的正常处理流程
        scroll_to_keywords_view(self.page, proof_type)
        file_input = get_label_corresponding_element(
            self.page,
            proof_type,
            'following-sibling::div//input[@type="file"]',
        )
        file_input.set_input_files(property_certificate)
        time.sleep(2)
        logger.info(f"已上传{proof_type}: {property_certificate}")

    def upload_fire_safety_certificate(self, fire_safety_certificate, test_fields=None):
        """
        上传消防合格证明文件

        Args:
            fire_safety_certificate (str): 消防合格证明文件路径
            test_fields (str): 测试字段，用逗号分隔
        """
        test_fields = test_fields.split(",") if test_fields else []

        # 处理消防合格证明文件
        if fire_safety_certificate:  # 修改点：检查文件路径是否存在（非空字符串和非None）
            if not os.path.exists(fire_safety_certificate):
                log_msg = f"消防合格证明文件不存在: {fire_safety_certificate}"

                if "fire_safety_certificate" in test_fields:
                    logger.warning(log_msg)
                else:
                    logger.error(log_msg)
                    raise FileNotFoundError(log_msg)
            else:
                scroll_to_keywords_view(self.page, "消防合格证明")
                fire_input = get_label_corresponding_element(
                    self.page,
                    "消防合格证明",
                    'following-sibling::div//input[@type="file"]',
                )
                fire_input.set_input_files(fire_safety_certificate)
                time.sleep(2)
                logger.info(f"已上传消防合格证明: {fire_safety_certificate}")
        else:
            logger.info("未提供消防合格证明文件路径或路径为空，跳过上传")  # 修改提示信息

    def upload_public_security_registration_form(self, public_security_registration_form, test_fields=None):
        """
        网约房治安管理登记表

        Args:
            public_security_registration_form (str): 消防合格证明文件路径
            test_fields (str): 测试字段，用逗号分隔
        """
        test_fields = test_fields.split(",") if test_fields else []

        # 处理消防合格证明文件
        if public_security_registration_form:  # 修改点：检查文件路径是否存在（非空字符串和非None）
            if not os.path.exists(public_security_registration_form):
                log_msg = f" 网约房治安管理登记表不存在: {public_security_registration_form}"

                if "public_security_registration_form" in test_fields:
                    logger.warning(log_msg)
                else:
                    logger.error(log_msg)
                    raise FileNotFoundError(log_msg)
            else:
                scroll_to_keywords_view(self.page, "网约房治安管理登记表")
                fire_input = get_label_corresponding_element(
                    self.page,
                    "网约房治安管理登记表",
                    'following-sibling::div//input[@type="file"]',
                )
                fire_input.set_input_files(public_security_registration_form)
                logger.info(f"已上网约房治安管理登记表: {public_security_registration_form}")
        else:
            logger.info("未提网约房治安管理登记表路径或路径为空，跳过上传")  # 修改提示信息

    def is_file_uploaded(self, label_text: str) -> bool:
        try:
            element = get_label_corresponding_element(
                self.page,
                label_text,
                'following-sibling::div//a[contains(@href, "onlinehotel/profile/upload/")]',
            )
            if element is None:
                logger.info("未找到上传文件的链接元素")
                return False
            logger.info("上传file成功")
            return True
        except Exception:  # 建议替换为具体的元素未找到异常类型
            return False

    def is_property_certificate_uploaded(self, label_text: str):
        return self.is_file_uploaded(label_text)

    def is_fire_safety_certificate_uploaded(self, label_text: str):
        return self.is_file_uploaded(label_text)

    def is_public_security_registration_form_uploaded(self, label_text: str):
        return self.is_file_uploaded(label_text)

    def delete_uploaded_file(self, label_text: str):
        logger.info("start delete")
        delete_button = get_label_corresponding_element(
            self.page, label_text, 'following-sibling::div//a[span[text()="删除"]]'
        )
        delete_button.click()
        logger.info("end delete")

    def submit_form(self):
        """提交房间新增表单"""
        scroll_to_bottom(self.page)
        time.sleep(1)
        self.page.get_by_role("button", name="确 定").click()
        time.sleep(0.5)

    def get_property_type(self):
        # 获取所有产权类型标签元素
        label_elements = get_label_corresponding_elements(self.page, "产权类型", 'following-sibling::div//label')

        # 查找被选中的元素
        for element in label_elements:
            if "is-checked" in element.get_attribute("class"):
                selected_label = element.locator(".el-radio__label").text_content()
                logger.info(f"选中的标签是: {selected_label}")
                return selected_label

    def room_name_error(self, message: str) -> bool:
        """检查房间名称输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.room_name, '../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def property_type_check(self, property_type):
        """
        根据产权类型检查页面上是否存在对应的文本

        Args:
            property_type (str): 产权类型，可选值为"自有", "租赁", "共有"

        Returns:
            bool: 如果存在对应文本返回True，否则返回False
        """
        text_mapping = {
            "自有": "产权证明",
            "租赁": "租赁证明",
            "共有": "共有产权证明",
        }

        if property_type not in text_mapping:
            raise ValueError(f"不支持的产权类型: {property_type}")

        expected_text = text_mapping[property_type]

        is_visible = self.page.get_by_text(expected_text, exact=True).is_visible()

        if is_visible:
            logger.info(f" ✅ 成功验证房产类型 [{property_type}] 对应提示词 [{expected_text}] 正确 ")
        else:
            logger.info(f" ❌ 未找到房产类型 [{property_type}] 的预期提示词 [{expected_text}]")

        return is_visible

    def ms_name_error(self, message: str) -> bool:
        """检查民宿名称输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.ms_name, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def ly_name_error(self, message: str) -> bool:
        """检查楼宇名称输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.ly_name, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def floor_error(self, message: str) -> bool:
        """检查楼层输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.floor, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def room_type_error(self, message: str) -> bool:
        """检查房间类型输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.room_type, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def bedroom_number_error(self, message: str) -> bool:
        """检查卧室数量输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.bedroom_number, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def living_room_number_error(self, message: str) -> bool:
        """检查客厅数量输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.living_room_number, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def kitchen_number_error(self, message: str) -> bool:
        """检查厨房数量输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.kitchen_number, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def bathroom_number_error(self, message: str) -> bool:
        """检查浴室数量输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.bathroom_number, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def area_error(self, message: str) -> bool:
        """检查房型面积输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.area, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def bed_number_error(self, message: str) -> bool:
        """检查床数量输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.bed_number, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def max_occupancy_error(self, message: str) -> bool:
        """检查最大住人数输入框是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.max_occupancy, '../../following-sibling::div[contains(@class, "el-form-item__error")]', message
        )

    def parking_error(self, message: str) -> bool:
        """检查车位选项是否显示指定的错误提示"""
        # 假设车位选项为单选框，错误提示位置与普通输入框一致
        return get_element_corresponding_error_tip(
            self.page.get_by_text("是否有车位", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def balcony_error(self, message: str) -> bool:
        """检查阳台选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("是否有阳台", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def window_error(self, message: str) -> bool:
        """检查窗户选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("是否有窗户", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def tv_error(self, message: str) -> bool:
        """检查电视机选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("电视机", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def projector_error(self, message: str) -> bool:
        """检查投影仪选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("投影仪", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def washing_machine_error(self, message: str) -> bool:
        """检查洗衣机选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("洗衣机", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def clothes_steamer_error(self, message: str) -> bool:
        """检查挂烫机选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("挂烫机", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def water_heater_error(self, message: str) -> bool:
        """检查热水器选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("热水器", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def hair_dryer_error(self, message: str) -> bool:
        """检查吹风机选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("吹风机", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def fridge_error(self, message: str) -> bool:
        """检查冰箱选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("冰箱", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def stove_error(self, message: str) -> bool:
        """检查炉灶选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("炉灶", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def toilet_error(self, message: str) -> bool:
        """检查便器选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            self.page.get_by_text("便器", exact=True), '../..//div[contains(@class, "el-form-item__error")]', message
        )

    def property_type_error(self, message: str) -> bool:
        """检查房产类型选项是否显示指定的错误提示"""
        return get_element_corresponding_error_tip(
            get_label_corresponding_element(self.page, "产权类型", '../following-sibling::div[contains(@class, "el-form-item__error")]'),
            message,
        )

    def property_certificate_empty_error(self, expected_text) -> bool:
        """检查房产类型选项是否显示指定的错误提示"""
        supported_types = {"自有", "租赁", "共有"}

        property_type = self.get_property_type()

        if property_type not in supported_types:
            raise ValueError(f"不支持的产权类型: {property_type}")

        time.sleep(1)
        is_visible = self.page.get_by_text(expected_text, exact=True).is_visible()

        if is_visible:
            logger.info(f" ✅ 成功验证提示词 [{expected_text}] 正确 ")
        else:
            logger.info(f" ❌ 未找到预期提示词 [{expected_text}]")

        return is_visible

    def property_certificate_error(self, expected_text) -> bool:
        """检查房产类型选项是否显示指定的错误提示"""
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        return is_matched

    def fire_safety_certificate_error(self, expected_text) -> bool:
        """检查消防证明文件是否显示指定的错误提示"""
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        if is_matched:
            logger.info(f"✅ 成功验证提示词 [{expected_text}] 正确 ")
        else:
            logger.info(f"❌ 未找到预期提示词 [{expected_text}]")
        return is_matched

    def public_security_registration_form_error(self, expected_text) -> bool:
        """检查治安登记表是否显示指定的错误提示"""
        is_matched, actual_text = check_alert_text(self.page, expected_text)
        if is_matched:
            logger.info(f"✅ 成功验证提示词 [{expected_text}] 正确 ")
        else:
            logger.info(f"❌ 未找到预期提示词 [{expected_text}]")
        return is_matched

    # def _create_room_data(self, index: int) -> dict:
    #     """创建房间数据字典"""
    #     return {
    #         "room_name": f"测试房间_{index}",
    #         "ms_name": f"测试民宿_{index}",
    #         "floor": "三层",
    #         "ly_name": "测试楼宇",
    #         "room_type": "大床房",
    #         "bedroom_number": "1",
    #         "living_room_number": "1",
    #         "kitchen_number": "1",
    #         "bathroom_number": "1",
    #         "area": "15",
    #         "bed_number": "2",
    #         "max_occupancy": "2",
    #         "parking": "有",
    #         "balcony": "有",
    #         "window": "有",
    #         "tv": "有",
    #         "projector": "无",
    #         "washing_machine": "有",
    #         "clothes_steamer": "无",
    #         "water_heater": "有",
    #         "hair_dryer": "有",
    #         "fridge": "有",
    #         "stove": "燃气灶",
    #         "toilet": "智能马桶",
    #         "property_type": "自有"
    #     }

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("http://192.168.40.61:3333/login_fd?redirect=%2Ffangwu_fangdong%2Fminsu")
#     page.get_by_role("textbox", name="账号").fill("fenghuang_456")
#     page.get_by_role("textbox", name="密码").fill("Aa123123!")
#     page.get_by_role("button", name="登 录").click()
#     page.get_by_role("menuitem", name="房屋管理").click()
#     page.get_by_role("link", name="房间管理").click()
#     for index in range(6, 50):
#         page.get_by_role("button", name="备案房间").click()
#         room_register_page = RoomRegisterPage(page)
#         # 创建民宿数据
#         room_data = room_register_page._create_room_data(index)
#         room_register_page.register_room(
#             property_certificate="6.png",
#             fire_safety_certificate="6.png",
#             bedroom_files="screenshots",
#             living_room_files="screenshots",
#             kitchen_files="screenshots",
#             bathroom_files="screenshots",
#             test_fields="all",
#             **room_data)
#         room_register_page.submit_form()
#
# with sync_playwright() as playwright:
#     run(playwright)
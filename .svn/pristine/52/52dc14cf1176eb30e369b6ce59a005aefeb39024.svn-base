# 标准库
import json
import re
import time

# 第三方库
import pytest
from datetime import datetime

from conf.config import *
# 本地模块
from conf.logging_config import logger
from tests.pages.fd.ft_manage_page import FTManagePage
from tests.pages.fd.home_page import HomePage
from tests.pages.fd.login_page import LoginPage
from tests.pages.fd.room_management_page import RoomManagementPage
from tests.pages.fd.filing_room_page import FilingRoomPage
from tests.utils.form_validation_utils import FormValidationUtils
from tests.utils.page_utils import *

# ------------------------------
# 工具函数：减少重复逻辑
# ------------------------------
def check_error_message(filing_room_page, field, expected_tip):
    """
    通用错误提示验证函数，用于验证页面上显示的错误提示信息是否符合预期。

    参数:
    filing_room_page: 房间注册页面对象。
    field: 需要验证的字段名称。
    expected_tip: 预期的错误提示信息。
    """
    error_method_name = FormValidationUtils.get_error_selector("room", field)
    error_check_method = getattr(filing_room_page, error_method_name)
    assert error_check_method(expected_tip)

# ------------------------------
# 测试类：合并重复方法，减少冗余
# ------------------------------
@pytest.mark.room
class TestFilingRoom:
    # """
    # 房间信息注册测试类，用于对房间注册页面的各项功能进行测试，包括基础字段验证、文件上传验证等。
    # """
    # #
    # # 场景1：基础字段非空验证
    base_field_empty_cases = [
        # 基本信息
        ("room_name", "", "房间名称不能为空"),
        ("ms_name", "", "请选择民宿"),
        ("floor", "", "请选择楼层"),
        ("ly_name", "", "请选择楼宇"),
        ("room_type", "", "请选择房间类型"),

        # 数量信息
        ("bedroom_number", "", "请输入卧室数量"),
        ("living_room_number", "", "请输入客厅数量"),
        ("kitchen_number", "", "请输入厨房数量"),
        ("bathroom_number", "", "请输入卫生间数量"),
        ("area", "", "房型面积(㎡)不能为空"),
        ("bed_number", "", "床数量不能为空"),
        ("max_occupancy", "", "最大住人数不能为空"),

        # 设施选择
        ("parking", "", "请选择是否有车位"),
        ("balcony", "", "请选择是否有阳台"),
        ("window", "", "请选择是否有窗户"),
        ("tv", "", "请选择电视机"),
        ("projector", "", "请选择投影仪"),
        ("washing_machine", "", "请选择洗衣机"),
        ("clothes_steamer", "", "请选择挂烫机"),
        ("water_heater", "", "请选择热水器"),
        ("hair_dryer", "", "请选择吹风机"),
        ("fridge", "", "请选择冰箱"),
        ("stove", "", "请选择炉灶"),
        ("toilet", "", "请选择便器"),

        # 证件类型与上传关联验证
        ("property_type", "自有", "请上传产权证明"),
        ("property_type", "租赁", "请上传租赁证明"),
        ("property_type", "共有", "请上传共有产权证明"),
    ]
    base_field_empty_ids = [
        "room_name_empty", "ms_not_selected", "floor_not_selected", "ly_not_selected", "room_type_not_selected",
        "bedroom_number_empty", "living_room_number_empty", "kitchen_number_empty", "bathroom_number_empty",
        "area_empty", "bed_number_empty", "max_guests_empty",
        "parking_not_selected", "balcony_not_selected", "window_not_selected",
        "tv_not_selected", "projector_not_selected", "washing_machine_not_selected",
        "clothes_steamer_not_selected", "water_heater_not_selected", "hair_dryer_not_selected",
        "fridge_not_selected", "stove_not_selected", "toilet_not_selected",
        "property_certificate_not_uploaded_owned", "property_certificate_not_uploaded_leased",
        "property_certificate_not_uploaded_shared"
    ]

    @pytest.mark.parametrize("field, test_value, expected_tip", base_field_empty_cases, ids=base_field_empty_ids)
    def test_base_field_validation(self, filing_room_page_setup, field, test_value, expected_tip):
        """
        测试基础字段的非空及合法性验证。
        该测试用例主要目的是验证房间注册页面中各个基础字段在输入为空或不合法数据时，是否能正确显示预期的错误提示信息。
        """
        filing_room_page = filing_room_page_setup
        params = FormValidationUtils.get_form_params("room", field, test_value)

        # 处理产权类型特殊逻辑
        if field == "property_type":
            test_fields = "property_certificate"
        else:
            test_fields = field

        filing_room_page.fill_room_info(test_fields=test_fields, **params)
        filing_room_page.submit_form()
        time.sleep(1)

        # 验证错误提示
        if field == "property_type":
            assert filing_room_page.property_certificate_empty_error(expected_tip)
        else:
            check_error_message(filing_room_page, field, expected_tip)

    # 场景2：文件上传验证用例
    file_upload_cases = [
        # 产权证明文件验证
        ("property_certificate", "", "", "empty_property_certificate"),
        ("property_certificate", LARGE_PROPERTY_CERTIFICATE, "上传文件大小不能超过 10 MB!",
         "large_property_certificate"),
        ("property_certificate", HTML_PROPERTY_CERTIFICATE, "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!",
         "html_property_certificate"),
        ("property_certificate", PHP_PROPERTY_CERTIFICATE, "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!",
         "php_property_certificate"),
        ("property_certificate", PY_PROPERTY_CERTIFICATE, "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!",
         "py_property_certificate"),
        ("property_certificate", SVG_PROPERTY_CERTIFICATE, "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!",
         "svg_property_certificate"),
        ("property_certificate", TXT_PROPERTY_CERTIFICATE, "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!",
         "txt_property_certificate"),
        ("property_certificate", ZIP_PROPERTY_CERTIFICATE, "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!",
         "zip_property_certificate"),
        ("property_certificate", JPEG_PROPERTY_CERTIFICATE, "上传文件数量不能超过 1 个!",
         "multi_property_certificate"),

        # 消防安全证明文件验证
        ("fire_safety_certificate", LARGE_PROPERTY_CERTIFICATE, "上传文件大小不能超过 10 MB!",
         "large_fire_safety_certificate"),
        ("fire_safety_certificate", HTML_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "html_fire_safety_certificate"),
        ("fire_safety_certificate", PHP_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "php_fire_safety_certificate"),
        ("fire_safety_certificate", PY_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "py_fire_safety_certificate"),
        ("fire_safety_certificate", SVG_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "svg_fire_safety_certificate"),
        ("fire_safety_certificate", TXT_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "txt_fire_safety_certificate"),
        ("fire_safety_certificate", ZIP_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "zip_fire_safety_certificate"),
        ("fire_safety_certificate", JPEG_PROPERTY_CERTIFICATE, "上传文件数量不能超过 1 个!",
         "multi_fire_safety_certificate"),

        # 公安登记表文件验证
        ("public_security_registration_form", LARGE_PROPERTY_CERTIFICATE, "上传文件大小不能超过 10 MB!",
         "large_public_security_form"),
        ("public_security_registration_form", HTML_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "html_public_security_form"),
        ("public_security_registration_form", PHP_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "php_public_security_form"),
        ("public_security_registration_form", PY_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "py_public_security_form"),
        ("public_security_registration_form", SVG_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "svg_public_security_form"),
        ("public_security_registration_form", TXT_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "txt_public_security_form"),
        ("public_security_registration_form", ZIP_PROPERTY_CERTIFICATE,
         "文件格式不正确, 请上传pdf/jpg/jpeg/png格式文件!", "zip_public_security_form"),
        ("public_security_registration_form", JPEG_PROPERTY_CERTIFICATE, "上传文件数量不能超过 1 个!",
         "multi_public_security_form_certificate"),
    ]

    @pytest.mark.parametrize("field, test_value, expected_tip, case_id", file_upload_cases)
    def test_file_upload_validation(self, request, filing_room_page_setup, field, test_value, expected_tip, case_id):
        """
        测试各类文件上传的合法性验证。
        该测试用例主要验证不同类型文件（如产权证明、消防安全证明、公安登记表等）在上传时，
        系统是否能正确处理文件大小、格式、数量等限制，并显示相应的错误提示信息。
        1.产权证明为空
        2.产权证明上传文件大小不能超过 10 MB
        3.产权证明上传HTML文件
        4.产权证明上传PHP文件
        5.产权证明上传PYTHON文件
        6.产权证明上传SVG文件
        7.产权证明上传TXT文件
        8.产权证明上传ZIP文件
        9.产权证明多次上传文件
        10.消防安全证明为空
        11.消防安全证明上传文件大小不能超过 10 MB
        12.消防安全证明上传HTML文件
        13.消防安全证明上传PHP文件
        14.消防安全证明上传PYTHON文件
        15.消防安全证明上传SVG文件
        16.消防安全证明上传TXT文件
        17.消防安全证明上传ZIP文件
        18.消防安全证明多次上传文件
        19.公安登记表为空
        20.公安登记表上传文件大小不能超过 10 MB
        21.公安登记表上传HTML文件
        22.公安登记表上传PHP文件
        23.公安登记表上传PYTHON文件
        24.公安登记表上传SVG文件
        25.公安登记表上传TXT文件
        26.公安登记表上传ZIP文件
        27.公安登记表多次上传文件
        """
        time.sleep(3)
        filing_room_page = filing_room_page_setup
        params = FormValidationUtils.get_form_params("room", field, test_value)
        current_test_id = request.node.name
        logger.info(f"📌 当前测试场景：: {current_test_id}")

        # 处理空文件特殊逻辑（遍历所有产权类型）
        if test_value == '':
            property_type_mapping = {
                "自有": "请上传产权证明",
                "租赁": "请上传租赁证明",
                "共有": "请上传共有产权证明"
            }
            for property_type, hint in property_type_mapping.items():
                new_params = params.copy()
                new_params["property_type"] = property_type
                new_params.pop("property_certificate", None)
                filing_room_page.fill_room_info(test_fields=field, **new_params)
                filing_room_page.submit_form()
                assert filing_room_page.property_certificate_empty_error(hint)
            return

        # 通用文件上传逻辑（根据字段动态处理）
        if field == "property_certificate":
            if re.search(r'multi_.+?_certificate', current_test_id):
                filing_room_page.upload_property_certificate(
                    params.get("property_type"), test_value, test_fields=field
                )

            filing_room_page.upload_property_certificate(
                params.get("property_type"), test_value, test_fields=field
            )
            # filing_room_page.submit_form()
            assert filing_room_page.property_certificate_error(expected_tip)

        elif field == "fire_safety_certificate":
            if re.search(r'multi_.+?_certificate', current_test_id):
                filing_room_page.upload_fire_safety_certificate(test_value, test_fields=field)

            filing_room_page.upload_fire_safety_certificate(test_value, test_fields=field)
            check_error_message(filing_room_page, field, expected_tip)

        elif field == "public_security_registration_form":
            if re.search(r'multi_.+?_certificate', current_test_id):
                filing_room_page.upload_public_security_registration_form(test_value, test_fields=field)
            filing_room_page.upload_public_security_registration_form(test_value, test_fields=field)
            check_error_message(filing_room_page, field, expected_tip)

    # 场景3：房间数量格式验证用例
    number_format_cases = [
        ("living_room_number", "1,,,", "请输入客厅数量"),
        ("kitchen_number", "1,1,,", "请输入厨房数量"),
        ("bathroom_number", "1,1,1,", "请输入卫生间数量"),
    ]
    number_format_ids = ["only_bedroom_number", "only_bedroom_living_room_number", "missing_bedroom_number"]

    @pytest.mark.parametrize("field, test_value, expected_tip", number_format_cases, ids=number_format_ids)
    def test_number_format_validation(self, filing_room_page_setup, field, test_value, expected_tip):
        """
        测试房间（包括客厅，厨房，卫生间）数量格式的合法性验证。
        该测试用例主要验证房间数量输入框在输入不合法格式的数据时，是否能正确显示预期的错误提示信息。
        """
        filing_room_page = filing_room_page_setup
        params = FormValidationUtils.get_form_params("room", field, test_value)
        filing_room_page.fill_room_info(test_fields=field, **params)
        check_error_message(filing_room_page, field, expected_tip)

    # 场景4：单选按钮标签文本与值映射
    radio_mapping = {
        "parking": "是否有车位",
        "balcony": "是否有阳台",
        "window": "是否有窗户",
        "tv": "电视机",
        "washing_machine": "洗衣机",
        "water_heater": "热水器",
        "fridge": "冰箱",
        "toilet": "便器",
        "projector": "投影仪",
        "clothes_steamer": "挂烫机",
        "hair_dryer": "吹风机",
        "stove": "炉灶"
    }

    # 单选按钮所有选项组合
    radio_all_options = [
        ("parking", "有"),
        ("parking", "无"),
        ("balcony", "有"),
        ("balcony", "无"),
        ("window", "有"),
        ("window", "无"),
        ("tv", "有"),
        ("tv", "无"),
        ("washing_machine", "有"),
        ("washing_machine", "无"),
        ("water_heater", "有"),
        ("water_heater", "无"),
        ("fridge", "有"),
        ("fridge", "无"),
        ("projector", "有"),
        ("projector", "无"),
        ("clothes_steamer", "有"),
        ("clothes_steamer", "无"),
        ("hair_dryer", "有"),
        ("hair_dryer", "无"),
        ("toilet", "智能马桶"),
        ("toilet", "普通马桶"),
        ("toilet", "蹲便"),
        ("toilet", "无"),
        ("stove", "无"),
        ("stove", "燃气灶"),
        ("stove", "电磁炉"),
        ("stove", "其他")
    ]

    @pytest.mark.parametrize("field, value", radio_all_options)
    def test_radio_button_selection(self, filing_room_page_setup, field, value):
        """
        测试单选按钮选择功能。
        该测试用例主要验证房间注册页面中的单选按钮是否能正确选中指定的选项。
        """
        filing_room_page = filing_room_page_setup
        label_text = self.radio_mapping[field]

        # 选择指定单选按钮
        select_radio_button(filing_room_page.page, label_text, value)

        # 验证是否正确选中
        assert is_radio_selected(filing_room_page.page, label_text, value)

    @pytest.mark.parametrize("field, value", radio_all_options)
    def test_radio_button_toggle(self, filing_room_page_setup, field, value):
        """
        测试单选按钮切换功能。
        该测试用例主要验证房间注册页面中的单选按钮是否能正确从一个选项切换到另一个选项。
        """
        filing_room_page = filing_room_page_setup
        time.sleep(1)
        label_text = self.radio_mapping[field]
        # 先选择相反的值（假设存在"有/无"）
        opposite_value = "无" if value == "有" else "有"
        if opposite_value in [v for f, v in self.radio_all_options if f == field]:
            select_radio_button(filing_room_page.page, label_text, opposite_value)
            assert is_radio_selected(filing_room_page.page, label_text, opposite_value), \
                f"单选按钮[{label_text}]选择[{opposite_value}]失败"

        # 再切换到目标值
        select_radio_button(filing_room_page.page, label_text, value)
        assert is_radio_selected(filing_room_page.page, label_text, value), \
            f"单选按钮[{label_text}]切换到[{value}]失败"

    def test_radio_initial_state(self, filing_room_page_setup):
        """
        测试所有单选按钮初始状态为未选中。
        该测试用例主要验证房间注册页面中的所有单选按钮在页面加载时是否都处于未选中状态。

        """
        filing_room_page = filing_room_page_setup
        time.sleep(1)

        for field, label_text in self.radio_mapping.items():
            # 获取该字段的所有选项
            options = [v for f, v in self.radio_all_options if f == field]

            # 验证所有选项初始状态均为未选中
            for option in options:
                assert not is_radio_selected(filing_room_page.page, label_text, option)

    @pytest.mark.parametrize("field", radio_mapping.keys())
    def test_radio_mutual_exclusion(self, filing_room_page_setup, field):
        """
        测试单选按钮组的互斥性。
        该测试用例主要验证房间注册页面中的单选按钮组是否具有互斥性，即同一组单选按钮中只能有一个选项被选中。
        """
        filing_room_page = filing_room_page_setup
        label_text = self.radio_mapping[field]

        # 获取该字段的所有选项
        options = [v for f, v in self.radio_all_options if f == field]

        for option in options:
            # 选择当前选项
            select_radio_button(filing_room_page.page, label_text, option)

            # 验证只有当前选项被选中，其他选项均未被选中
            for other_option in options:
                if other_option == option:
                    assert is_radio_selected(filing_room_page.page, label_text, other_option)
                else:
                    assert not is_radio_selected(filing_room_page.page, label_text, other_option)

    # 场景5：文件删除功能测试
    file_delete_cases = [
        ("property_certificate", "自有", "产权证明"),
        ("property_certificate", "租赁", "租赁证明"),
        ("property_certificate", "共有", "共有产权证明"),
        ("fire_safety_certificate", None, "消防合格证明"),
        ("public_security_registration_form", None, "网约房治安管理登记表"),
    ]
    file_delete_ids = [
        "delete_property_certificate_owned",
        "delete_property_certificate_leased",
        "delete_property_certificate_shared",
        "delete_fire_safety_certificate",
        "delete_public_security_form",
    ]

    @pytest.mark.parametrize("field, property_type, label_text", file_delete_cases, ids=file_delete_ids)
    def test_file_deletion(self, filing_room_page_setup, field, property_type, label_text):
        """
        测试各类上传文件的删除功能（包括产权类型：自有租赁，共有，以及不同产权类型页面对应的提示词是否正确）。
        该测试用例主要验证房间注册页面中上传的文件是否能正确删除，包括验证文件上传成功和删除成功。

        """
        filing_room_page = filing_room_page_setup
        params = FormValidationUtils._get_default_room_params()
        params["property_type"] = property_type
        # 上传测试文件
        if field == "property_certificate":
            filing_room_page.fill_room_info(test_fields=field, **params)
            filing_room_page.upload_property_certificate(
                property_type, JPG_PROPERTY_CERTIFICATE, test_fields=field
            )
        elif field == "fire_safety_certificate":
            filing_room_page.upload_fire_safety_certificate(
                JPG_PROPERTY_CERTIFICATE, test_fields=field
            )
        elif field == "public_security_registration_form":
            filing_room_page.upload_public_security_registration_form(
                JPG_PROPERTY_CERTIFICATE, test_fields=field
            )

        # 等待上传完成
        time.sleep(2)

        # 验证文件已上传
        if field == "property_certificate":
            assert filing_room_page.is_property_certificate_uploaded(label_text)
        elif field == "fire_safety_certificate":
            assert filing_room_page.is_fire_safety_certificate_uploaded(label_text)
        elif field == "public_security_registration_form":
            assert filing_room_page.is_public_security_registration_form_uploaded(label_text)

        # 删除文件
        filing_room_page.delete_uploaded_file(label_text)

        # 验证文件已删除
        time.sleep(2)
        if field == "property_certificate":
            assert not filing_room_page.is_property_certificate_uploaded(label_text)
        elif field == "fire_safety_certificate":
            assert not filing_room_page.is_fire_safety_certificate_uploaded(label_text)
        elif field == "public_security_registration_form":
            assert not filing_room_page.is_public_security_registration_form_uploaded(label_text)

    # 场景6：房间数量与文件输入框关联验证用例
    number_format_cases = [
        ("bedroom_number", "1,1,1,1"),
        ("bedroom_number", "2,1,1,1"),
        ("living_room_number", "1,2,1,1"),
        ("kitchen_number", "1,1,2,1"),
        ("bathroom_number", "1,1,1,2"),
    ]
    number_format_ids = [
        "origianl",
        "increase_bedroom_number",
        "increase_living_room_numbe",
        "increase_kitchen_number",
        "increase_bathroom_number",
    ]

    @pytest.mark.parametrize("field, test_value", number_format_cases, ids=number_format_ids)
    def test_number_format_validation(self, request, filing_room_page_setup, field, test_value):
        """
        测试房间数量格式的合法性验证。
        该测试用例主要验证房间数量输入与文件输入框之间的关联逻辑，确保输入合法的房间数量后，文件输入框的验证逻辑正确。

        """
        filing_room_page = filing_room_page_setup
        params = FormValidationUtils.get_form_params("room", field, test_value)
        current_test_id = request.node.name
        logger.info(f"📌 当前测试场景：: {current_test_id}")
        filing_room_page.fill_room_info(test_fields=field, **params)
        assert filing_room_page.validate_file_inputs(
            params["bedroom_number"],
            params["living_room_number"],
            params["kitchen_number"],
            params["bathroom_number"]
        )

    # 场景7：备案房间成功用例
    def test_room_register_success_redirect(self, filing_room_page_setup):
        """
        测试房间注册成功后是否正确跳转到指定页面。
        """
        filing_room_page = filing_room_page_setup
        # 准备合法的房间信息
        params = {
            "room_name": "Test Room",
            "property_type":"自有",
            "ms_name": "手持机民宿",
            "floor": "六层",
            "ly_name": "一栋一单元",
            "room_type": "大床房",
            "bedroom_number": "1",
            "living_room_number": "1",
            "kitchen_number": "1",
            "bathroom_number": "1",
            "area": "10",
            "bed_number": "1",
            "max_occupancy": "2",
            "parking": "有",
            "balcony": "有",
            "window": "有",
            "tv": "有",
            "projector": "无",
            "washing_machine": "有",
            "clothes_steamer": "无",
            "water_heater": "有",
            "hair_dryer": "有",
            "fridge": "有",
            "stove": "燃气灶",
            "toilet": "智能马桶",
        }

        # 填充房间信息
        # filing_room_page.fill_room_info(test_fields="all", **params)
        filing_room_page.filing_room(test_fields="all", property_certificate=JPEG_FIRE_SAFETY_CERTIFICATE,fire_safety_certificate= JPEG_FIRE_SAFETY_CERTIFICATE,
                                         public_security_registration_form= JPEG_PUBLIC_SECURITY_CERTIFICATE, bedroom_files= BEDROOM_FILES, living_room_files=LIVING_ROOM_FILES,
                                         kitchen_files=KITCHEN_FILES,bathroom_files=BATHROOM_FILES,**params)

        # 提交表单
        filing_room_page.submit_form()
        # 验证注册结果
        assert filing_room_page.check_register_result()

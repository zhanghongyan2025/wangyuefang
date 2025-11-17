import random

import pytest
from conf.logging_config import logger

class FormValidationUtils:
    """表单验证测试工具类（优化版）"""

    # 房产类型选项
    PROPERTY_TYPE_OPTIONS = ['自有', '租赁', '共有']

    # 登录表单字段映射配置
    LOGIN_FIELD_MAPPING = {
        "login_username": "login_username",
        "login_password": "login_password",
        "login_button": "login_button"
    }

    # 注册表单字段映射配置
    REGISTER_FIELD_MAPPING = {
        "username": "username",
        "password": "password",
        "confirm_password": "password_conform",
        "phone": "phone_number",
        "verify_code": "verify_code",
        "verify_code_button": "phone_number",  # 验证码按钮依赖手机号
        "person_in_charge": "person_in_charge",
        "person_in_charge_ID": "person_in_charge_ID",
        "person_in_charge_tel": "person_in_charge_tel",
        "enterprise_name": "enterprise_name",
        "USCC": "USCC",
    }

    # 房间信息表单字段映射配置
    ROOM_FIELD_MAPPING = {
        "room_name": "room_name",
        "property_type": "property_type",
        "ms_name": "ms_name",
        "floor": "floor",
        "ly_name": "ly_name",
        "room_type": "room_type",
        "bedroom_number": "bedroom_number",
        "living_room_number": "living_room_number",
        "kitchen_number": "kitchen_number",
        "bathroom_number": "bathroom_number",
        "area": "area",
        "bed_number": "bed_number",
        "max_occupancy": "max_occupancy",
        "parking": "parking",
        "balcony": "balcony",
        "window": "window",
        "tv": "tv",
        "projector": "projector",
        "washing_machine": "washing_machine",
        "clothes_steamer": "clothes_steamer",
        "water_heater": "water_heater",
        "hair_dryer": "hair_dryer",
        "fridge": "fridge",
        "stove": "stove",
        "toilet": "toilet",
    }

    @staticmethod

    def get_form_params(form_type: str, field: str, test_value: str) -> dict:
        """根据表单类型、测试字段和值生成表单参数字典"""
        if form_type == "login":
            mapping = FormValidationUtils.REGISTER_FIELD_MAPPING
            default_params = FormValidationUtils._get_default_login_params()
        elif form_type == "register":
            mapping = FormValidationUtils.REGISTER_FIELD_MAPPING
            default_params = FormValidationUtils._get_default_register_params()
        elif form_type == "room":
            mapping = FormValidationUtils.ROOM_FIELD_MAPPING
            default_params = FormValidationUtils._get_default_room_params()
        else:
            raise ValueError(f"不支持的表单类型: {form_type}")

        param_name = mapping.get(field, field)
        params = default_params.copy()
        params[param_name] = test_value

        # 特殊字段处理
        if form_type == "register":
            # 确认密码测试需要设置有效密码
            if field == "confirm_password":
                params["password"] = "ValidPwd123"
            # 验证码按钮点击需要有效手机号
            if field == "verify_code_button" and test_value:
                params["phone_number"] = test_value

        # 房产类型默认值处理
        if form_type == "room" and field != "property_type":
            params["property_type"] = "自有"

        # 房间数量字段处理
        room_number_fields = ["bedroom_number", "living_room_number", "kitchen_number", "bathroom_number"]
        if form_type == "room":
            # 处理"1,0,0,0"格式的值
            if field in room_number_fields and "," in test_value:
                values = test_value.split(',')
                if len(values) == len(room_number_fields):
                    for i, room_field in enumerate(room_number_fields):
                        room_param_name = mapping.get(room_field, room_field)
                        params[room_param_name] = values[i]
                    return params  # 提前返回，避免后续重复处理

            # 单个字段处理逻辑
            for room_field in room_number_fields:
                room_param_name = mapping.get(room_field, room_field)
                # 如果当前字段不是正在测试的字段，则随机生成值
                if room_field != field:
                    params[room_param_name] = str(random.randint(1, 3))
                # 如果当前字段是正在测试的字段，但值无效，则也随机生成
                elif not test_value or not test_value.isdigit() or int(test_value) not in range(1, 4):
                    params[room_param_name] = str(random.randint(1, 3))

        # 确保如果field在params里，其值最终为test_value
        if param_name in params:
            params[param_name] = test_value

        return params

    @staticmethod
    def get_error_selector(form_type: str, field: str, code_type: str = None) -> str:
        """根据表单类型和字段获取对应的错误元素选择器"""

        if form_type == "login":
            selector_map = FormValidationUtils._get_login_error_selectors()
        elif form_type == "register":
            selector_map = FormValidationUtils._get_register_error_selectors()
        elif form_type == "room":
            selector_map = FormValidationUtils._get_room_error_selectors()
        else:
            raise ValueError(f"不支持的表单类型: {form_type}")

        # 处理特殊情况：验证码错误选择器
        if field == "verify_code" and code_type:
            return f"verify_code_{code_type}_error"

        return selector_map.get(field, f"{field}_error")

    # 登录表单默认参数
    @staticmethod
    def _get_default_login_params() -> dict:
        """获取登录表单默认参数"""
        return {
            "login_username": "hongyan20256",
            "login_password": "Aa123123!",
        }

    @staticmethod
    def _get_default_register_params() -> dict:
        """获取注册表单默认参数"""
        return {
            "username": "",
            "password": "",
            "password_conform": "",
            "phone_number": "",
            "verify_code": "",
            "person_in_charge": "",
            "person_in_charge_ID": "",
            "person_in_charge_tel": "",
            "enterprise_name": "",
            "USCC": "",
        }

    @staticmethod
    def _get_default_room_params() -> dict:
        """获取房间信息表单默认参数"""
        return {
            "room_name": "",
            "property_type": "自有",  # 设置默认值为自有
            "ms_name": "",
            "floor": "",
            "ly_name": "",
            "room_type": "",
            "bedroom_number": "",
            "living_room_number": "",
            "kitchen_number": "",
            "bathroom_number": "",
            "area": "",
            "bed_number": "",
            "max_occupancy": "",
            "parking": "",
            "balcony": "",
            "window": "",
            "tv": "",
            "projector": "",
            "washing_machine": "",
            "clothes_steamer": "",
            "water_heater": "",
            "hair_dryer": "",
            "fridge": "",
            "stove": "",
            "toilet": "",
        }


    @staticmethod
    def _get_login_error_selectors() -> dict:  # 新增登录表单错误选择器
        """获取登录表单错误选择器映射"""
        return {
            "username": "login_username_error",
            "password": "login_password_error",
            "login_button": "login_error"  # 登录按钮点击后的错误提示
        }

    @staticmethod
    def _get_register_error_selectors() -> dict:
        """获取注册表单错误选择器映射"""
        return {
            "username": "username_error",
            "password": "password_error",
            "confirm_password": "confirm_password_error",
            "phone": "phone_error",
            "verify_code": "verify_code_error",
            "verify_code_button": "phone_error",  # 验证码按钮点击验证手机号
            "person_in_charge": "legal_name_error",
            "person_in_charge_ID": "id_card_error",
            "person_in_charge_tel": "legal_tel_error",
            "enterprise_name": "enterprise_name_error",
            "USCC": "USCC_error",
        }

    @staticmethod
    def _get_room_error_selectors() -> dict:
        """获取房间信息表单错误选择器映射"""
        return {
            "room_name": "room_name_error",
            "property_type": "property_type_check",
            "ms_name": "ms_name_error",
            "floor": "floor_error",
            "ly_name": "ly_name_error",
            "room_type": "room_type_error",
            "bedroom_number": "bedroom_number_error",
            "living_room_number": "living_room_number_error",
            "kitchen_number": "kitchen_number_error",
            "bathroom_number": "bathroom_number_error",
            "area": "area_error",
            "bed_number": "bed_number_error",
            "max_occupancy": "max_occupancy_error",
            "parking": "parking_error",
            "balcony": "balcony_error",
            "window": "window_error",
            "tv": "tv_error",
            "projector": "projector_error",
            "washing_machine": "washing_machine_error",
            "clothes_steamer": "clothes_steamer_error",
            "water_heater": "water_heater_error",
            "hair_dryer": "hair_dryer_error",
            "fridge": "fridge_error",
            "stove": "stove_error",
            "toilet": "toilet_error",
            "public_security_registration_form": "public_security_registration_form_error",
        }
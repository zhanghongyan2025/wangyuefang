import random
import string

from faker import Faker
from utils.id_card_validator import validate_id_card  # 新增校验模块

# 创建Faker实例，用于生成各种随机数据
fake = Faker('zh_CN')

# 企业类型列表（限定为制造企业和销售企业）
enterprise_types = ["制造企业", "销售企业"]

# 经营范围列表（限定为射钉器、射钉弹、射钉器和射钉弹）
scopes = ["射钉器", "射钉弹", "射钉器和射钉弹"]


def generate_random_credit_code():
    """生成随机的统一社会信用代码"""
    # 统一社会信用代码由18位数字或字母组成
    characters = string.digits + 'ABCDEFGHJKLMNPQRTUWXY'
    return ''.join(random.choice(characters) for _ in range(18))


def generate_random_phone():
    """生成随机的11位手机号码"""
    return '1' + ''.join(random.choice(string.digits) for _ in range(10))


def generate_id_card():
    """生成符合国家标准的18位身份证号码"""
    # 使用Faker生成原始身份证号码（包含校验码）
    raw_id = fake.ssn(min_age=18, max_age=80)  # 生成18位有效身份证

    # 验证并确保格式正确
    if validate_id_card(raw_id):
        return raw_id
    else:
        # 递归重试（极个别情况Faker可能生成无效号码）
        return generate_id_card()


def generate_registration_data(num_users=500):
    """生成指定数量的用户注册数据"""
    data_list = []

    for i in range(1, num_users + 1):
        # 硬编码省份、城市和区县
        province = "山东省"
        city = "潍坊市"
        district = "坊子区"

        # 构建地址字符串
        address = f"{province}{city}{district}"

        # 生成企业名称
        enterprise_name = f"{fake.company_prefix()}{fake.company_suffix()}_{i}"

        # 生成法定代表人姓名
        legal_representative = f"{fake.last_name()}{fake.first_name_male() if random.random() > 0.3 else fake.first_name_female()}_{i}"

        # 生成统一社会信用代码
        unified_social_credit_code = generate_random_credit_code()

        # 生成注册地址和经营场所
        registered_address = f"{province}{city}{district}{fake.street_address()}_{i}"
        business_location = f"{province}{city}{district}{fake.building_number()}{fake.street_name()}_{i}"

        # 生成安全负责人姓名
        safety_director = f"{fake.last_name()}{fake.first_name_male() if random.random() > 0.3 else fake.first_name_female()}_{i}"

        # 生成经营范围（从限定列表中选择）
        scope = random.choice(scopes)

        # 生成电话号码
        telephone = generate_random_phone()

        # 生成营业执照路径
        business_license_path = f"C:\\Users\\Administrator\\Pictures\\Screenshots\\1.png"
        enterprise_type = random.choice(enterprise_types)

        # 创建注册数据字典
        data = {
            "enterprise_name": enterprise_name,
            "enterprise_type": enterprise_type,
            "province": province,
            "city": city,
            "district": district,
            "legal_representative": legal_representative,
            "unified_social_credit_code": unified_social_credit_code,
            "registered_address": registered_address,
            "business_location": business_location,
            "telephone": telephone,
            "safety_director": safety_director,
            "scope": scope,
            "business_license_path": business_license_path
        }

        if enterprise_type == "销售企业":
            data[
                "handle_by"] = f"{fake.last_name()}{fake.first_name_male() if random.random() > 0.3 else fake.first_name_female()}_{i}"
            data["handler_tel"] = generate_random_phone()
            data["handler_ID"] = generate_id_card()
            data_list.append(data)

    return data_list    
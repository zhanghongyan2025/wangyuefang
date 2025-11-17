import json
import re
import time
import pytest
from playwright.sync_api import expect

from conf.config import *
from conf.logging_config import logger
from tests.pages.fd.add_new_minsu import AddNewMinsuPage
from tests.utils.validation_utils import check_add_new_minsu_error_messages, assert_filed_messages


# ------------------------------
# 工具函数：注册页面错误提示验证
# ------------------------------


# ------------------------------
# 测试类：个人/企业房东注册功能测试
# ------------------------------
@pytest.mark.register
class TestAddNewMinsu:
    """添加民宿功能测试类"""

    # ------------------------------
    # 场景1：民宿信息-空字段验证
    # ------------------------------
    empty_cases = [
        # (场景标识, 各字段值, 预期错误)
        (
            "all_fields_empty",
            {
                "minsu_name": "",
                "detail_address":"",
                "province":"",
                "city": "",
                "district": "",
                "street": "",
                "front_image": "",
                "back_image": ""
            },
            {
                "minsu_name": "民宿名称不能为空",
                "administrative_area": "请选择乡/镇/街道行政区划",
                "detail_address": "详细地址不能为空",
                "front_image": "请上传负责人证件照(正面)",
                "back_image": "请上传负责人证件照(反面)"
            }
        )
    ]
    empty_ids = [case[0] for case in empty_cases]

    @pytest.mark.parametrize(
        "scenario, fields, expected_errors",
        empty_cases,
        ids=empty_ids
    )
    def test_minsu_empty_fields(
            self,
            scenario,
            fields,
            expected_errors,
            add_new_minsu_setup  # 将fixture作为参数传入，pytest会自动处理其依赖
    ):
        """
        测试民宿新增页面的空字段验证逻辑
        1.所有字段都为空
        """
        # 直接使用fixture返回的对象，无需手动调用
        add_new_minsu_page = add_new_minsu_setup
        # 点击提交按钮
        add_new_minsu_page.add_new_minsu(**fields)
        add_new_minsu_page.save_minsu_info()
        # 验证错误提示
        logger.info(f"📌 民宿新增场景：执行空字段测试 [{scenario}]")
        for field, expected_tip in expected_errors.items():
                assert check_add_new_minsu_error_messages(add_new_minsu_page, field, expected_tip), \
                    (
                        f"❌  场景[{scenario}], 字段 [{field}] 错误提示不匹配 - "
                        f"预期: {expected_tip}, 实际未匹配"
                    )


    # 场景2：民宿名称长度限制测试用例
    name_length_cases = [
        (
            "name_exceed_30_chars",
            {
                "minsu_name": "这是一个超过三十个字符的民宿名称用于测试长度限制情况且长度大于三十",  # 33个字符
                **COMMON_minsu_PARAMS,
            },
            {
                "minsu_name": "最多30个字符"
            }
        ),
        (
            "name_exactly_30_chars",
            {
                "minsu_name": "这是一个刚好三十个字符的民宿名称用于测试长度限制",  # 30个字符
                 **COMMON_minsu_PARAMS,
            },
            {"add_success": "保存成功"}  # 无错误
        ),
        (
            "name_under_30_chars",
            {
                "minsu_name": "短",  # 6个字符
                 **COMMON_minsu_PARAMS,
            },
            {"add_success": "保存成功"}
        )
    ]
    name_length_ids = [case[0] for case in name_length_cases]

    @pytest.mark.parametrize(
        "scenario, fields, expected_errors",
        name_length_cases,
        ids=name_length_ids
    )
    def test_minsu_name_length_fields(
            self,
            scenario,
            fields,
            expected_errors,
            minsu_management_setup,   # 将fixture作为参数传入，pytest会自动处理其依赖
            page):
        """
        测试民宿新增页面的民宿名称长度验证逻辑
        1.民宿名称长度超过30个字段
        2.民宿名称长度正好30个字段
        3.民宿名称长度小于30个字段
        """
        # 直接使用fixture返回的对象，无需手动调用
        minsu_management_page = minsu_management_setup
        # 点击提交按钮
        minsu_management_page.minsu_delete(fields["minsu_name"])
        minsu_management_page.go_to_add_minsu_page()
        add_new_minsu_page = AddNewMinsuPage(page)
        add_new_minsu_page.add_new_minsu(**fields)

        # 验证错误提示
        logger.info(f"📌 民宿新增场景：执行空字段测试 [{scenario}]")

        assert_filed_messages(
            page=add_new_minsu_page,
            scenario=scenario,
            expected_errors=expected_errors,  # 预期的成功/错误信息字典
            check_success_func=lambda page, tip: page.add_new_minsu_success_alert(tip),
            check_error_func=check_add_new_minsu_error_messages
        )


    # 场景3：详细地址长度限制测试用例
    detail_adress_length_cases = [
        # 1：详细地址超过50字符 → 预期失败（提示“最多50个字符”）
        (
            "detail_address_exceed_50_chars",  # 用例名：清晰标识测试目标
            {
                "minsu_name": "详细地址51个字符的民宿",  # 非核心字段用正常值即可
                 **COMMON_minsu_PARAMS,
                "detail_address": "是一段用于测试详细地址超过50字符限制的文本，共51个中文字符，验证是否会触发错误提示:最多50个字符",

            },
            {"detail_address": "最多50个字符"}  # 预期错误提示
        ),
        # 2：详细地址刚好50字符 → 预期成功（无错误，保存成功）
        (
            "detail_address_exactly_50_chars",  # 用例名：明确“刚好50字符”
            {
                "minsu_name": "详细地址刚好50个字符的民宿",
                **COMMON_minsu_PARAMS,
                "detail_address": "是一段用于测试详细地址超过50字符限制的文本，共50个中文字符，验证是否会触发错误提示:保存成功弹框",

            },
            {"add_success": "保存成功"}  # 预期正常保存
        ),
        # # 3：详细地址少于50字符 → 预期成功（正常场景）
        (
            "detail_address_under_50_chars",  # 用例名：明确“少于50字符”
            {
                "minsu_name": "详细地址1个字符的民宿",
                **COMMON_minsu_PARAMS,
                "detail_address": "鼓",
            },
            {"add_success": "保存成功"}  # 预期正常保存
        )
    ]
    detail_adress_length_ids = [case[0] for case in detail_adress_length_cases]

    @pytest.mark.parametrize(
        "scenario, fields, expected_errors",
        detail_adress_length_cases,
        ids=detail_adress_length_ids
    )
    def test_minsu_detail_adress(
            self,
            scenario,
            fields,
            expected_errors,
            minsu_management_setup,  # 将fixture作为参数传入，pytest会自动处理其依赖
            page):
        """
        测试民宿新增页面的详细地址字段验证逻辑
        1.详细地址长度超过50个字符
        2.详细地址长度正好50个字符
        3.详细地址长度小于50个字符
        """
        minsu_management_page = minsu_management_setup

        minsu_management_page.minsu_delete(fields["minsu_name"])

        minsu_management_page.go_to_add_minsu_page()
        add_new_minsu_page = AddNewMinsuPage(page)
        fields["detail_address"] = fields["detail_address"]
        add_new_minsu_page.add_new_minsu(**fields)
        # 验证错误提示
        logger.info(f"📌 民宿新增场景：测试 [{scenario}]")

        assert_filed_messages(
                page=add_new_minsu_page,
                scenario=scenario,
                expected_errors=expected_errors,  # 预期的成功/错误信息字典
                check_success_func=lambda page, tip: page.add_new_minsu_success_alert(tip),
                check_error_func=check_add_new_minsu_error_messages
            )

    # 场景4：身份证正反面上传验证测试用例（补充jpg/jpeg细节）
    id_card_upload_cases = [
        # 1. 合法情况测试
        # 1.1 正面jpg + 反面jpeg（均合法）
        (
            "both_valid_jpg_jpeg",
            {
                "front_image": JPG_ID_CARD,  # 合法jpg
                "back_image": JPEG_ID_CARD,  # 合法jpeg
            },
            {"add_ID_card_images_success": "保存成功"}
        ),
        # 1.2 正面png + 反面jpg（均合法）
        (
            "both_valid_png_jpg",
            {
                "front_image": PNG_ID_CARD,  # 合法png
                "back_image": JPG_ID_CARD,  # 合法jpg
            },
            {"add_ID_card_images_success": "保存成功"}
        ),
        # 1.3 正面刚好10MB jpg（边界测试）
        (
            "front_exactly_10mb_jpg",
            {
                "front_image": EXACTLY_10M_ID_CARD,  # 10MB jpg
                "back_image": PNG_ID_CARD,  # 合法png
            },
            {"add_ID_card_images_success": "保存成功"}
        ),

        # 2. 大小限制测试（超过10MB）
        # 2.1 正面超过10MB（png）
        (
            "front_exceed_10mb_png",
            {
                "front_image": LARGE_ID_CARD,  # 超过10M
                "back_image": JPEG_ID_CARD,  # 正常jpeg
            },
            {"add_ID_card_failed": "上传头像图片大小不能超过 10 MB!"}
        ),
        # 2.2 反面超过10MB（png）
        (
            "back_exceed_10mb_png",
            {
                "front_image": JPG_ID_CARD,  # 正常jpg
                "back_image": LARGE_ID_CARD,  # 超过10M
            },
            {"add_ID_card_failed": "上传头像图片大小不能超过 10 MB!"}
        ),
        # 2.3 正反两面都超过10MB
        (
            "both_exceed_10mb",
            {
                "front_image": LARGE_ID_CARD,  # 超过10M
                "back_image": LARGE_ID_CARD,  # 超过10M
            },
            {"add_ID_card_failed": "上传头像图片大小不能超过 10 MB!"}
        ),

        # 3. 格式限制测试（不支持的格式）
        # 3.1 正面为exe（扩展名欺骗）
        (
            "front_disguised_exe",
            {
                "front_image": EXE_ID_CARD,  # 改名为.jpg的exe
                "back_image": PNG_ID_CARD,  # 合法png
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.2 反面为bmp格式
        (
            "back_invalid_bmp",
            {
                "front_image": JPEG_ID_CARD,  # 合法jpeg
                "back_image": BMP_ID_CARD,  # bmp格式
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.3 正面为pdf格式
        (
            "front_invalid_pdf",
            {
                "front_image": PDF_ID_CARD,  # pdf格式
                "back_image": PNG_ID_CARD,  # 合法png
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.4 反面为php格式
        (
            "back_invalid_php",
            {
                "front_image": JPG_ID_CARD,  # 合法jpg
                "back_image": PHP_ID_CARD,  # php格式
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.5 正面为python脚本
        (
            "front_invalid_python",
            {
                "front_image": PY_ID_CARD,  # python格式
                "back_image": JPEG_ID_CARD,  # 合法jpeg
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.6 反面为svg格式
        (
            "back_invalid_svg",
            {
                "front_image": PNG_ID_CARD,  # 合法png
                "back_image": SVG_ID_CARD,  # svg格式
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.7 正面为txt格式
        (
            "front_invalid_txt",
            {
                "front_image": TXT_ID_CARD,  # txt格式
                "back_image": JPG_ID_CARD,  # 合法jpg
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.8 反面为zip格式
        (
            "back_invalid_zip",
            {
                "front_image": JPEG_ID_CARD,  # 合法jpeg
                "back_image": ZIP_ID_CARD,  # zip格式
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),
        # 3.9 正面为html格式
        (
            "front_invalid_html",
            {
                "front_image": HTML_ID_CARD,  # html格式
                "back_image": PNG_ID_CARD,  # 合法png
            },
            {"add_ID_card_failed": "文件格式不正确, 请上传jpg/jpeg/png图片格式文件!"}
        ),

        # 4. 混合场景测试
        # 4.1 正面合法jpg + 反面超大且格式不合法
        (
            "back_large_invalid_front_valid",
            {
                "front_image": JPG_ID_CARD,  # 合法jpg
                "back_image": LARGE_ID_CARD,  # 超大且可能格式问题
            },
            {"add_ID_card_failed": "上传头像图片大小不能超过 10 MB!"}
        ),
        # # 4.2 正面超大 + 反面格式不合法
        # (
        #     "both_failed_front_large_back_invalid",
        #     {
        #         "front_image": LARGE_ID_CARD,  # 超大
        #         "back_image": EXE_ID_CARD,  # 格式不合法
        #     },
        #     {"add_ID_card_failed": "上传头像图片大小不能超过 10 MB!"}
        # )
    ]

    id_card_upload_ids = [case[0] for case in id_card_upload_cases]


    @pytest.mark.parametrize(
        "scenario, fields, expected_errors",
        id_card_upload_cases,
        ids=id_card_upload_ids
    )
    def test_id_card_upload_validation(
            self,
            scenario,
            fields,
            expected_errors,
            add_new_minsu_setup  # 复用页面初始化fixture
    ):
        """
        测试身份证上传的大小限制（≤10MB）和格式限制（jpg/jpeg/png）
        1. 正面jpg + 反面jpeg（均合法）
        2. 正面png + 反面jpg（均合法）
        3. 正面刚好10MB jpg（边界测试）
        4. 大小限制测试（超过10MB），正面超过10MB（png）
        5. 反面超过10MB（png）
        6. 正反两面都超过10MB
        7. 正面为exe（扩展名欺骗）
        8. 反面为bmp格式
        9. 正面为pdf格式
        10. 反面为php格式
        11. 正面为python脚本
        12. 反面为svg格式
        13. 正面为txt格式
        14. 反面为zip格式
        15. 正面为html格式
        16. 正面合法jpg + 反面超大且格式不合法
        """

        add_new_minsu_page = add_new_minsu_setup

        logger.info(f"📌 执行身份证上传测试场景：[{scenario}]")
        if scenario.startswith("front"):
            add_new_minsu_page.upload_front_id_card_image(fields["front_image"])
            for field, expected_tip in expected_errors.items():
                if expected_tip == "保存成功":
                    assert add_new_minsu_page.add_ID_card_front_image_success_error()
                else:
                    assert add_new_minsu_page.add_ID_card_failed_alert_error(expected_tip)
            add_new_minsu_page.upload_back_id_card_image(fields["back_image"])
            assert add_new_minsu_page.add_ID_card_back_image_success_error()

        elif scenario.startswith("back"):
            add_new_minsu_page.upload_front_id_card_image(fields["front_image"])
            assert add_new_minsu_page.add_ID_card_front_image_success_error()

            add_new_minsu_page.upload_back_id_card_image(fields["back_image"])
            for field, expected_tip in expected_errors.items():
                assert  add_new_minsu_page.add_ID_card_failed_alert_error( expected_tip
                ), f"场景[{scenario}]成功提示不匹配：预期[{expected_tip}]"
        elif scenario.startswith("both_valid"):
            add_new_minsu_page.upload_front_id_card_image(fields["front_image"])
            assert add_new_minsu_page.add_ID_card_front_image_success_error()
            add_new_minsu_page.upload_back_id_card_image(fields["back_image"])
            assert add_new_minsu_page.add_ID_card_back_image_success_error()
        else:
            add_new_minsu_page.upload_front_id_card_image(fields["front_image"])
            for field, expected_tip in expected_errors.items():
                assert add_new_minsu_page.add_ID_card_failed_alert_error(expected_tip), f"场景[{scenario}]成功提示不匹配：预期[{expected_tip}]"
            add_new_minsu_page.upload_back_id_card_image(fields["back_image"])
            for field, expected_tip in expected_errors.items():
                assert add_new_minsu_page.add_ID_card_failed_alert_error(expected_tip), f"场景[{scenario}]成功提示不匹配：预期[{expected_tip}]"

        time.sleep(2)




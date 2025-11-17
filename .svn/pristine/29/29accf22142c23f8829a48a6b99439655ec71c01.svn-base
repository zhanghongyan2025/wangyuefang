# base page operations
import time
from typing import Union, List
from faker import Faker
from typing import Optional, List
from playwright.async_api import Page, Locator
from conf.logging_config import logger
from tests.utils.validator import *


def find_file_input(label):
    """
    查找标签对应的文件输入框

    Args:
        label: 标签元素

    Returns:
        ElementHandle: 文件输入框元素，如果未找到则返回None
    """
    try:
        return label.query_selector('xpath=following-sibling::div').query_selector(
            'xpath=//input[@type="file"]')
    except AttributeError:
        return None

def scroll_to_bottom(page: Page) -> None:
    """
    滚动到页面底部

    :param page: Playwright的Page对象
    """
    try:
        # 按下End键，尝试快速滚动到页面底部
        page.keyboard.press('End')
        # 等待500毫秒，确保页面滚动完成
        page.wait_for_timeout(500)

        # 循环5次，每次按下PageDown键，进一步微调滚动位置
        for _ in range(5):
            page.keyboard.press('PageDown')
            page.wait_for_timeout(300)
    except Exception as e:
        # 若滚动过程中出现异常，记录错误日志
        logger.error(f"滚动到页面底部时出错: {e}")

def scroll_to_keywords_view(page: Page, keywords) -> None:
    """
    滚动到包含指定关键字的元素可见区域

    :param page: Playwright的Page对象
    :param keywords: 要查找的关键字
    """
    try:
        # 定位包含指定关键字的元素（模糊匹配）
        element = page.locator(f':text-matches(".*{keywords}.*")')
        # 滚动到元素位置，确保元素可见
        element.scroll_into_view_if_needed()
    except Exception as e:
        # 若滚动过程中出现异常，记录错误日志
        logger.error(f"滚动到关键字 {keywords} 视图时出错: {e}")

def locate_elements_by_step_strategy(target_label: Locator, xpath: str) -> Optional[Locator]:
    """
    使用分步策略定位元素

    :param target_label: 标签元素的Locator
    :param xpath: 自定义XPath表达式
    :return: 定位到的元素Locator或None
    """
    # 尝试分步定位策略
    steps = xpath.split('//', 1)  # 拆分为两部分

    if len(steps) > 1:
        first_step, remaining_steps = steps
        # 第一步：定位到中间元素
        middle_locator = target_label.locator(f'xpath={first_step}')
        # 检查第一步是否成功
        if middle_locator.count() > 0:
            # logger.info(f"第一步定位成功: {first_step}")
            # 第二步：在中间元素基础上继续定位
            final_locator = middle_locator.locator(f'xpath=//{remaining_steps}')
            try:
                # 返回所有定位到的元素
                return final_locator
            except TimeoutError:
                pass  # 继续尝试其他策略

    # 原始的整体定位策略作为后备
    # logger.info(f"尝试整体定位: {xpath}")
    relative_locator = target_label.locator(f'xpath={xpath}')
    try:
        # 返回所有定位到的元素
        return relative_locator.all()
    except TimeoutError:
        # 若定位超时，抛出异常
        raise ValueError(f"对应的元素，XPath: {xpath}")

def locate_element_by_step_strategy(target_label: Locator, xpath: str) -> Locator:
    """
    使用分步策略定位单个元素（确保返回非空Locator）

    :param target_label: 标签元素的Locator
    :param xpath: 自定义XPath表达式
    :return: 定位到的单个元素Locator
    :raises ValueError: 当元素无法定位时抛出异常
    """
    # 尝试分步定位策略
    steps = xpath.split('//', 1)  # 拆分为两部分

    if len(steps) > 1:
        first_step, remaining_steps = steps
        # 第一步：定位到中间元素
        middle_locator = target_label.locator(f'xpath={first_step}')
        # 检查第一步是否成功
        if middle_locator.count() > 0:
            # logger.info(f"第一步定位成功: {first_step}")
            # 第二步：在中间元素基础上继续定位
            final_locator = middle_locator.locator(f'xpath=//{remaining_steps}')
            # 使用nth(0)确保返回Locator对象，元素不存在时会触发超时
            return final_locator.nth(0)

    # 原始的整体定位策略作为后备
    # logger.info(f"尝试整体定位: {xpath}")
    relative_locator = target_label.locator(f'xpath={xpath}')
    # 使用nth(0)确保返回Locator对象，元素不存在时会触发超时
    element = relative_locator.nth(0)

    # 显式检查元素是否存在（超时处理）
    try:
        return element
    except TimeoutError:
        raise ValueError(f"无法定位元素，XPath: {xpath}")

def upload_file(page: Page, file_path: str) -> None:
    """
    上传文件

    :param page: Playwright的Page对象
    :param file_path: 要上传的文件路径
    """
    try:
        # 先滚动到页面底部
        scroll_to_bottom(page)
        # 查询页面上的文件输入框
        upload_input = page.query_selector('input[type="file"]')
        if upload_input is None:
            # 若未找到文件输入框，抛出异常
            raise ValueError("未找到文件输入框")
        # 设置要上传的文件路径
        upload_input.set_input_files(file_path)
    except Exception as e:
        # 若上传文件过程中出现异常，记录错误日志
        logger.error(f"上传文件 {file_path} 时出错: {e}")

def get_label_corresponding_content(page: Page, element, label_text, value_locator_xpath) -> str:
    """
    获取指定标签对应的内容，例如获取用户名密码的值

    :param page: Playwright的Page对象
    :param element: 定位的基础元素
    :param label_text: 标签文本
    :param value_locator_xpath: 用于定位值的XPath表达式
    :return: 标签对应的内容
    """
    try:
        # 定位指定标签元素
        target_label = element.locator(f'label:has-text("{label_text}")')
        # 定位标签对应的内容元素
        target_value = target_label.locator(f'xpath={value_locator_xpath}')
        # 获取内容元素的文本内容
        return target_value.text_content()
    except Exception as e:
        # 若获取内容过程中出现异常，记录错误日志并抛出异常
        logger.error(f"获取标签 {label_text} 对应的内容时出错: {e}")
        raise

def get_label_corresponding_error_tip(page: Page, label_text: str, expected_message):
    """
    获取指定标签对应的错误提示信息，并验证是否符合预期

    :param page: Playwright的Page对象
    :param label_text: 标签文本
    :param expected_message: 预期的错误提示信息
    """
    try:
        # 定位指定标签元素
        target_label = page.get_by_text(label_text, exact=True)
        # 定位标签对应的错误提示元素
        target_element = target_label.locator('.el-form-item__error')
        # 获取错误提示元素的文本内容并去除首尾空白
        error_text = target_element.text_content().strip()
        # 验证错误提示信息是否符合预期
        assert error_text == expected_message, f"错误提示信息不符，预期: {expected_message}，实际: {error_text}"
    except AssertionError as ae:
        # 若验证失败，记录错误日志并抛出异常
        logger.error(f"验证标签 {label_text} 的错误提示信息时出错: {ae}")
        raise
    except Exception as e:
        # 若获取错误提示信息过程中出现其他异常，记录错误日志并抛出异常
        logger.error(f"获取标签 {label_text} 对应的错误提示信息时出错: {e}")
        raise

def get_label_corresponding_input(page: Page, label_text) -> Locator:
    """
    获取指定标签对应的输入框

    :param page: Playwright的Page对象
    :param label_text: 标签文本
    :return: 定位到的输入框Locator对象
    """
    try:
        # 定位指定标签元素
        target_label = page.get_by_text(label_text, exact=True)
        # 定位标签对应的输入框元素
        target_element = target_label.locator('xpath=following-sibling::div//input')
        return target_element
    except Exception as e:
        # 若获取输入框过程中出现异常，记录错误日志并抛出异常
        logger.error(f"获取标签 {label_text} 对应的输入框时出错: {e}")
        raise


def get_label_corresponding_element(page: Page, label_text: str, xpath: str) -> Locator:
    """
    获取与标签文本对应的表单元素（分步定位策略）

    :param page: Playwright的Page对象
    :param label_text: 标签文本内容
    :param xpath: 自定义XPath表达式，用于定位目标元素
    :return: 定位到的表单元素Locator，若未找到则返回None
    :raises ValueError: 未提供自定义XPath表达式
    """
    if not xpath:
        # 若未提供XPath表达式，抛出异常
        raise ValueError("必须提供自定义XPath表达式")
    try:
        # 定位标签元素
        target_label = page.get_by_text(label_text, exact=True)
        # 检查标签是否可见
        if not target_label.is_visible():
            # 若标签不可见，抛出异常
            raise ValueError(f"未找到标签文本: '{label_text}'")

        # 尝试分步定位策略
        steps = xpath.split('//', 1)  # 拆分为两部分

        if len(steps) > 1:
            first_step, remaining_steps = steps
            # 第一步：定位到中间元素
            middle_locator = target_label.locator(f'xpath={first_step}')
            # 检查第一步是否成功
            if middle_locator.count() > 0 and middle_locator.is_visible():
                # logger.info(f"第一步定位成功: {first_step}")
                # 第二步：在中间元素基础上继续定位
                final_locator = middle_locator.locator(f'xpath=//{remaining_steps}')

                # 新增：检查最终元素是否存在
                if final_locator.count() == 0:
                    logger.info(f"第二步定位未找到元素: //{remaining_steps}")
                    return None

                return final_locator

        # 原始的整体定位策略作为后备
        # logger.info(f"尝试整体定位: {xpath}")
        relative_locator = target_label.locator(f'xpath={xpath}')

        # 新增：检查是否找到元素
        if relative_locator.count() == 0:
            return None

        return relative_locator
    except TimeoutError:
        # 若定位超时，返回None而非抛出异常
        logger.warning(f"定位超时，未找到与标签 '{label_text}' 对应的可见元素，XPath: {xpath}")
        return None
    except Exception as e:
        # 若出现其他异常，记录错误日志并抛出异常
        logger.error(f"获取标签 {label_text} 对应的元素时出错: {e}")
        raise

def get_label_corresponding_elements(page: Page, label_text: str, xpath: str, timeout: int = 3000) -> List[Locator]:
    """
    获取与标签文本对应的所有表单元素（不强制要求元素可见）

    :param page: Playwright的Page对象
    :param label_text: 标签文本内容
    :param xpath: 自定义XPath表达式，用于定位目标元素
    :param timeout: 等待元素存在的超时时间（毫秒），默认为3000ms
    :return: 定位到的所有元素Locator列表
    :raises ValueError: 未找到匹配的元素
    """
    if not xpath:
        # 若未提供XPath表达式，抛出异常
        raise ValueError("必须提供自定义XPath表达式")
    try:
        # 定位标签元素
        target_label = page.get_by_text(label_text, exact=True)
        # 等待标签元素出现
        target_label.wait_for(timeout=timeout)
    except TimeoutError:
        # 若未找到精确匹配的标签元素，尝试非精确匹配作为后备
        target_label = page.get_by_text(label_text)
        try:
            # 等待非精确匹配的标签元素出现
            target_label.wait_for(timeout=timeout)
        except TimeoutError:
            # 若仍未找到标签元素，抛出异常
            raise ValueError(f"未找到标签文本: '{label_text}'")

    # 尝试分步定位策略
    steps = xpath.split('//', 1)  # 拆分为两部分

    if len(steps) > 1:
        first_step, remaining_steps = steps
        # 第一步：定位到中间元素
        middle_locator = target_label.locator(f'xpath={first_step}')
        # 检查第一步是否成功
        if middle_locator.count() > 0:
            #logger.info(f"第一步定位成功: {first_step}")
            # 第二步：在中间元素基础上继续定位
            final_locator = middle_locator.locator(f'xpath=//{remaining_steps}')
            try:
                # 返回所有定位到的元素
                return final_locator.all()
            except TimeoutError:
                pass  # 继续尝试其他策略

    # 原始的整体定位策略作为后备
    # logger.info(f"尝试整体定位: {xpath}")
    relative_locator = target_label.locator(f'xpath={xpath}')
    try:
        # 返回所有定位到的元素
        return relative_locator.all()
    except TimeoutError:
        # 若定位超时，抛出异常
        raise ValueError(f"未找到与标签 '{label_text}' 对应的元素，XPath: {xpath}")

def get_element_corresponding_error_tip(target_element: Locator, xpath: str, expected_message: str) -> bool:
    """
    获取指定占位符对应的错误提示信息，并验证是否符合预期

    :param page: Playwright的Page对象
    :param target_element: 目标元素
    :param xpath: 自定义XPath表达式，用于定位错误提示元素
    :param expected_message: 预期的错误提示信息
    :param timeout: 等待元素出现的超时时间（毫秒），默认为3000ms
    """
    if not xpath:
        raise ValueError("必须提供自定义XPath表达式")

    try:
        # 定位包含指定占位符文本的输入元素
        # target_input = page.get_by_role("textbox", name=placeholder_text)

        # 使用分步定位策略查找错误提示元素
        final_locator = locate_element_by_step_strategy(target_element, xpath)

        if final_locator:
            error_element = final_locator
        else:
            # 后备策略：使用相对定位
            logger.info(f"分步定位失败，使用后备策略: {xpath}")
            error_element = target_element.locator(f'xpath={xpath}')
        # 关键修改：添加元素存在性检查
        if error_element.count() == 0 :
            # 当预期消息为None时，表示我们期望没有错误提示，此时验证通过
            result = (expected_message is None)
            logger.info(f"定位失败，该元素没有任何错误提示， <返回值>: {result}")
            return result

        else :
            error_text = error_element.text_content().strip()
            # 验证错误提示信息
            if error_text == expected_message:
                logger.info(f"✅ 验证成功：错误提示信息正确，内容为 '{error_text}'")
                return True
            else:
                logger.error(f"错误提示信息不符，预期: '{expected_message}'，实际: '{error_text}'")
                return False

    except AssertionError as ae:
        logger.error(f"错误提示信息时出错: {ae}")
        raise


def wait_dialog_with_expected_message(page: Page, expected_message: str = "") -> Locator:
    """
    等待对话框出现并返回对话框的Locator对象，可选择验证对话框内容

    :param page: Playwright的Page对象
    :param expected_message: 可选，期望在对话框中出现的文本内容
    :return: 对话框的Locator对象
    :raises AssertionError: 当指定了expected_message但对话框内容不包含时抛出
    """
    try:
        # 等待并定位对话框元素
        dialog = page.wait_for_selector('div[role="dialog"]', timeout=5000)
        if not dialog:
            raise AssertionError("未找到对话框元素")

        # 如果指定了期望消息，则验证内容
        if expected_message:
            actual_message = dialog.text_content()
            logger.info(f"期望消息: {expected_message}")
            logger.info(f"实际消息: {actual_message}")

            if expected_message in actual_message:
                logger.info(f"✅ 验证通过: 对话框文本包含 '{expected_message}'")
            else:
                logger.error(f"❌ 验证失败: 对话框文本 '{actual_message}' 不包含 '{expected_message}'")
                raise AssertionError(f"对话框内容不包含期望消息: {expected_message}")

        return dialog

    except AssertionError as ae:
        logger.error(f"验证对话框时出错: {ae}")
        raise
    except TimeoutError:
        logger.error(f"等待对话框超时 (5000ms)")
        raise AssertionError("等待对话框超时")
    except Exception as e:
        logger.error(f"定位对话框时发生异常: {e}")
        raise

def close_dialog(page: Page) -> None:
    """
    关闭对话框

    :param page: Playwright的Page对象
    """
    try:
        # 定位关闭按钮
        close_button = page.get_by_role("button", name="Close")
        # 点击关闭按钮
        close_button.click()
        # 等待关闭按钮隐藏
        close_button.wait_for(state='hidden')
    except Exception as e:
        # 若关闭对话框过程中出现异常，记录错误日志
        logger.error(f"关闭对话框时出错: {e}")

def operation_for_dialog(page: Page, aria_label: str, operation: str) -> None:
    """
    对话框操作：点击确认、取消或关闭按钮

    :param page: Playwright 的 Page 对象
    :param aria_label: 对话框的 aria-label 属性值，用于精确定位
    :param operation: 操作类型，支持"confirm"（确认）、"cancel"（取消）、"close"（关闭）
    :raises ValueError: 当操作类型不支持时抛出
    :raises TimeoutError: 当对话框未在指定时间内出现时抛出
    """
    # 同时使用 role 和 aria-label 定位对话框，提高准确性
    selector = f'div[role="dialog"][aria-label="{aria_label}"]'
    target_dialog = page.wait_for_selector(selector, timeout=5000)

    if operation.lower() == "confirm":
        # 定位确认按钮（使用query_selector而非locator）
        confirm_btn = target_dialog.query_selector(
            "button:has-text('确认'), button:has-text('确定'), button[type='submit']")
        if confirm_btn:
            confirm_btn.click()
        else:
            raise ValueError("未找到确认按钮")

    elif operation.lower() == "cancel":
        # 定位取消按钮
        cancel_btn = target_dialog.query_selector("button:has-text('取消'), button[type='button']:not([type='submit'])")
        if cancel_btn:
            cancel_btn.click()
        else:
            raise ValueError("未找到取消按钮")

    elif operation.lower() == "close":
        # 定位关闭按钮
        close_btn = target_dialog.query_selector("button[aria-label='Close']")
        if close_btn:
            close_btn.click()
        else:
            raise ValueError("未找到关闭按钮")

    else:
        raise ValueError(f"不支持的操作类型: {operation}，请使用'confirm'、'cancel'或'close'")

def fill_textbox(page: Page, label: str, value: str) -> None:
    """
    填写文本框

    :param page: Playwright的Page对象
    :param label: 文本框的标签
    :param value: 要填写的值
    """
    try:
        # 定位文本框并填写值
        page.get_by_role("textbox", name=label).fill(value)
    except Exception as e:
        # 若填写文本框过程中出现异常，记录错误日志
        logger.error(f"填写文本框 {label} 时出错: {e}")

def select_option_by_text(page, tip_text, target_text):
    """
    在下拉菜单中选择包含指定文本的选项

    :param page: Playwright的Page对象
    :param tip_text: 下拉菜单的提示文本
    :param target_text: 要选择的目标文本
    :return: 若找到并选择目标选项返回True，否则返回False
    """
    try:
        # 定位到下拉菜单容器并点击
        page.get_by_role("textbox", name="请选择民宿").click()
        time.sleep(1)
        # 定位下拉菜单元素
        dropdown = page.locator(".el-scrollbar")
        # 等待下拉菜单可见
        dropdown.wait_for(state="visible")

        # 定位滚动内容区域和滚动条
        scroll_wrap = dropdown.locator(".el-select-dropdown__wrap")
        scrollbar = dropdown.locator(".el-scrollbar__thumb")

        # 计算滚动步长 (根据实际情况调整)
        scroll_step = 100
        max_scroll_attempts = 10
        scroll_attempt = 0

        while scroll_attempt < max_scroll_attempts:
            # 查找当前可见区域内的选项
            options = dropdown.locator("li.el-select-dropdown__item")
            count = options.count()

            for i in range(count):
                option = options.nth(i)
                text = option.text_content()
                if target_text in text:
                    # 若找到目标选项，点击并返回True
                    option.click()
                    logger.info(f"已选择: {text}")
                    return True

            # 如果未找到，滚动页面
            current_scroll = page.evaluate('(element) => element.scrollTop', scroll_wrap)
            page.evaluate('(element, step) => element.scrollBy(0, step)', scroll_wrap, scroll_step)

            # 等待页面滚动和内容加载
            page.wait_for_timeout(300)

            # 检查是否已滚动到底部
            new_scroll = page.evaluate('(element) => element.scrollTop', scroll_wrap)
            if new_scroll == current_scroll:
                logger.info("已滚动到底部")
                break

            scroll_attempt += 1

        logger.info(f"未找到文本为 '{target_text}' 的选项")
        return False
    except Exception as e:
        # 若选择选项过程中出现异常，记录错误日志并返回False
        logger.error(f"选择选项 {target_text} 时出错: {e}")
        return False

def select_region(page: Page, label: str, province: str, city: str, district: str) -> None:
    """
    选择行政区划

    :param page: Playwright的Page对象
    :param label: 行政区划选择框的标签
    :param province: 省份名称
    :param city: 城市名称
    :param district: 区县名称
    """
    try:
        # 点击行政区划选择框
        page.get_by_role("textbox", name=label).click()
        # 填写行政区划信息
        page.get_by_role("textbox", name=label).fill(f"{province}{city}{district}")
        # 点击第一个列表项
        page.get_by_role("listitem").first.click()
    except Exception as e:
        # 若选择行政区划过程中出现异常，记录错误日志
        logger.error(f"选择行政区划 {province}{city}{district} 时出错: {e}")

def select_radio_button(page: Page, label_text: str, target_option: str) -> None:
    """
    在指定标签下遍历单选按钮，根据文本内容匹配并选择目标选项

    :param page: Playwright 页面对象
    :param label_text: 父级标签文本（如"便器"）
    :param target_option: 目标选项文本（如"智能马桶"）
    :raises ValueError: 未找到匹配的选项
    """
    try:
        # 获取所有相关的单选按钮元素
        radio_buttons = get_label_corresponding_elements(page, label_text, 'following-sibling::div//label')

        # 遍历按钮并匹配文本内容
        for btn in radio_buttons:
            # 获取按钮文本（去除空白）
            btn_text = btn.text_content().strip()

            # 匹配目标选项（支持模糊匹配，如需精确匹配可改为 ==）
            if target_option in btn_text:
                # 点击匹配的按钮
                btn.click()
                logger.info(f"已选择选项：{btn_text}")
                return  # 匹配后立即返回

        # 未找到匹配项时抛出异常
        raise ValueError(f"未找到选项：{target_option}，可用选项为：{[btn.text_content().strip() for btn in radio_buttons]}")
    except Exception as e:
        # 若选择单选按钮过程中出现异常，记录错误日志并抛出异常
        logger.error(f"选择单选按钮 {target_option} 时出错: {e}")
        raise

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
        logger.info(f"开始检查单选按钮: {label_text} > {target_option}")

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
            error_msg = f"未找到选项：{target_option}，可用选项为：{available_options}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # 获取实际的 input 元素
        input_element = matched_btn.locator('input[type="radio"]')
        if not input_element.count():
            error_msg = f"无法在标签元素中找到对应的单选按钮输入框: {target_option}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        # 确认选中状态并记录结果
        is_checked = input_element.is_checked()
        status_icon = "✅" if is_checked else "❌"
        logger.info(f"{status_icon} [{target_option}]状态：{'已选中' if is_checked else '未选中'}")
        return is_checked

    except (ValueError, RuntimeError) as e:
        logger.error(f"检查单选按钮时出错: {str(e)}")
        raise  # 重新抛出特定异常，保持原有行为

    except Exception as e:
        logger.error(f"意外错误: {str(e)}")
        return False  # 非预期异常时返回False，保持原有行为

def set_selector_input_by_label_text(page: Page, label_text, value):
    """
    设置输入框的值

    Args:
        label_text (str): 标签文本
        value (str): 要设置的值
    """
    target_input = get_label_corresponding_element(page, label_text, 'following-sibling::div//input')
    increase_button = get_label_corresponding_element(page, label_text,
                                                      'following-sibling::div//*[contains(@class, "increase")]')
    click_increase_button(increase_button, target_input, value)

def set_selector_input_by_input_element(input_element, xpath, value):
    """
    设置输入框的值

    Args:
        label_text (str): 标签文本
        value (str): 要设置的值
    """

    increase_button = locate_element_by_step_strategy(input_element, xpath)
    click_increase_button(increase_button, input_element, value)

def get_error_elements_with_text(page: Page, text: str) -> list[Locator]:
    """
    查找所有包含 "error" 的 class 元素，并筛选出文本内容包含指定字段的元素

    :param page: Playwright 页面对象
    :param text: 需要在元素文本中查找的字段
    :return: 符合条件的元素定位器列表
    """
    try:
        # 定位所有包含 "error" 的 class 元素
        error_elements = page.locator('[class*="error"]')

        # 筛选出文本内容包含指定字段的元素
        matching_elements = []
        for i in range(error_elements.count()):
            element = error_elements.nth(i)
            if text in element.inner_text().strip():
                matching_elements.append(element)

        return matching_elements
    except Exception as e:
        # 若查找错误元素过程中出现异常，记录错误日志并返回空列表
        logger.error(f"查找包含文本 {text} 的错误元素时出错: {e}")
        return []

def click_increase_button(increase_button, target_input, expected_number):
    """
    点击增加按钮，直到目标输入框中的数字达到预期值

    :param increase_button: 增加按钮的Locator对象
    :param target_input: 目标输入框的Locator对象
    :param expected_number: 预期的数字
    """
    try:
        # 检查expected_number是否为None
        if expected_number is None:
            logger.info("请输入正确的数字")
            return

        # 尝试将预期值转换为整数
        try:
            expected_number = int(expected_number)
        except (ValueError, TypeError):
            logger.info("请输入正确的数字")
            return

        # 获取当前值（处理空字符串的情况）
        try:
            current_number = int(target_input.input_value())
        except ValueError:
            current_number = 0

        # 循环点击增加按钮，直到达到预期值
        while current_number < expected_number:
            increase_button.click()
            # 等待输入框值更新
            time.sleep(0.3)

            # 再次获取值并处理可能的空字符串
            try:
                current_number = int(target_input.input_value())
            except ValueError:
                current_number = 0
    except Exception as e:
        # 若点击增加按钮过程中出现异常，记录错误日志
        logger.error(f"点击增加按钮直到达到 {expected_number} 时出错: {e}")

def check_success_message(page: Page, expected_text, timeout=5000):
    """
    检查页面上是否显示成功消息。

    :param page: Playwright的Page对象
    :param expected_text: 期望的成功消息文本
    :param timeout: 等待元素出现的超时时间（毫秒），默认为5000ms
    :return: 如果找到匹配的成功消息则返回True，否则返回False
    """
    try:
        # 检查必要参数是否为空
        if not expected_text:
            raise ValueError("Expected text is required.")

        # 定位具有role="alert"的元素并检查其文本内容
        alert_element = page.get_by_role("alert")
        alert_element.wait_for(timeout=timeout)
        # 检查元素是否可见且包含期望的文本
        if alert_element.is_visible() and expected_text in alert_element.inner_text():
            return True
        else:
            return False
    except Exception as e:
        # 若检查成功消息过程中出现异常，记录错误日志并返回False
        logger.error(f"检查成功消息 {expected_text} 时出错: {e}")
        return False

def check_alert_text(page: Page, expected_text: str, timeout: int = 1000) -> tuple[bool, str]:
    """
    检查页面上的 alert 元素文本是否与预期文本匹配

    参数:
        page (Page): Playwright 页面对象
        expected_text (str): 期望的 alert 文本内容
        timeout (int, optional): 等待 alert 元素的超时时间(毫秒)，默认1000

    返回:
        tuple[bool, str]: 验证结果和实际文本内容
    """
    actual_text = ""
    try:
        # 等待 alert 元素出现
        alert_element = page.wait_for_selector('[role="alert"]', timeout=timeout)
        if not alert_element:
            logger.info("错误: 未找到 [role='alert'] 元素")
            return False, actual_text

        # 获取 alert 元素的文本内容
        actual_text = alert_element.inner_text()

        # 对比实际文本与预期文本
        if actual_text == expected_text:
            logger.info(f"✅ 验证通过: alert 文本 '{actual_text}' 与预期一致")
            return True, actual_text
        else:
            logger.info(f"❌ 验证失败: 实际文本 '{actual_text}' 与预期 '{expected_text}' 不匹配")
            return False, actual_text

    except TimeoutError:
        logger.info(f"错误: 等待 alert 元素超时 ({timeout}ms)")
        return False, actual_text
    except Exception as e:
        logger.info(f"错误: 获取 alert 文本时发生异常: {str(e)}")
        return False, actual_text

def check_dialog_text(page: Page, expect_message: str) -> tuple[Locator, str]:
    """
    等待对话框出现并验证标题，返回对话框定位器和实际文本内容

    参数:
        page (Page): Playwright 页面对象
        expect_message (str): 期望的对话框文本内容

    返回:
        tuple[Locator, str]: 对话框定位器和实际文本内容

    异常:
        AssertionError: 对话框内容不包含期望的消息
    """
    actual_message = ""
    try:
        # 等待对话框元素出现
        dialog = page.wait_for_selector('div[role="dialog"]', timeout=5000)
        if not dialog:
            logger.error("❌ 验证失败: 未找到对话框元素")
            raise AssertionError("未找到对话框元素")

        # 获取对话框的文本内容
        actual_message = dialog.text_content()
        logger.info(f"期望消息: {expect_message}")
        logger.info(f"实际消息: {actual_message}")

        # 验证消息内容
        if expect_message in actual_message:
            logger.info(f"✅ 验证通过: 对话框文本包含 '{expect_message}'")
            return dialog, actual_message
        else:
            logger.error(f"❌ 验证失败: 对话框文本 '{actual_message}' 不包含 '{expect_message}'")
            raise AssertionError(f"对话框内容不包含期望消息: {expect_message}")

    except TimeoutError:
        logger.error(f"❌ 验证失败: 等待对话框元素超时 (5000ms)")
        raise AssertionError("等待对话框超时")
    except AssertionError as ae:
        # 直接重新抛出断言错误
        raise
    except Exception as e:
        logger.error(f"❌ 验证失败: 获取对话框文本时发生异常: {str(e)}")
        raise AssertionError(f"获取对话框文本异常: {str(e)}")

def wait_alert_text_disappear(page: Page, expected_text: str, timeout: int = 5000) -> bool:
    """
    等待页面上的 alert 元素包含预期文本后消失

    参数:
        page (Page): Playwright 页面对象
        expected_text (str): 期望消失的 alert 文本内容
        timeout (int, optional): 等待超时时间(毫秒)，默认5000

    返回:
        bool: 如果 alert 文本成功消失返回 True，否则返回 False
    """
    try:
        # 等待 alert 元素出现并包含预期文本
        alert_selector = '[role="alert"]'
        page.wait_for_selector(
            f'{alert_selector}:has-text("{expected_text}")',
            timeout=timeout
        )

        # 等待 alert 元素消失或文本变化
        page.wait_for_function(
            f'''() => {{
                const alert = document.querySelector('{alert_selector}');
                return !alert || alert.innerText !== "{expected_text}";
            }}''',
            timeout=timeout
        )
        time.sleep(1)
        logger.info(f"✅ 验证通过: 包含文本 '{expected_text}' 的 alert 元素已消失")
        return True

    except TimeoutError:
        logger.info(f"❌ 验证失败: 等待 alert 消失超时 ({timeout}ms)")
        return False

    except Exception as e:
        logger.info(f"错误: 等待 alert 消失时发生异常: {str(e)}")
        return False

def operation_alert_error(page, expected_text):
    is_matched, actual_text = check_alert_text(page, expected_text)
    return is_matched

def select_option_by_label_text(page: Page, label_text, option_text):
    """
    选择下拉列表中的选项

    Args:
        label_text (str): 标签文本
        option_text (str): 选项文本
    """
    page.get_by_role("textbox", name=label_text).click()
    page.get_by_role("listitem").filter(has_text=regex_pattern(option_text)).click()

def select_option_by_input_element(page: Page, input_element, option_text=None):
    """
    选择下拉列表中的选项

    Args:
        label_element: 标签元素对象
        option_text (str, optional): 选项文本。默认为None，表示不选择具体选项。
    """
    if option_text is not None and option_text.strip():
        input_element.click()
        page.get_by_role("listitem").filter(has_text=regex_pattern(option_text)).click()
    else:
        print("option_text为空、None或仅包含空白字符，未执行选择操作")

def select_radio(page: Page, label_text, option_text):
    """
    选择单选按钮

    Args:
        label_text (str): 标签文本
        option_text (str): 选项文本
    """
    select_radio_button(page, label_text, option_text)

def simulate_blur(element):
    """
    模拟元素失去焦点的动作

    Args:
        element: 需要模拟失去焦点的元素
    """
    try:
        element.blur()
    except Exception as e:
        # 记录错误但不中断测试
        print(f"警告: 模拟元素失去焦点失败: {e}")

def validate_upload_results(label_types):
    """
    验证文件上传结果

    Args:
        label_types (dict): 房间类型及其上传数据

    Returns:
        dict: 验证结果，包含每个房间类型的上传状态

    Raises:
        AssertionError: 如果有文件未成功上传
    """
    upload_results = {}
    for label_type, data in label_types.items():
        expected = data["expected"]
        actual = data["uploaded"]
        is_complete = expected == actual

        upload_results[label_type] = {
            "expected": expected,
            "actual": actual,
            "is_complete": is_complete
        }

        status = "全部上传成功" if is_complete else "部分上传失败"
        logger.info(f"{label_type.capitalize()} 上传状态: {status} ({actual}/{expected})")

    all_complete = all(result["is_complete"] for result in upload_results.values())
    if not all_complete:
        incomplete_types = [t for t, r in upload_results.items() if not r["is_complete"]]
        raise AssertionError(f"上传未完成: {', '.join(incomplete_types)} 有文件未成功上传")

    return upload_results

def validate_count_results(label_types):
    """
    验证文件输入框数量结果

    Args:
        label_types (dict): 房间类型及其验证数据

    Returns:
        dict: 验证结果，包含每个房间类型的验证状态

    Raises:
        AssertionError: 如果有房间类型的输入框数量不符合预期
    """
    validation_results = {}
    for label_type, data in label_types.items():
        expected = data["param"]
        actual = data["count"]

        # 处理expected为空字符串的情况
        if expected == "":
            expected = 0
        elif isinstance(expected, str) and expected.isdigit():
            expected = int(expected)

        is_valid = expected == actual

        validation_results[label_type] = {
            "expected": expected,
            "actual": actual,
            "is_valid": is_valid
        }

        status = "通过" if is_valid else "失败"
        logger.info(f"{label_type.capitalize()} 验证 {status}: 预期={expected}, 实际={actual}")

    all_valid = all(result["is_valid"] for result in validation_results.values())
    if not all_valid:
        failed_types = [t for t, r in validation_results.items() if not r["is_valid"]]
        raise AssertionError(f"验证失败: {', '.join(failed_types)} 的文件输入框数量不符合预期")

    return validation_results

def calculate_expected_inputs(labels):
    """
    计算预期的文件输入框数量

    Args:
        labels (list): 标签元素列表

    Returns:
        int: 预期的文件输入框数量
    """
    expected = 0
    for label in labels:
        try:
            file_input = label.query_selector('xpath=following-sibling::div').query_selector(
                'xpath=//input[@type="file"]')
            if file_input:
                expected += 1
        except Exception:
            continue
    return expected

def check_page_title(page: Page, expected_title: str, timeout=5000) -> bool:
    """
    检查页面标题是否符合预期。

    :param page: Playwright的Page对象
    :param expected_title: 期望的页面标题文本
    :param timeout: 等待标题加载的超时时间（毫秒），默认为5000ms
    :return: 如果页面标题与预期一致则返回True，否则返回False
    """
    try:
        # 检查必要参数是否为空
        if not expected_title:
            raise ValueError("Expected title is required.")

        # 等待页面标题加载完成（通过轮询检查标题变化）
        start_time = time.time()
        while (time.time() - start_time) * 1000 < timeout:
            current_title = page.title()
            if expected_title == current_title:
                logger.info(f"✅ 页面标题与预期一致，当前标题: {page.title()}")
                return True
            # 短暂休眠后重试
            time.sleep(0.1)

        # 超时后仍未匹配标题
        logger.warning(f"❌ 页面标题与预期不符，当前标题: {page.title()}, 预期标题: {expected_title}")
        return False

    except Exception as e:
        # 若检查页面标题过程中出现异常，记录错误日志并返回False
        logger.error(f" ❌ 检查页面标题 {expected_title} 时出错: {e}")
        return False

def checkTipDialog(
    page: Page,
    expected_text: str,
    confirm_text: Union[str, List[str]],
    cancel_text: Union[str, List[str]],
    operation: str  # 新增参数："confirm" 返回确认按钮，"cancel" 返回取消按钮
) -> Union[Page.locator, None]:
    """
    检查可见的确认对话框，并根据operation参数返回对应的按钮

    Args:
        page: Playwright 的 Page 对象
        expected_text: 对话框的预期提示文本
        confirm_text: 确认按钮的可能文本（单个字符串或列表）
        cancel_text: 取消按钮的可能文本（单个字符串或列表）
        operation: 操作类型，"confirm" 表示返回确认按钮，"cancel" 表示返回取消按钮

    Returns:
        匹配的按钮定位器；验证失败或参数错误则返回 None
    """
    try:
        # 验证operation参数有效性
        if operation not in ["confirm", "cancel"]:
            logger.error(f"❌ 无效的operation参数：{operation}，必须是'confirm'或'cancel'")
            return None
        confirm_button = None
        cancel_button = None
        # 工具函数：处理多文本匹配按钮
        def get_button_by_multi_text(locator_parent, text_list: Union[str, List[str]]):
            text_list = [text_list] if isinstance(text_list, str) else text_list
            for text in text_list:
                button = locator_parent.locator(f"button:has-text('{text}')")
                if button.is_visible() and button.count() > 0:
                    logger.info(f"✅ 找到匹配按钮：{text}")
                    return button
            logger.error(f"❌ 未找到匹配按钮，预期文本：{text_list}")
            return None

        # 等待并获取所有对话框
        page.wait_for_selector('div[role="dialog"]', state="attached", timeout=8000)
        all_dialogs = page.locator('div[role="dialog"]')
        dialog_count = all_dialogs.count()
        # logger.info(f"✅ 共找到 {dialog_count} 个对话框元素")

        if dialog_count == 0:
            logger.error("❌ 未找到任何对话框元素")
            return None

        # 筛选可见的对话框
        visible_dialog = None
        for i in range(dialog_count):
            dialog = all_dialogs.nth(i)
            if dialog.is_visible():
                visible_dialog = dialog
                # logger.info(f"✅ 找到可见对话框（索引 #{i+1}）")
                break

        if not visible_dialog:
            logger.error("❌ 所有对话框均处于隐藏状态")
            return None

        # 验证对话框提示文本
        message_locator = visible_dialog.locator(".el-message-box__message")
        message_locator.wait_for(state="visible", timeout=3000)
        message_text = message_locator.text_content().strip()

        if message_text != expected_text:
            logger.error(f"❌ 提示文本不匹配：预期「{expected_text}」，实际「{message_text}」")
            return None

        # 查找确认和取消按钮
        if confirm_text:
            confirm_button = get_button_by_multi_text(visible_dialog, confirm_text)
        if confirm_text:
            cancel_button = get_button_by_multi_text(visible_dialog, cancel_text)

        # 验证按钮状态
        if confirm_button  and not confirm_button.is_enabled():
            logger.error("❌ 确认按钮处于禁用状态")
            return None
        if cancel_button and not cancel_button.is_enabled():
            logger.error("❌ 取消按钮处于禁用状态")
            return None

        # 根据operation参数返回对应的按钮
        if operation == "confirm":
            if confirm_button:
                logger.info("✅ 成功返回确认按钮")
                return confirm_button
            else:
                logger.error("❌ 确认按钮不存在，无法返回")
                return None
        else:  # operation == "cancel"
            if cancel_button:
                logger.info("✅ 成功返回取消按钮")
                return cancel_button
            else:
                logger.error("❌ 取消按钮不存在，无法返回")
                return None

    except Exception as e:
        logger.error(f"❌ 检查对话框时发生异常：{str(e)}", exc_info=True)
        return None

def get_table_cell_or_button(
        page,
        row: int,  # 行索引（从0开始）
        col: int,  # 列索引（从0开始）
        button_text: str = None,  # 可选：按钮文本（如"详情""修改"，不传则返回td单元格）
        timeout: int = 5000
) -> Locator:
    """
    定位表格目标单元格（td），或直接定位单元格内指定文本的操作按钮
    适配Element UI表格按钮样式：el-button--text、el-button--mini、span包含按钮文本

    参数说明：
    --------
    page:
        Playwright页面对象（self.page）
    row: int
        目标行索引（非负整数，0=第一行）
    col: int
        目标列索引（非负整数，0=第一列）
    button_text: str | None
        可选参数：需查找的按钮文本（如"详情""修改""禁用""注销"），
        不传则返回目标td单元格；传值则返回该按钮的Locator
    timeout: int
        元素查找超时时间（默认5秒）

    返回值：
    ------
    Locator: 若传button_text则返回按钮Locator，否则返回td单元格Locator

    异常：
    ----
    ValueError: 索引非法、未找到行/列/按钮
    TimeoutError: 元素加载超时
    """
    # ---------------------- 1. 基础定位：tbody → 目标行 → 目标td ----------------------
    # 按指定逻辑获取tbody和所有行
    tbody = page.locator('//tbody')
    tr_elements = tbody.locator('tr')

    # 等待tbody加载可见
    try:
        tbody.wait_for(state="visible", timeout=timeout)
    except TimeoutError:
        raise TimeoutError(f"表格tbody加载超时（{timeout}ms）")

    # 校验行索引有效性
    row_count = tr_elements.count()
    if row < 0 or row >= row_count:
        raise ValueError(
            f"行索引{row}超出范围！表格共{row_count}行（有效索引：0~{row_count - 1}）"
        )

    # 定位目标行
    target_row = tr_elements.nth(row)
    if not target_row.is_visible(timeout=timeout):
        raise ValueError(f"第{row}行（索引）不可见或未加载")
    logger.info(f"✅ 定位目标行：索引{row}（共{row_count}行）")

    # 定位目标td（适配Element UI表格单元格类名，确保精准匹配）
    # 注：nth-child从1开始，需将列索引（0开始）+1
    target_td = target_row.locator(f"td:nth-child({col + 1})")
    if not target_td.is_visible(timeout=timeout):
        raise ValueError(f"第{row}行第{col}列（索引）的td单元格不存在或不可见")
    logger.info(f"✅ 定位目标单元格（td）：行{row} → 列{col}")

    # ---------------------- 2. 若需查找按钮，在td内定位目标按钮 ----------------------
    if button_text is not None:
        # 校验按钮文本合法性
        if not isinstance(button_text, str) or len(button_text.strip()) == 0:
            raise ValueError("按钮文本不能为空字符串")

        # 定位td内指定文本的按钮（精准匹配Element UI按钮样式）
        # 匹配规则：el-button--text类（文本按钮）+ el-button--mini（迷你尺寸）+ span包含目标文本
        target_button = target_td.locator(
            f"button:has(span:has-text('{button_text}'))"
        )

        # 校验按钮是否存在且可见
        if target_button.count() == 0:
            raise ValueError(
                f"目标td内未找到文本为「{button_text}」的按钮！"
                f"当前td包含按钮：{target_td.locator('button span').all_text_contents()}"
            )
        if not target_button.is_visible(timeout=timeout):
            raise ValueError(f"文本为「{button_text}」的按钮存在但不可见")

        logger.info(f"✅ 定位目标按钮：td（行{row}列{col}）→ 「{button_text}」按钮")
        return target_button

    # ---------------------- 3. 若无需查找按钮，直接返回td单元格 ----------------------
    return target_td

def check_label_corresponding_input_value(
        page: Page,
        label_text: str,  # 英文标签文本（如"Building"）
        expected_value: str,  # 预期值（如louyu_info["modified_louyu_name"]的英文/中文值）
        timeout: int = 5000
) -> bool:
    """
    Verify if the value of the input box corresponding to the target label matches the expected value.
    （校验目标标签对应的输入框值是否与预期值匹配）

    :param label_text: English label text (e.g., "Building", "Room Number")
    :param expected_value: Expected value (e.g., modified building name from test data)
    :param timeout: Maximum waiting time for element loading (default: 5000ms)
    :return: True if matched, False otherwise
    """
    try:

        time.sleep(2)
        input_locator = get_label_corresponding_input(page, label_text)
        # Check if input is found
        if not input_locator or input_locator.count() == 0:
            raise ValueError(f"Input box corresponding to label '{label_text}' not found")

        # 2. Wait for input to load and get its current value
        input_locator.wait_for(state="visible", timeout=timeout)
        actual_value = input_locator.input_value()

        # 4. 去除两端空格（现在操作的是字符串，而非Locator）
        actual_value_stripped = actual_value.strip()
        expected_value_stripped = expected_value.strip()

        # 3. Log comparison result (English logs for international teams)
        logger.info(f"   Expected Value: {expected_value_stripped}")
        logger.info(f"   Actual Value: {actual_value_stripped}")

        # 4. Exact match (recommended for strict verification)
        if actual_value_stripped == expected_value_stripped:
            logger.info(f"✅ Value matched successfully!")
            return True
        else:
            logger.error(f"❌ Value mismatch!")
            return False

    except TimeoutError:
        logger.error(f"❌ Timeout: Input box for label '{label_text}' did not load within {timeout}ms")
        raise
    except Exception as e:
       logger.error(f"❌ Failed to verify input value for label '{label_text}': {str(e)}")
       raise

def query_target_name_tr(page, target_part:str, target_part_name: str):
    """
    根据楼宇名称查询，优化按钮定位逻辑，确保正确识别"自定义查询"按钮
    采用严格的文字完全匹配策略，允许tbody为None的情况
    """
    try:
        # 1. 优化按钮定位逻辑：使用更可靠的策略查找"自定义查询"按钮
        time.sleep(1)
        custom_query_btn = page.get_by_role("button", name="自定义查询", exact=True)

        # 检查按钮是否存在
        btn_exists = custom_query_btn.count() > 0
        used_locator = ""

        if btn_exists:
            custom_query_btn.click()
            used_locator = "get_by_role(button, name='自定义查询')"
        else:
            # 检查"收起查询"按钮
            collapse_query_btn = page.get_by_role("button", name="收起查询", exact=True)
            collapse_query_btn_alt = page.locator(f"button:has-text('收起查询')")
            collapse_exists = collapse_query_btn.count() > 0 or collapse_query_btn_alt.count() > 0

            if not collapse_exists:
                # 输出页面中所有按钮文本用于调试
                all_buttons = page.locator("button")
                btn_count = all_buttons.count()
                btn_texts = []
                for i in range(btn_count):
                    text = all_buttons.nth(i).text_content().strip()
                    if text:
                        btn_texts.append(text)
                logger.debug(f"页面中所有按钮文本：{', '.join(btn_texts)}")

        time.sleep(1)
        # 清除输入框并填入查询关键词
        target_query_input = page.locator(f'//input[@placeholder="请输入{target_part}名称"]')
        target_query_button = page.get_by_role("button", name="搜索")
        target_query_input.fill("")
        target_query_input.fill(target_part_name)
        target_query_button.click()
        logger.info(f" 已执行{target_part}查询，查询关键词：{target_part_name}（完全匹配模式）")
        time.sleep(1)
        # 等待搜索结果加载完成
        logger.info("等待搜索结果加载...")
        page.wait_for_load_state("networkidle", timeout=30000)
        empty_block = page.locator('//div[@class="el-table__empty-block"]')
        # 检查无数据提示块是否存在且可见（避免隐藏元素干扰判断）
        if empty_block.count() > 0 and empty_block.is_visible():
            logger.info(f" 未找到任何 tr 元素（查询关键词：{target_part_name}，页面显示'暂无数据'）")
            return None

        # 3. 若无无数据提示，再执行原有tbody及tr元素的查询逻辑
        tbody = page.locator('//tbody')

        # 检查tbody是否存在
        if tbody.count() == 0:
            logger.info(f" 未找到tbody元素（查询关键词：{target_part_name}）")
            return None

        # 等待tbody可见（确保DOM已加载完成）
        try:
            tbody.wait_for(state="visible", timeout=5000)  # 5秒超时避免无限等待
        except Exception as e:
            logger.warning(f" tbody存在但不可见：{str(e)}")
            return None

        tr_elements = tbody.locator('tr')
        tr_count = tr_elements.count()

        if tr_count == 0:
            logger.info(f" tbody 下未找到任何 tr 元素（查询关键词：{target_part_name}）")
            return None
        logger.info(f" tbody 下共找到 {tr_count} 个 tr 元素，开始精确匹配{target_part}名称")

        # 4. 精确匹配目标名称（完全匹配td:nth-child(2)下的div内容）
        matched_tr = None
        target_name = target_part_name.strip()  # 去除关键词前后空格，避免空格干扰匹配

        for i in range(tr_count):
            current_tr = tr_elements.nth(i)
            # 定位目标列（第2列的div元素，与原逻辑保持一致）
            target_div = current_tr.locator('td:nth-child(2) > div')
            try:
                target_div.wait_for(state="visible", timeout=2000)  # 等待当前行内容可见
            except Exception:
                logger.warning(f" 第 {i + 1} 个tr的目标div不可见，跳过检查")
                continue

            div_content = target_div.text_content().strip()  # 去除内容前后空格

            # 严格完全匹配（区分大小写、无额外字符）
            if div_content == target_name:
                matched_tr = current_tr
                logger.info(f" 找到完全匹配的 tr 元素（第 {i + 1} 个，内容：{div_content}）")
                break

        if matched_tr:
            time.sleep(2)  # 预留加载时间（可根据页面响应速度调整）
            return matched_tr
        else:
            logger.info(f" 未找到与 {target_name} 完全匹配的元素")
            # 收集所有结果用于调试（定位匹配失败原因）
            all_td2_contents = []
            for i in range(tr_count):
                content = tr_elements.nth(i).locator('td:nth-child(2) > div').text_content().strip()
                all_td2_contents.append(f"第 {i + 1} 个：{content}")
            logger.debug(f"所有 tr 的 td[2] 内容：{', '.join(all_td2_contents)}")
            return None

    except Exception as e:
        # 捕获全局异常，记录详细堆栈信息（便于排查复杂问题）
        logger.error(f" 查询{target_part} {target_part_name} 时发生异常：{str(e)}", exc_info=True)
        return None

def query_target_name_index(page, target_part:str, target_part_name: str):
    """
    根据楼宇名称查询，优化按钮定位逻辑，确保正确识别"自定义查询"按钮
    采用严格的文字完全匹配策略，允许tbody为None的情况
    查找成功时返回匹配行的位置（从1开始计数），失败返回None
    """
    try:
        # 1. 优化按钮定位逻辑：使用更可靠的策略查找"自定义查询"按钮
        time.sleep(1)
        custom_query_btn = page.get_by_role("button", name="自定义查询", exact=True)

        # 检查按钮是否存在
        btn_exists = custom_query_btn.count() > 0

        if btn_exists:
            custom_query_btn.click()
            used_locator = "get_by_role(button, name='自定义查询')"
        else:
            # 检查"收起查询"按钮
            collapse_query_btn = page.get_by_role("button", name="收起查询", exact=True)
            collapse_query_btn_alt = page.locator(f"button:has-text('收起查询')")
            collapse_exists = collapse_query_btn.count() > 0 or collapse_query_btn_alt.count() > 0

            if not collapse_exists:
                # 输出页面中所有按钮文本用于调试
                all_buttons = page.locator("button")
                btn_count = all_buttons.count()
                btn_texts = []
                for i in range(btn_count):
                    text = all_buttons.nth(i).text_content().strip()
                    if text:
                        btn_texts.append(text)
                logger.debug(f"页面中所有按钮文本：{', '.join(btn_texts)}")

        time.sleep(1)
        # 清除输入框并填入查询关键词
        target_query_input = page.locator(f'//input[@placeholder="请输入{target_part}名称"]')
        target_query_button = page.get_by_role("button", name="搜索")
        target_query_input.fill("")
        target_query_input.fill(target_part_name)
        target_query_button.click()
        logger.info(f" 已执行{target_part}查询，查询关键词：{target_part_name}（完全匹配模式）")
        time.sleep(1)
        # 等待搜索结果加载完成
        logger.info("等待搜索结果加载...")
        page.wait_for_load_state("networkidle", timeout=30000)
        empty_block = page.locator('//div[@class="el-table__empty-block"]')
        # 检查无数据提示块是否存在且可见（避免隐藏元素干扰判断）
        if empty_block.count() > 0 and empty_block.is_visible():
            logger.info(f" 未找到任何 tr 元素（查询关键词：{target_part_name}，页面显示'暂无数据'）")
            return None

        # 3. 若无无数据提示，再执行原有tbody及tr元素的查询逻辑
        tbody = page.locator('//tbody')

        # 检查tbody是否存在
        if tbody.count() == 0:
            logger.info(f" 未找到tbody元素（查询关键词：{target_part_name}）")
            return None

        # 等待tbody可见（确保DOM已加载完成）
        try:
            tbody.wait_for(state="visible", timeout=5000)  # 5秒超时避免无限等待
        except Exception as e:
            logger.warning(f" tbody存在但不可见：{str(e)}")
            return None

        tr_elements = tbody.locator('tr')
        tr_count = tr_elements.count()

        if tr_count == 0:
            logger.info(f" tbody 下未找到任何 tr 元素（查询关键词：{target_part_name}）")
            return None
        logger.info(f" tbody 下共找到 {tr_count} 个 tr 元素，开始精确匹配{target_part}名称")

        # 4. 精确匹配目标名称（完全匹配td:nth-child(2)下的div内容）
        matched_row = None  # 记录匹配到的行号（从1开始）
        target_name = target_part_name.strip()  # 去除关键词前后空格，避免空格干扰匹配

        for i in range(tr_count):
            current_tr = tr_elements.nth(i)
            # 定位目标列（第2列的div元素，与原逻辑保持一致）
            target_div = current_tr.locator('td:nth-child(2) > div')
            try:
                target_div.wait_for(state="visible", timeout=2000)  # 等待当前行内容可见
            except Exception:
                logger.warning(f" 第 {i + 1} 个tr的目标div不可见，跳过检查")
                continue

            div_content = target_div.text_content().strip()  # 去除内容前后空格

            # 严格完全匹配（区分大小写、无额外字符）
            if div_content == target_name:
                matched_row = i + 1  # 行号从1开始计数
                logger.info(f" 找到完全匹配的 tr 元素（第 {matched_row} 个，内容：{div_content}）")
                break

        if matched_row:
            time.sleep(2)  # 预留加载时间（可根据页面响应速度调整）
            return matched_row  # 返回匹配到的行号
        else:
            logger.info(f" 未找到与 {target_name} 完全匹配的元素")
            # 收集所有结果用于调试（定位匹配失败原因）
            all_td2_contents = []
            for i in range(tr_count):
                content = tr_elements.nth(i).locator('td:nth-child(2) > div').text_content().strip()
                all_td2_contents.append(f"第 {i + 1} 个：{content}")
            logger.debug(f"所有 tr 的 td[2] 内容：{', '.join(all_td2_contents)}")
            return None

    except Exception as e:
        # 捕获全局异常，记录详细堆栈信息（便于排查复杂问题）
        logger.error(f" 查询{target_part} {target_part_name} 时发生异常：{str(e)}", exc_info=True)
        return None

def batch_target_operation(page, operation_index: int, operation: str,
                           confirm_text: Union[str, List[str]], cancel_text: Union[str, List[str]], sure_operation):
    """
    对表格中的所有行执行批量操作，无需搜索功能
    遍历表格所有行并点击指定位置的操作按钮
    只有当成功操作数量等于表格总行数时，才判定为整体成功

    参数:
        page: 页面对象
        operation_index: 操作按钮所在的列索引（整型，从1开始计数）
        operation: 要执行的操作名称（按钮上的文本）

    返回:
        操作结果字典，包含：
        - overall_success: 布尔值，表示整体操作是否成功（成功数量等于总行数）
        - success_count: 成功操作的行数
        - fail_count: 失败操作的行数
        - total_rows: 表格总行数
        - fail_details: 失败详情列表
    """

    result = {
        "overall_success": False,
        "success_count": 0,
        "fail_count": 0,
        "total_rows": 0,  # 新增：记录表格总行数
        "fail_details": []
    }

    try:
        # 等待页面加载完成
        logger.info("等待页面加载完成...")
        page.wait_for_load_state("networkidle", timeout=30000)

        # 检查无数据提示
        empty_block = page.locator('//div[@class="el-table__empty-block"]')
        if empty_block.count() > 0 and empty_block.is_visible():
            logger.info("表格显示'暂无数据'，无法执行批量操作")
            return result

        # 定位表格主体
        tbody = page.locator('//tbody')

        # 检查tbody是否存在
        if tbody.count() == 0:
            logger.info("未找到表格tbody元素，无法执行批量操作")
            return result

        # 等待tbody可见
        try:
            tbody.wait_for(state="visible", timeout=5000)
        except Exception as e:
            logger.warning(f"tbody存在但不可见：{str(e)}")
            return result

        # 获取所有行元素
        tr_elements = tbody.locator('tr')
        tr_count = tr_elements.count()
        result["total_rows"] = tr_count  # 记录总行数

        if tr_count == 0:
            logger.info("表格中没有找到任何行元素，无需执行批量操作")
            # 没有行需要操作时视为成功
            result["overall_success"] = True
            return result

        logger.info(f"开始对表格中的 {tr_count} 行执行批量操作：{operation}")

        # 遍历所有行并执行操作
        for i in range(tr_count):
            page.wait_for_load_state()
            # 每次循环都重新获取行元素，避免DOM变化导致定位失效
            current_tr = tbody.locator(f'tr:nth-child({i + 1})')
            row_index = i + 1  # 行号从1开始

            try:
                # 获取当前行标识（第二列内容）用于日志记录和提示信息
                row_identifier_locator = current_tr.locator('td:nth-child(2) > div.cell')
                row_identifier = row_identifier_locator.text_content().strip() or f"第{row_index}行"
                # 获取房间名称（第二列内容）
                room_name = row_identifier  # 从表格结构看，第二列就是房间名称

                logger.info(f"处理行: {row_identifier}")

                # 定位操作按钮
                operation_button = current_tr.locator(
                    f"td:nth-child({operation_index}) button", has_text=operation
                )

                # 点击操作按钮
                operation_button.click()
                logger.info(f"成功点击 {row_identifier} 的'{operation}'按钮")

                # 处理注销操作的确认提示
                if operation == "注销":
                    # 根据表格结构定制注销提示信息
                    expected_text = f'是否确认注销房间名称为"{room_name}"的数据项？'
                    logger.info(f"验证注销提示: {expected_text}")
                else:
                    expected_text = confirm_text  # 使用默认确认文本

                # 检查提示对话框并执行确认操作
                checkTipDialog(page, expected_text, confirm_text, cancel_text, sure_operation).click()

                # 操作后等待，确保页面稳定
                time.sleep(3)

                # 记录成功
                result["success_count"] += 1

            except Exception as e:
                # 记录失败信息
                fail_msg = f"{row_identifier} 的'{operation}'操作失败: {str(e)}"
                logger.error(fail_msg)
                logger.debug(f"行HTML: {current_tr.inner_html()}")

                result["fail_count"] += 1
                result["fail_details"].append(fail_msg)

                # 失败后继续处理下一行
                continue

        # 判定整体成功：成功数量等于总行数
        result["overall_success"] = (result["success_count"] == result["total_rows"])

        logger.info(
            f"批量操作完成 - 成功: {result['success_count']}, 失败: {result['fail_count']}, "
            f"总行数: {result['total_rows']}, 整体成功: {result['overall_success']}"
        )
        return result

    except Exception as e:
        logger.error(f"执行批量操作时发生全局异常：{str(e)}", exc_info=True)
        # 全局异常时整体操作视为失败
        result["overall_success"] = False
        return result


def check_table_column(page, target_column: int, target_value: str):
    """
    遍历表格的指定列，检查是否存在目标值
    采用严格的文字完全匹配策略，找到匹配项后立即返回，不再继续遍历
    允许tbody为None的情况

    参数:
        page: 页面对象
        target_column: 目标列索引（从1开始）
        target_value: 要查找的目标值

    返回:
        找到的匹配行元素，如果未找到则返回None
    """
    try:
        # 等待页面加载完成
        logger.info("等待页面加载完成...")
        page.wait_for_load_state("networkidle", timeout=30000)

        # 检查无数据提示
        empty_block = page.locator('//div[@class="el-table__empty-block"]')
        if empty_block.count() > 0 and empty_block.is_visible():
            logger.info(f"表格显示'暂无数据'，无法查找目标值：{target_value}")
            return None

        # 定位表格主体
        tbody = page.locator('//tbody')

        # 检查tbody是否存在
        if tbody.count() == 0:
            logger.info("未找到表格tbody元素")
            return None

        # 等待tbody可见
        try:
            tbody.wait_for(state="visible", timeout=5000)
        except Exception as e:
            logger.warning(f"tbody存在但不可见：{str(e)}")
            return None

        # 获取所有行元素
        tr_elements = tbody.locator('tr')
        tr_count = tr_elements.count()

        if tr_count == 0:
            logger.info("表格中没有找到任何行元素")
            return None

        logger.info(f"表格中共有 {tr_count} 行数据，开始检查第 {target_column} 列是否存在目标值：{target_value}")

        # 遍历行，检查目标列
        matched_tr = None
        target_value_clean = target_value.strip()

        for i in range(tr_count):
            current_tr = tr_elements.nth(i)
            # 定位目标列的div元素
            target_div = current_tr.locator(f'td:nth-child({target_column}) > div')

            try:
                target_div.wait_for(state="visible", timeout=2000)
            except Exception:
                logger.warning(f"第 {i + 1} 行的目标列不可见，跳过检查")
                continue

            # 获取单元格内容并清理
            cell_content = target_div.text_content().strip()

            # 严格完全匹配，找到后立即返回
            if cell_content == target_value_clean:
                matched_tr = current_tr
                logger.info(f"找到完全匹配的行（第 {i + 1} 行，内容：{cell_content}）")
                # 找到匹配项后立即跳出循环，不再继续检查后续行
                break

        if not matched_tr:
            logger.info(f"未找到与 {target_value_clean} 完全匹配的内容")
            # 收集所有结果用于调试
            all_contents = []
            for i in range(tr_count):
                content = tr_elements.nth(i).locator(f'td:nth-child({target_column}) > div').text_content().strip()
                all_contents.append(f"第 {i + 1} 行：{content}")
            logger.debug(f"所有行的第 {target_column} 列内容：{', '.join(all_contents)}")

        return matched_tr

    except Exception as e:
        logger.error(f"检查表格列时发生异常：{str(e)}", exc_info=True)
        return None

def is_query_reset_successful(
        page: Page,
        search_types: List[str],
        reset_button_text: str = "重置"
) -> bool:
    """
    验证搜索重置功能是否成功（所有指定输入框是否为空）

    :param page: Playwright页面对象
    :param search_types: 要验证的搜索方式集合
    :param reset_button_text: 重置按钮文本
    :return: 布尔值：True表示所有输入框重置后为空，False表示存在未清空的输入框
    """
    try:
        # 点击重置按钮
        # reset_button = page.get_by_role("button", name=reset_button_text, exact=True)
        reset_button = page.locator('button:has(span:text("重置"))')
        reset_button.wait_for(state="visible", timeout=5000)
        reset_button.click()
        logger.info(f"点击「{reset_button_text}」按钮")

        # 等待重置完成
        page.wait_for_timeout(500)

        # 检查所有输入框
        for search_type in search_types:
            input_locator = get_label_corresponding_input(page, search_type)
            input_locator.wait_for(state="visible", timeout=5000)

            # 获取并检查输入值
            actual_value = input_locator.input_value().strip()
            if actual_value != "":
                logger.error(f"「{search_type}」重置后值不为空: {actual_value}")
                return False  # 只要有一个不为空就返回False

        # 所有输入框都为空
        logger.info("所有搜索条件均已成功重置为空")
        return True

    except Exception as e:
        logger.error(f"重置验证失败: {str(e)}")
        return False


from playwright.sync_api import Page, TimeoutError
import logging


def wait_for_loading_disappear(page: Page, timeout: int = 20000) -> bool:
    """
    修复版：同步等待上传加载遮罩消失（适配Element UI全屏遮罩）
    核心：只判断“加载中遮罩”是否隐藏，删除矛盾的visible验证

    Args:
        page: Playwright同步页面对象
        timeout: 加载中遮罩的最大等待时间（毫秒），默认20秒（适配图片上传耗时）

    Returns:
        bool: 遮罩消失返回True，超时/异常返回False
    """
    # 1. 精确定位“加载中”的全屏遮罩（完全匹配你提供的DOM特征）
    loading_mask = page.locator(
        '.el-loading-mask.is-fullscreen'  # 全屏遮罩类
        '[style*="background-color: rgba(0, 0, 0, 0.7)"]'  # 背景色
        '[style*="z-index: 2001"]'  # 层级
        ':has(.el-loading-spinner:has-text("正在上传图片，请稍候..."))'  # 包含上传文本
    )

    try:
        # 2. 先检测“加载中遮罩”是否出现（最多等3秒，避免错过短暂加载态）
        mask_appeared = False
        try:
            loading_mask.wait_for(state="visible", timeout=3000)
            mask_appeared = True
            logging.info("✅ 检测到上传加载遮罩，等待其消失...")
        except TimeoutError:
            # 未出现加载遮罩：直接检查是否有“display:none的遮罩”（确认已消失）
            hidden_mask_count = page.locator('.el-loading-mask[style*="display: none"]').count()
            if hidden_mask_count > 0:
                logging.info("✅ 加载遮罩已处于隐藏状态（display: none）")
                return True
            logging.info("✅ 未检测到加载遮罩，上传可能已完成")
            return True

        # 3. 若加载遮罩已出现：等待其变为“隐藏状态”（核心判断）
        if mask_appeared:
            # 等待“加载中遮罩”消失（hidden状态：包含display:none、visibility:hidden等）
            loading_mask.wait_for(state="hidden", timeout=timeout)
            logging.info("✅ 上传加载遮罩已完全消失")

            # （可选）额外验证：确认页面中没有“加载中”的遮罩残留
            remaining_loading_mask = loading_mask.count()
            if remaining_loading_mask == 0:
                return True
            else:
                logging.warning(f"⚠️ 仍存在{remaining_loading_mask}个加载遮罩残留，但已隐藏，继续执行")
                return True

    except TimeoutError:
        # 加载遮罩超时未消失：截图留存证据

        logging.error(f"❌ 等待加载遮罩消失超时（{timeout}ms）")
        return False
    except Exception as e:
        logging.error(f"❌ 处理加载遮罩时发生异常：{str(e)}", exc_info=True)
        return False
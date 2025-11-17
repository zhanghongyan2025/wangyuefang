
from datetime import datetime  # 正确的导入方式
import pytest
import allure
import logging
from playwright.sync_api import sync_playwright
import os
import re
import time
# 原始代码无此导入，新增一行
import allure

from tests.pages.fd.add_new_minsu import AddNewMinsuPage
from tests.pages.fd.filing_room_page import FilingRoomPage
from tests.pages.fd.ft_manage_page import FTManagePage
from tests.pages.fd.home_page import HomePage
from tests.pages.fd.login_page import LoginPage
from tests.pages.fd.louyu_management import louYuManagementPage
from tests.pages.fd.minsu_management_page import MinsuManagementPage
from tests.pages.fd.room_management_page import RoomManagementPage
from tests.pages.ga.ga_filing_management_page import GAFilingManagementPage
from tests.pages.ga.ga_fw_manage_page import GAFWManagementPage
from tests.pages.ga.ga_home_page import GAHomePage

# 确保截图目录存在
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def sanitize_filename(name):
    """
    清洗文件名，移除或替换所有可能导致路径问题的特殊字符
    """
    # 替换Windows系统不允许的文件名特殊字符
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', name)
    # 替换空格和Unicode字符
    sanitized = re.sub(r'\s+', '_', sanitized)
    # 限制文件名长度，避免路径过长
    max_length = 120
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """钩子函数：捕获测试结果并在失败时截图"""
    outcome = yield
    report = outcome.get_result()

    # 只处理测试用例失败的情况，且测试函数需要page参数
    if report.when == "call" and report.failed and "page" in item.fixturenames:
        # 获取page对象
        page = item.funcargs["page"]

        # 生成唯一的截图文件名（包含时间戳和测试用例名）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清洗测试用例名称，移除特殊字符
        test_name = sanitize_filename(item.nodeid.replace("::", "_").replace("/", "_"))
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"failed_{test_name}_{timestamp}.png")

        try:
            # 保存截图
            page.screenshot(path=screenshot_path)
            print(f"\n测试失败，已保存截图至：{screenshot_path}")
        except Exception as e:
            print(f"\n保存截图失败：{str(e)}")

        # 2. 新增：将截图附加到Allure报告
        try:
            # 截取全屏（full_page=True），返回二进制字节流（无需生成临时文件）
            screenshot_bytes = page.screenshot(full_page=True)
            # 调用allure.attach()将二进制流附加到报告
            allure.attach(
                body=screenshot_bytes,  # 截图二进制数据
                name=f"Failed_Screenshot_{test_name}_{timestamp}",  # 报告中显示的附件名称（含用例名+时间戳，避免重复）
                attachment_type=allure.attachment_type.PNG  # 指定附件类型为PNG，确保报告能正确渲染图片
            )
        except Exception as e:
            print(f"\n附加截图到Allure报告失败：{str(e)}")

@pytest.fixture(autouse=True)
def configure_logging():
    # 配置基本日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 获取日志记录器
    logger = logging.getLogger('conf.logging_config')  # 与你的日志名称匹配
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # 可以添加更多浏览器启动参数
        browser = p.chromium.launch(
            headless=False,
            args=[
                  "--start-maximized",
                  "--window-size=1920,1080",
                  "--disable-dev-shm-usage" # 解决 WSL/Xvfb 无法捕获 dialog 问题
                 ]  # 最大化窗口
        )
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page(no_viewport=True)  # 使用实际窗口大小
    yield page
    page.close()

@pytest.fixture(scope="session")
def fd_base_url():
    return "http://192.168.40.61:3333"

@pytest.fixture(scope="session")
def ga_base_url():
    return "http://192.168.40.61:1111"

@pytest.fixture(scope="session")
def fd_suffix_home_url():
    return "/fangdonghome/home"

@pytest.fixture(scope="session")
def ga_suffix_home_url():
    return "/gonganhome/home"

@pytest.fixture(scope="session")
def fd_test_user():
    return {
        "username": "fenghuang_123",
        "password": "Aa123123!"
    }

@pytest.fixture(scope="session")
def ga_test_user():
    return {
        "username": "fuzhou_xian",
        "password": "Aa123123!"
    }

@pytest.fixture(scope="function")
def fd_login_setup(page, fd_base_url, fd_test_user):
    """房东端登录页面页面前置操作"""
    # 登录操作
    login_page = LoginPage(page)
    login_page.navigate(fd_base_url)
    login_page.fill_credentials(fd_test_user["username"], fd_test_user["password"])
    login_page.click_login_button()

    # 验证登录是否成功
    time.sleep(2)
    assert page.title() == "网约房智慧安全监管平台"
    return LoginPage(page)

@pytest.fixture(scope="function")  # 修改为function作用域解决冲突
def louyu_management_setup(page, fd_login_setup):
    """
    楼宇页面测试的前置操作Fixture。

    参数:
    page: 页面对象，用于操作浏览器页面。
    fd_base_url: 测试的基础URL。
    fd_test_user: 包含用户名和密码的测试用户信息。

    返回:
    LouYuManagementPage 对象，用于楼宇相关操作。
    """
    home_page = HomePage(page)
    home_page.navigate_to_house_manage_page()
    ft_manage_page = FTManagePage(page)
    ft_manage_page.navigate_to_other_manage_page("楼宇管理")
    ft_manage_page.page.wait_for_load_state("load")
    return louYuManagementPage(page)


@pytest.fixture(scope="function")
def minsu_management_setup(page, fd_login_setup):
    """
    民宿管理测试的前置操作Fixture，依赖登录Fixture完成登录，再导航到民宿管理页面。

    参数:
    page: 页面对象，用于操作浏览器页面。
    fd_login_setup: 房东端登录Fixture，确保先完成登录操作。

    返回:
    MinsuManagementPage 对象，用于后续的民宿管理页面操作。
    """
    # 已通过fd_login_setup完成登录，直接进行页面导航
    home_page = HomePage(page)
    home_page.navigate_to_house_manage_page()

    ft_manage_page = FTManagePage(page)
    ft_manage_page.navigate_to_other_manage_page("民宿管理")

    return MinsuManagementPage(page)

@pytest.fixture(scope="function")
def add_new_minsu_setup(page, minsu_management_setup):
    """
    添加民宿测试的前置操作Fixture，依赖民宿管理页面Fixture，导航到添加民宿页面。

    参数:
    page: 页面对象，用于操作浏览器页面。
    minsu_management_setup: 民宿管理页面Fixture，确保已导航到民宿管理页面。

    返回:
    AddNewMinsuPage 对象，用于后续的添加民宿页面操作。
    """
    # 已通过minsu_management_setup完成登录和导航到民宿管理页面
    minsu_management_page = minsu_management_setup
    minsu_management_page.go_to_add_minsu_page()
    page.wait_for_load_state("load")

    return AddNewMinsuPage(page)

@pytest.fixture(scope="function")
def room_management_setup(page, fd_login_setup):
    """
    房间管理页面测试的前置操作Fixture，依赖登录Fixture完成登录，再导航到房间管理页面。

    参数:
    page: 页面对象，用于操作浏览器页面。
    fd_login_setup: 登录Fixture，确保先完成登录操作。

    返回:
    RoomManagementPage 对象，用于后续的房间管理页面操作。
    """
    # 已通过fd_login_setup完成登录，直接进行页面导航
    home_page = HomePage(page)
    home_page.navigate_to_house_manage_page()

    ft_manage_page = FTManagePage(page)
    ft_manage_page.navigate_to_other_manage_page("房间管理")

    return RoomManagementPage(page)

@pytest.fixture(scope="function")
def filing_room_page_setup(page, room_management_setup):
    """
    房间注册测试的前置操作Fixture，依赖房间管理页面Fixture，导航到房间注册页面。

    参数:
    page: 页面对象，用于操作浏览器页面。
    room_management_setup: 房间管理页面Fixture，确保已导航到房间管理页面。

    返回:
    FilingRoomPage 对象，用于后续的房间注册页面操作。
    """
    # 已通过room_management_setup完成登录和导航到房间管理页面
    room_management_page = room_management_setup
    room_management_page.go_to_filling_room_page()

    # 返回房间注册页对象
    return FilingRoomPage(page)

@pytest.fixture(scope="function")
def ga_login_setup(page, ga_base_url, ga_test_user):
    """公安端登录页面页面前置操作"""
    # 登录操作
    login_page = LoginPage(page)
    login_page.navigate(ga_base_url)
    login_page.fill_credentials(ga_test_user["username"], ga_test_user["password"])
    login_page.click_login_button()

    # 验证登录是否成功
    time.sleep(2)
    assert page.title() == "网约房智慧安全监管平台"
    return login_page


@pytest.fixture(scope="function")
def ga_filing_management_setup(page, ga_login_setup):
    """
    公安端民宿备案管理测试的前置操作Fixture，依赖公安端登录Fixture完成登录，再导航到备案管理页面。

    参数:
    page: 页面对象，用于操作浏览器页面。
    ga_login_setup: 公安端登录Fixture，确保先完成登录操作。

    返回:
    GAFilingManagementPage 对象，用于后续的备案管理页面操作。
    """
    # 已通过ga_login_setup完成登录，直接进行页面导航
    ga_home_page = GAHomePage(page)
    ga_home_page.navigate_to_other_page("房屋管理")

    ga_fw_management_page = GAFWManagementPage(page)
    ga_fw_management_page.navigate_to_other_management_page("民宿备案管理")

    return GAFilingManagementPage(page)

def pytest_configure(config):
    # 注册更多自定义标记
    config.addinivalue_line("markers", "register: 标记注册流程相关的测试用例")
    config.addinivalue_line("markers", "room: 标记房间管理相关的测试用例")  # 解决之前的UnknownMarkWarning

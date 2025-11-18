#!/bin/bash
set -e

# --- 1. 检查并安装系统级依赖 ---
echo "INFO: Checking for system dependencies..."
if ! dpkg -l | grep -q python3.12-venv; then
    echo "WARN: python3.12-venv is not installed. Installing now..."
    sudo apt update
    sudo apt install -y python3.12-venv
else
    echo "INFO: python3.12-venv is already installed."
fi

# --- 2. 准备 Python 虚拟环境 ---
echo "INFO: Creating Python virtual environment in the current directory..."
# 在当前目录（即 $WORKSPACE）下创建 venv
python3.12 -m venv venv

# --- 3. 先定义变量，再激活虚拟环境（核心修复点） ---
# 定义虚拟环境 Python 绝对路径（避免相对路径歧义）
VENV_PYTHON="$(pwd)/venv/bin/python"
# 激活虚拟环境，同时校验激活结果
echo "INFO: Activating virtual environment..."
if ! source ./venv/bin/activate; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "INFO: Using Python interpreter at: $VENV_PYTHON"

echo "INFO: Upgrading pip and installing project dependencies..."
# 使用相对路径调用 pip
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r requirements.txt

# --- 4. 检查并安装 Playwright 浏览器 ---
echo "INFO: Checking if Playwright browsers are installed..."
PLAYWRIGHT_BROWSERS_PATH="$HOME/.cache/ms-playwright"
if [ -d "$PLAYWRIGHT_BROWSERS_PATH" ] && [ "$(ls -A "$PLAYWRIGHT_BROWSERS_PATH")" ]; then
    echo "INFO: Playwright browsers are already installed."
else
    echo "INFO: Playwright browsers not found. Installing now..."
    # 使用相对路径调用 playwright
    "$VENV_PYTHON" -m playwright install
fi

# --- 5. 运行准备脚本 ---
echo "INFO: Running delete_users.py to prepare the test environment..."
# 使用相对路径执行 Python 脚本
echo y | "$VENV_PYTHON" tests/prepare/delete_users.py

# --- 6. 运行指定的 Pytest 测试 ---
echo "INFO: Running Pytest for test_register.py..."
# 使用相对路径调用 pytest
#xvfb-run "$VENV_PYTHON" -m pytest -v tests/test_suites/fd/test_register.py
xvfb-run "$VENV_PYTHON" -m pytest -v tests/test_suites/fd/test_register.py --alluredir=allure-results
echo "INFO: All tasks completed successfully."
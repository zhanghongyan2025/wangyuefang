import logging

import paramiko
import re
import time
from datetime import datetime, date

from faker import Faker

from conf.logging_config import logger

import random

# 确保 fake 在全局作用域中定义
fake = Faker("zh_CN")

def validate_id_card(id_card):
    """验证身份证号码是否合法"""
    if len(id_card) != 18:
        return False

    # 前17位权重系数
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    # 校验码映射
    check_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    # 计算前17位加权和
    total = sum(int(id_card[i]) * weights[i] for i in range(17))
    mod = total % 11
    expected_check = check_code[mod]

    return id_card[-1].upper() == expected_check

def connect_ssh(hostname, username, password, port=22):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username, password=password)
        return ssh
    except Exception as e:
        print(f"连接错误: {e}")
        return None

def extract_code_from_line(line, target_phone):
    """
    从单条日志中提取验证码的独立函数

    Args:
        line: 日志行字符串
        target_phone: 目标手机号

    Returns:
        提取到的验证码字符串，未匹配则返回None
    """
    # 保持与主函数一致的正则匹配逻辑
    pattern = fr'^.*?(\d{{2}}:\d{{2}}:\d{{2}}(\.\d+)?).*?【{target_phone}】短信验证码【(\d+)】请求结果【\d+】'
    match = re.search(pattern, line)
    return match.group(3) if match else None


def check_recent_logs(config, log_path, target_phone, start_datetime, timeout):
    """
    超时后检查最近日志的函数：
    1. 读取包含目标手机号的最新日志
    2. 检查是否是start_datetime前2秒内的记录
    3. 提取并返回验证码

    Args:
        config: SSH连接配置
        log_path: 日志文件路径
        target_phone: 目标手机号
        start_datetime: 监控开始时间
        timeout: 超时时间（秒）

    Returns:
        提取到的验证码或None
    """
    logger = logging.getLogger(__name__)
    ssh = None
    try:
        ssh = connect_ssh(**config)
        # 查找包含目标手机号的最新日志（取最后10行避免过多数据）
        command = f'grep {target_phone} {log_path} | tail -n 10'
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8', errors='replace')
        error = stderr.read().decode('utf-8', errors='replace')

        if error:
            logger.warning(f"执行命令错误: {error}")
            return None

        # 按时间倒序检查日志行
        for line in reversed(output.split('\n')):
            line = line.strip()
            if not line:
                continue

            # 提取时间戳和验证码
            time_pattern = fr'^.*?(\d{{2}}:\d{{2}}:\d{{2}}(\.\d+)?).*?【{target_phone}】'
            time_match = re.search(time_pattern, line)
            if not time_match:
                continue

            code = extract_code_from_line(line, target_phone)
            if not code:
                continue

            # 解析日志时间
            timestamp_str = time_match.group(1)
            current_date = date.today().isoformat()
            try:
                full_timestamp = f"{current_date} {timestamp_str}"
                log_datetime = datetime.strptime(full_timestamp, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                log_datetime = datetime.strptime(full_timestamp, '%Y-%m-%d %H:%M:%S')

            # 检查是否在有效时间范围内（开始时间前2秒内）
            time_diff = (start_datetime - log_datetime).total_seconds()
            if 0 <= time_diff <= 2:
                logger.info(f"在超时后找到有效验证码: {code} (时间: {log_datetime})")
                return code

        logger.warning("超时后未找到符合时间条件的验证码")
        return None

    finally:
        if ssh:
            ssh.close()

def extract_verification_code_live(hostname, username, password, port, log_path, target_phone, timeout=70,
                                   show_logs=True, sample_rate=1.0):
    """
    使用改进的日志处理逻辑提取验证码，防止被刷屏问题
    超时后会调用check_recent_logs函数进行二次检查

    Args:
        hostname: SSH服务器地址
        username: SSH用户名
        password: SSH密码
        port: SSH端口
        log_path: 日志文件路径
        target_phone: 目标手机号
        timeout: 超时时间（秒）
        show_logs: 是否显示日志
        sample_rate: 日志采样率(0.0-1.0)，用于减少显示的日志量

    Returns:
        提取到的验证码或None
    """
    config = {
        "hostname": hostname,
        "username": username,
        "password": password,
        "port": port
    }

    logger = logging.getLogger(__name__)
    # 记录监控开始时间（用于超时后检查）
    start_datetime = datetime.now()

    ssh = connect_ssh(**config)
    try:
        command = f'tail -f {log_path}'
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.setblocking(0)

        # 优化正则表达式，增加行首锚点提高匹配效率
        pattern = fr'^.*?(\d{{2}}:\d{{2}}:\d{{2}}(\.\d+)?).*?【{target_phone}】短信验证码【(\d+)】请求结果【\d+】'
        compiled_pattern = re.compile(pattern)

        logger.info(f"开始监控文件 {log_path}，等待{target_phone}的验证码...")

        buffer = b''
        last_matched_time = None
        log_counter = 0

        while (datetime.now() - start_datetime).total_seconds() < timeout:
            if stdout.channel.recv_ready():
                new_data = stdout.channel.recv(4096)  # 增大缓冲区
                buffer += new_data

                try:
                    decoded = buffer.decode('utf-8', errors='replace')
                    lines = decoded.split('\n')

                    # 处理未完成的行
                    if not decoded.endswith('\n') and lines:
                        buffer = lines[-1].encode('utf-8')
                        lines = lines[:-1]
                    else:
                        buffer = b''

                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue

                        log_counter += 1
                        # 日志采样，避免刷屏
                        should_log = (sample_rate >= 1.0 or log_counter % int(1 / sample_rate) == 0)
                        if show_logs and should_log:
                            logger.info(f"日志行: {line[:200]}...")  # 限制显示长度

                        # 使用预编译的正则表达式
                        match = compiled_pattern.search(line)

                        if match:
                            timestamp_str = match.group(1)
                            code = match.group(3)

                            # 解析时间戳
                            current_date = date.today().isoformat()
                            try:
                                full_timestamp = f"{current_date} {timestamp_str}"
                                timestamp = datetime.strptime(full_timestamp, '%Y-%m-%d %H:%M:%S.%f')
                            except ValueError:
                                timestamp = datetime.strptime(full_timestamp, '%Y-%m-%d %H:%M:%S')

                            # 防重复匹配：检查是否是新的验证码
                            if last_matched_time and (timestamp - last_matched_time).total_seconds() < 1:
                                continue

                            last_matched_time = timestamp

                            logger.info(f"找到验证码: {code} (时间: {timestamp})")

                            # 优雅停止监控
                            stdin.write('\x03')  # 发送Ctrl+C
                            stdin.flush()
                            time.sleep(0.5)  # 等待命令终止

                            return code

                except UnicodeDecodeError as e:
                    logger.warning(f"解码错误: {e}")
                    buffer = b''  # 清空损坏的缓冲区

            time.sleep(0.05)  # 减少CPU占用

        logger.warning(f"超时({timeout}秒)未找到匹配的验证码，尝试检查最近日志...")
        stdin.write('\x03')  # 发送Ctrl+C
        stdin.flush()
        time.sleep(0.5)  # 等待命令终止

        # 超时后调用二次检查函数
        return check_recent_logs(config, log_path, target_phone, start_datetime, timeout)

    finally:
        if ssh:
            ssh.close()

def generate_uscc():
    """生成18位社会统一信用代码（模拟）"""
    # 注：真实的USCC有校验规则，这里仅生成格式相似的随机码
    # 前17位为数字和字母（不包含I、O、Z、S、V）
    chars = '0123456789ABCDEFGHJKLMNPQRTUWXY'
    uscc_prefix = ''.join(fake.random_choices(chars, length=17))
    # 第18位为校验码（简化处理，随机生成）
    check_code = fake.random_choices(chars, length=1)[0]
    return uscc_prefix + check_code

def generate_random_phone_number():
    """
    生成符合中国大陆规则的随机电话号码

    规则：
    - 共11位数字
    - 第一位为1
    - 第二位为3/4/5/7/8（主流运营商常见号段）
    - 后9位为随机数字
    """
    # 号段前缀列表（覆盖移动、联通、电信主要号段）
    prefixes = [
        # 13x号段
        "130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
        # 14x号段
        "145", "147", "149",
        # 15x号段
        "150", "151", "152", "153", "155", "156", "157", "158", "159",
        # 17x号段
        "170", "171", "173", "175", "176", "177", "178",
        # 18x号段
        "180", "181", "182", "183", "184", "185", "186", "187", "188", "189"
    ]

    # 随机选择一个前缀
    prefix = random.choice(prefixes)

    # 生成后8位随机数字（前缀3位 + 后8位 = 11位）
    suffix = ''.join(str(random.randint(0, 9)) for _ in range(8))

    return f"{prefix}{suffix}"

def regex_pattern(text: str):
    # 构造精确匹配的正则表达式
    regex_pattern = r'^' + re.escape(text) + r'$'
    return re.compile(regex_pattern)
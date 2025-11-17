import paramiko
import re
from datetime import datetime

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

def get_latest_verify_code(
        remote_host: str,
        username: str,
        password: str,
        remote_file_path: str,
        phone_number: str,
        port: int = 22,
) -> str | None:
    """
    从远程服务器获取指定电话号码的最新短信验证码

    参数:
        remote_host (str): 远程服务器主机名或IP地址
        username (str): SSH用户名
        password (str): SSH密码
        remote_file_path (str): 远程服务器上的日志文件路径
        phone_number (str): 需要查询的电话号码
        port (int): SSH端口，默认为22

    返回:
        str | None: 找到的最新验证码，如果未找到则返回None
    """
    try:
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # 连接到远程服务器
        ssh.connect(remote_host, port=port, username=username, password=password)

        # 创建SFTP客户端
        sftp = ssh.open_sftp()

        # 读取远程文件内容
        with sftp.file(remote_file_path, 'r') as remote_file:
            content = remote_file.read().decode('utf-8')

        # 关闭连接
        sftp.close()
        ssh.close()

        # 定义正则表达式模式，用于匹配时间戳、电话号码和验证码
        pattern = re.compile(
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*?【(\d+)】.*?短信验证码【(\d+)】'
        )

        # 存储匹配的验证码及其时间戳
        matches = []

        # 查找所有匹配项
        for match in pattern.finditer(content):
            timestamp_str, phone, code = match.groups()

            # 只处理目标电话号码的记录
            if phone == phone_number:
                # 将时间戳字符串转换为datetime对象
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                matches.append((timestamp, code))

        # 如果找到匹配项，按时间戳排序并返回最新的验证码
        if matches:
            # 按时间戳降序排序
            matches.sort(key=lambda x: x[0], reverse=True)
            return matches[0][1]  # 返回最新的验证码
        else:
            return None  # 未找到匹配的记录

    except Exception as e:
        print(f"发生错误: {e}")
        return None

#
# # 使用示例
# if __name__ == "__main__":
#     # 配置远程服务器信息
#     remote_config = {
#         "remote_host": "your_server_ip",  # 替换为实际服务器IP
#         "username": "your_username",  # 替换为实际用户名
#         "password": "your_password",  # 替换为实际密码
#         "remote_file_path": "/path/to/sms/logs.txt",  # 替换为实际文件路径
#     }
#
#     # 需要查询的电话号码
#     target_phone = "13501284047"
#
#     # 获取验证码
#     code = get_latest_sms_code(**remote_config, phone_number=target_phone)
#
#     if code:
#         print(f"电话号码 {target_phone} 的最新验证码是: {code}")
#     else:
#         print(f"未找到电话号码 {target_phone} 的验证码记录")
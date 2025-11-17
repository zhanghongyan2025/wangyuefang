import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, List
from conf.logging_config import logger

def read_json_file(file_path: str) -> Dict[str, Any]:
    """读取JSON文件并返回内容"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_file(file_path: str, data: Dict[str, Any]) -> None:
    """将数据写入JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_file_lines(file_path: str) -> List[str]:
    """读取文件所有行"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def write_file_lines(file_path: str, lines: List[str]) -> None:
    """将行列表写入文件

    Args:
        file_path: 文件路径
        lines: 要写入的行列表
    """
    # 确保目录存在
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        # 使用join方法将列表转换为字符串，并添加换行符
        f.write('\n'.join(lines))

    # 可选：添加日志输出
    print(f"已成功写入 {len(lines)} 行到文件: {file_path}")

def create_data_directory(output_dir: str) -> Path:
    """创建数据目录（如果不存在）"""
    data_dir = Path(output_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

def append_info_to_csv(file_path: str, info: list[dict]) -> None:
    """将信息追加到CSV文件"""
    import csv
    file_exists = Path(file_path).exists()
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = info[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists or os.path.getsize(file_path) == 0:
            writer.writeheader()
        writer.writerows(info)

def read_credentials(file_path: str) -> list[dict]:
    """从CSV文件读取用户名和密码"""
    if not Path(file_path).exists():
        raise FileNotFoundError(f"Credential file not found: {file_path}")

    credentials = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        # 验证CSV文件包含必要的列
        if not all(field in reader.fieldnames for field in ['用户名', '密码']):
            raise ValueError("CSV file must contain '用户名' and '密码' columns")

        for row in reader:
            credentials.append({
                'username': row['用户名'],
                'password': row['密码']
            })

    if not credentials:
        raise ValueError("No credentials found in the CSV file")

    return credentials

def get_image_files( directory):
    """
    获取目录下的所有图片文件

    Args:
        directory (str): 目录路径

    Returns:
        list: 图片文件列表
    """
    if os.path.exists(directory) and os.path.isdir(directory):
        files = [f for f in os.listdir(directory)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        return sorted(files)
    else:
        logger.warning(f"警告：目录 {directory} 不存在或不是目录")
        return []



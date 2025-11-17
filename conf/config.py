
import os

# 获取项目根目录路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 如果是放在 conf 目录下，获取项目根目录可能需要调整，比如：
# PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 定义数据文件路径常量
LARGE_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'large.png')
EXACTLY_10M_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', '10M.jpg')
HTML_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.html')
JPEG_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.jpeg')
JPEG_FIRE_SAFETY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.jpeg')
JPEG_PUBLIC_SECURITY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.jpeg')
JPG_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.jpg')
PDF_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.pdf')
PHP_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.php')
PNG_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.png')
PY_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.py')
SVG_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.svg')
TXT_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.txt')
ZIP_PROPERTY_CERTIFICATE = os.path.join(PROJECT_ROOT, 'tests', 'data', 'evidence_files', 'lease.zip')

# 证件文件
LARGE_ID_CARD =  os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'large.png')
EXACTLY_10M_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', '10M.jpg')
HTML_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.html')
JPEG_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.jpeg')
JPG_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.jpg')
EXE_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.exe')
BMP_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.bmp')
PDF_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.exe')
PHP_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.pdf')
PNG_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.png')
PY_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.exe')
SVG_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.py')
TXT_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.txt')
ZIP_ID_CARD = os.path.join(PROJECT_ROOT, 'tests', 'data', 'id_card_files', 'lease.zip')

# 房间区域文件
BEDROOM_FILES = os.path.join(PROJECT_ROOT, 'tests', 'data', 'bedroom_files')
LIVING_ROOM_FILES = os.path.join(PROJECT_ROOT, 'tests', 'data', 'livingroom_files')
KITCHEN_FILES = os.path.join(PROJECT_ROOT, 'tests', 'data', 'kitchen_files')
BATHROOM_FILES = os.path.join(PROJECT_ROOT, 'tests', 'data', 'bathroom_files')


# 准备数据
BEDROOM = os.path.join(PROJECT_ROOT, 'tests', 'prepare', 'bedroom_files')
ROOM_JSON_FILES = os.path.join(PROJECT_ROOT, 'tests', 'prepare', 'room.json')
MINSU_JSON_FILES = os.path.join(PROJECT_ROOT, 'tests', 'prepare', 'minsu.json')
BATHROOM = os.path.join(PROJECT_ROOT, 'tests', 'prepare', 'bathroom_files')

# 房间公共参数
COMMON_ROOM_PARAMS = {
    "property_type": "自有",
    # "ms_name": "手持机民宿",
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

# 民宿公共参数
COMMON_minsu_PARAMS = {
    "province": "福建省",
    "city": "福州市",
    "district": "鼓楼区",
    "street": "鼓东街道",
    "detail_address": "测试详细地址123",
    "front_image": JPG_ID_CARD,
    "back_image": JPG_ID_CARD
}


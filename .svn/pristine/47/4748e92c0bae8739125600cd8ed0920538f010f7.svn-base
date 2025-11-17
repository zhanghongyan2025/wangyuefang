import os
from PIL import Image, ImageDraw


def create_large_image(target_size_mb, output_file):
    """生成指定大小（MB）的图片文件"""
    size_bytes = target_size_mb * 1024 * 1024

    # 先创建基础图片
    width, height = 1024, 1024
    img = Image.new('RGB', (width, height), color='black')
    draw = ImageDraw.Draw(img)

    # 确保文件首次保存成功
    try:
        img.save(output_file, quality=100)
    except Exception as e:
        print(f"首次保存失败: {e}")
        return

    # 循环增加文件大小
    quality = 99  # 从次高质量开始，避免首次保存就是最大尺寸
    while os.path.getsize(output_file) < size_bytes:
        try:
            # 尝试降低质量
            img.save(output_file, quality=quality)
            quality -= 1

            # 质量降到最低后调整分辨率
            if quality < 1:
                width += 100
                height += 100
                img = img.resize((width, height), Image.LANCZOS)
                quality = 100  # 重置质量

            # 防止无限循环（设置最大尝试次数）
            if width > 10000 or height > 10000:
                print("达到最大分辨率，无法继续增大文件")
                break

        except Exception as e:
            print(f"保存失败: {e}")
            break


# 生成30MB的图片（指定完整路径避免路径问题）
output_path = os.path.join(os.getcwd(), "large.jpg")
create_large_image(30, output_path)
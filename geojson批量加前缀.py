import os

def add_prefix_to_files(
    target_dir,
    file_suffix=".geojson",
    prefix="GIS_"
):
    """
    给指定目录下、指定后缀的文件统一加前缀

    :param target_dir: 目标目录
    :param file_suffix: 文件后缀，如 '.geojson'
    :param prefix: 要添加的前缀，如 'GIS_'
    """

    if not os.path.isdir(target_dir):
        print(f"❌ 目录不存在: {target_dir}")
        return

    file_suffix = file_suffix.lower()

    for filename in os.listdir(target_dir):
        old_path = os.path.join(target_dir, filename)

        # 只处理文件
        if not os.path.isfile(old_path):
            continue

        # 后缀判断（不区分大小写）
        if not filename.lower().endswith(file_suffix):
            continue

        # 已有前缀则跳过
        if filename.startswith(prefix):
            print(f"跳过（已有前缀）: {filename}")
            continue

        new_filename = prefix + filename
        new_path = os.path.join(target_dir, new_filename)

        os.rename(old_path, new_path)
        print(f"✔ 重命名: {filename} -> {new_filename}")


if __name__ == "__main__":
    # ====== 配置区 ======
    target_directory = r"D:\Ren\2026\01meijiang\01martinmj\geojsonmj"   # 改成你的目录
    suffix = ".geojson"
    prefix = "GIS_"

    add_prefix_to_files(
        target_dir=target_directory,
        file_suffix=suffix,
        prefix=prefix
    )

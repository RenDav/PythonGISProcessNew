import os
import sys

# ===== 用户配置 =====
WIN_GEOJSON_DIR = r"D:\qgis_export_geojson4326"
WIN_OUTPUT_MB = r"D:\qgis_export_geojson4326\base.mbtiles"

# ===== Windows 路径 → WSL 路径 =====
def win_to_wsl(path):
    path = os.path.abspath(path)
    drive, rest = os.path.splitdrive(path)
    drive_letter = drive.replace(":", "").lower()
    rest = rest.replace("\\", "/")
    return f"/mnt/{drive_letter}{rest}"

WSL_GEOJSON_DIR = win_to_wsl(WIN_GEOJSON_DIR)
WSL_OUTPUT_MB = win_to_wsl(WIN_OUTPUT_MB)

# ===== tippecanoe 固定参数 =====
BASE_ARGS = [
    "tippecanoe",
    f"-o {WSL_OUTPUT_MB}",
    "-zg",
    "--drop-densest-as-needed",
    "--extend-zooms-if-still-dropping",
    "--force",
]

layers = []

# ===== 扫描目录 =====
for fname in sorted(os.listdir(WIN_GEOJSON_DIR)):
    if not fname.lower().endswith(".geojson"):
        continue

    layer_name = os.path.splitext(fname)[0]
    win_full_path = os.path.join(WIN_GEOJSON_DIR, fname)
    wsl_full_path = win_to_wsl(win_full_path)

    layers.append(f"--layer {layer_name}:{wsl_full_path}")

if not layers:
    print("❌ 目录中未找到 geojson 文件")
    sys.exit(1)

# ===== 生成一行命令 =====
cmd = " ".join(BASE_ARGS + layers)

print(cmd)

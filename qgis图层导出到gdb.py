from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter
)
from qgis.utils import iface
import os
import re

# =========================
# 1. 设置 GDB 输出路径
#    （必须以 .gdb 结尾）
# =========================
gdb_path = r"D:/qgis_export/output.gdb"   # ← 改成你自己的路径

# =========================
# 2. 目标坐标系（如不想重投影，可设为 None）
# =========================
target_crs = QgsCoordinateReferenceSystem("EPSG:4326")

# =========================
# 3. 创建 GDB（若不存在）
# =========================
if not os.path.exists(gdb_path):
    os.makedirs(gdb_path)

# =========================
# 4. 获取当前“可见”的图层
# =========================
root = QgsProject.instance().layerTreeRoot()
visible_layer_ids = [
    node.layerId()
    for node in root.findLayers()
    if node.isVisible()
]

layers = [
    QgsProject.instance().mapLayer(lid)
    for lid in visible_layer_ids
]

print("开始导出可见图层到 GDB……")

# =========================
# 5. 逐图层导出
# =========================
for layer in layers:

    if not isinstance(layer, QgsVectorLayer):
        continue

    if not layer.isValid():
        print(f"跳过无效图层: {layer.name()}")
        continue

    # ---- GDB 图层名合法化 ----
    layer_name = layer.name()
    layer_name = re.sub(r"[^\w\u4e00-\u9fa5]", "_", layer_name)

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "OpenFileGDB"
    options.layerName = layer_name
    options.fileEncoding = "UTF-8"

    if target_crs:
        options.destCRS = target_crs

    error = QgsVectorFileWriter.writeAsVectorFormatV2(
        layer,
        gdb_path,
        QgsProject.instance().transformContext(),
        options
    )

    if error[0] == QgsVectorFileWriter.NoError:
        print(f"✓ 已导出: {layer.name()} -> {layer_name}")
    else:
        print(f"✗ 导出失败: {layer.name()}")

print("GDB 导出完成。")

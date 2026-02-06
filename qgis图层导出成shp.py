from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsVectorFileWriter
)
import os
import re

# 1. 输出目录（自行修改）
# =========================
output_dir = r"D:/qgis_export_shp"   # ← 改成你的目录

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# =========================
# 2. 目标坐标系：EPSG:4326
# =========================
target_crs = QgsCoordinateReferenceSystem("EPSG:4326")

# =========================
# 3. 获取当前工程的所有图层
# =========================
layers = QgsProject.instance().mapLayers().values()

print("开始批量导出 Shapefile ……")

# =========================
# 4. 逐图层导出
# =========================
for layer in layers:

    if not isinstance(layer, QgsVectorLayer):
        continue

    if not layer.isValid():
        print(f"跳过无效图层: {layer.name()}")
        continue

    # ---- Shapefile 文件名合法化 ----
    layer_name = re.sub(r"[^\w\u4e00-\u9fa5]", "_", layer.name())
    shp_path = os.path.join(output_dir, f"{layer_name}.shp")

    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "ESRI Shapefile"
    options.fileEncoding = "UTF-8"
    options.destCRS = target_crs

    error = QgsVectorFileWriter.writeAsVectorFormatV2(
        layer,
        shp_path,
        QgsProject.instance().transformContext(),
        options
    )

    if error[0] == QgsVectorFileWriter.NoError:
        print(f"✓ 已导出: {layer.name()}")
    else:
        print(f"✗ 导出失败: {layer.name()}")

print("全部图层 Shapefile 导出完成。")

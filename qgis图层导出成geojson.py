from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsVectorFileWriter
)
import os

# =========================
# 1. 设置输出目录（自行修改）
# =========================
output_dir = r"D:/qgis_export_geojson"   # ← 改成你自己的目录

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

print("开始导出 GeoJSON 图层……")

for layer in layers:
    # 仅处理矢量图层
    if not isinstance(layer, QgsVectorLayer):
        continue

    if not layer.isValid():
        print(f"跳过无效图层: {layer.name()}")
        continue

    layer_name = layer.name().replace(" ", "_")
    output_path = os.path.join(output_dir, f"{layer_name}.geojson")

    # =========================
    # 4. 导出参数
    # =========================
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GeoJSON"
    options.fileEncoding = "UTF-8"
    options.destCRS = target_crs

    # =========================
    # 5. 执行导出（自动重投影）
    # =========================
    error = QgsVectorFileWriter.writeAsVectorFormatV2(
        layer,
        output_path,
        QgsProject.instance().transformContext(),
        options
    )

    if error[0] == QgsVectorFileWriter.NoError:
        print(f"✓ 已导出: {layer.name()} -> {output_path}")
    else:
        print(f"✗ 导出失败: {layer.name()}")

print("全部图层导出完成。")

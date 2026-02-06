import geopandas as gpd
from pathlib import Path

# =========================
# 参数区（按需修改）
# =========================
input_dir = Path(r"D:\qgis_export_geojson")    # 原始 GeoJSON 目录
output_dir = Path(r"D:\qgis_export_geojson4326")  # 输出目录（EPSG:4326）

target_crs = "EPSG:4326"

# =========================
# 主逻辑
# =========================
output_dir.mkdir(parents=True, exist_ok=True)

geojson_files = list(input_dir.glob("*.geojson"))

if not geojson_files:
    raise RuntimeError(f"目录中未找到 GeoJSON 文件: {input_dir}")

for geojson_path in geojson_files:
    try:
        print(f"处理文件: {geojson_path.name}")

        gdf = gpd.read_file(geojson_path)

        if gdf.crs is None:
            raise ValueError("源文件无 CRS 信息，无法重投影")

        if gdf.crs.to_string() != target_crs:
            gdf = gdf.to_crs(target_crs)

        output_path = output_dir / geojson_path.name
        gdf.to_file(output_path, driver="GeoJSON")

    except Exception as e:
        print(f"❌ 处理失败: {geojson_path.name}")
        print(f"   原因: {e}")

print("✅ 所有文件处理完成")

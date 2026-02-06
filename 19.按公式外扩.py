import geopandas as gpd
from shapely.geometry import Polygon
import math


# 计算扩展矩形的边界（DEM）
def calculate_DEM_expanded_bounds(x_coords, y_coords, D, d):
    x_min = math.floor((min(x_coords) - D) / d) * d
    x_max = math.floor((max(x_coords) + D) / d) * d
    y_min = math.floor((min(y_coords) - D) / d) * d
    y_max = math.floor((max(y_coords) + D) / d) * d
    return x_min, y_min, x_max, y_max


# 计算扩展矩形的边界（DBM）
def calculate_DBM_expanded_bounds(x_coords, y_coords, D, d):
    x_min = math.floor((min(x_coords) - D) / d) * d
    x_max = math.floor(((max(x_coords) + D) / d) + 1) * d
    y_min = math.floor((min(y_coords) - D) / d) * d
    y_max = math.floor(((max(y_coords) + D) / d) + 1) * d
    return x_min, y_min, x_max, y_max


# 扩展多边形并保存新的 Shapefile，同时复制属性
def process_shapefile(input_shp, output_shp, D, d, flag):
    # 读取输入 Shapefile
    gdf = gpd.read_file(input_shp)

    expanded_geometries = []

    for idx, row in gdf.iterrows():
        geom = row['geometry']

        # 确保几何类型为 Polygon 或 MultiPolygon
        if geom.geom_type not in ['Polygon', 'MultiPolygon']:
            print(f"第 {idx} 个几何体不是 Polygon 或 MultiPolygon， 跳过.")
            expanded_geometries.append(None)
            continue

        # 对于 MultiPolygon，处理每个部分
        if geom.geom_type == 'MultiPolygon':
            sub_polygons = []
            for poly in geom:
                x_coords = [p[0] for p in poly.exterior.coords[:-1]]  # 去掉最后一个点
                y_coords = [p[1] for p in poly.exterior.coords[:-1]]

                if flag == 'DEM':
                    x_min, y_min, x_max, y_max = calculate_DEM_expanded_bounds(x_coords, y_coords, D, d)
                elif flag == 'DBM':
                    x_min, y_min, x_max, y_max = calculate_DBM_expanded_bounds(x_coords, y_coords, D, d)
                else:
                    raise ValueError("只能处理 'DEM' 或 'DBM'")

                expanded_polygon = Polygon([
                    (x_min, y_min),
                    (x_min, y_max),
                    (x_max, y_max),
                    (x_max, y_min)
                ])
                sub_polygons.append(expanded_polygon)
            # 合并所有扩展后的子多边形为一个 MultiPolygon
            expanded_geometries.append(gpd.GeoSeries(sub_polygons).unary_union)
        else:
            # 处理单个 Polygon
            x_coords = [p[0] for p in geom.exterior.coords[:-1]]  # 去掉最后一个点
            y_coords = [p[1] for p in geom.exterior.coords[:-1]]

            if flag == 'DEM':
                x_min, y_min, x_max, y_max = calculate_DEM_expanded_bounds(x_coords, y_coords, D, d)
            elif flag == 'DBM':
                x_min, y_min, x_max, y_max = calculate_DBM_expanded_bounds(x_coords, y_coords, D, d)
            else:
                raise ValueError("只能处理 'DEM' 或 'DBM'")

            # 创建扩展后的矩形
            expanded_polygon = Polygon([
                (x_min, y_min),  # 左下角
                (x_min, y_max),  # 左上角
                (x_max, y_max),  # 右上角
                (x_max, y_min)  # 右下角
            ])

            expanded_geometries.append(expanded_polygon)

    # 创建一个新的 GeoDataFrame，保留原有属性并替换几何体
    expanded_gdf = gdf.copy()
    expanded_gdf['geometry'] = expanded_geometries

    # 移除任何因非多边形几何体而产生的空值
    expanded_gdf = expanded_gdf[expanded_gdf['geometry'].notnull()]

    # 保存扩展后的 Shapefile
    expanded_gdf.to_file(output_shp)
    print(f"扩展后的 Shapefile 已保存到：{output_shp}")


# 示例调用
if __name__ == "__main__":
    input_shp = r"F:\图框外扩\25年2m需要的图框zone41-DEM12047.shp"  #
    output_shp = r"F:\图框外扩\25年2m需要的图框zone41-DEM12047-2mDEM格网.shp"
    D = 100
    d = 2
    process_shapefile(input_shp, output_shp, D, d, 'DEM')



    # input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok.shp"  #
    # output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok-2mDEM格网.shp"
    # D = 100
    # d = 2
    # process_shapefile(input_shp, output_shp, D, d, 'DEM')
    #
    #
    # input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok.shp"  #
    # output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok-10mDEM格网.shp"
    # D = 100
    # d = 10
    # process_shapefile(input_shp, output_shp, D, d, 'DEM')
    #
    # # DBM
    # input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok.shp"  #
    # output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok-10mDBM格网.shp"
    # D = 100
    # d = 10
    # process_shapefile(input_shp, output_shp, D, d, 'DBM')
    #
    #
    # input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部.shp"  #
    # output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部-2mDEM格网.shp"
    # D = 100
    # d = 2
    # process_shapefile(input_shp, output_shp, D, d, 'DEM')
    #
    # input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部.shp"  #
    # output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部-10mDBM格网.shp"
    # D = 100
    # d = 10
    # process_shapefile(input_shp, output_shp, D, d, 'DBM')
    #
    # input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部.shp"  #
    # output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部-10mDEM格网.shp"
    # D = 100
    # d = 10
    # process_shapefile(input_shp, output_shp, D, d, 'DEM')

    # input_shp = r"D:\program\Tencent\wxfile\WeChat Files\wxid_lg5qw50izy2122\FileStorage\File\2025-01\5bao结合表\结合表.shp"
    # output_shp = r"D:\program\Tencent\wxfile\WeChat Files\wxid_lg5qw50izy2122\FileStorage\File\2025-01\5bao结合表\结合表-2mDEM格网.shp"
    # D = 100
    # d = 2
    # process_shapefile(input_shp, output_shp, D, d, 'DEM')
    #
    # input_shp = r"D:\program\Tencent\wxfile\WeChat Files\wxid_lg5qw50izy2122\FileStorage\File\2025-01\5bao结合表\结合表.shp"
    # output_shp = r"D:\program\Tencent\wxfile\WeChat Files\wxid_lg5qw50izy2122\FileStorage\File\2025-01\5bao结合表\结合表-10mDEM格网.shp"
    # D = 100
    # d = 10
    # process_shapefile(input_shp, output_shp, D, d, 'DEM')
    #
    # input_shp = r"D:\program\Tencent\wxfile\WeChat Files\wxid_lg5qw50izy2122\FileStorage\File\2025-01\5bao结合表\结合表.shp"
    # output_shp = r"D:\program\Tencent\wxfile\WeChat Files\wxid_lg5qw50izy2122\FileStorage\File\2025-01\5bao结合表\结合表-10mDBM格网.shp"
    # D = 100
    # d = 10
    # process_shapefile(input_shp, output_shp, D, d, 'DBM')

# import geopandas as gpd
# from shapely.geometry import Polygon
# import math
#
#
# # 计算扩展矩形的边界
# def calculate_DEM_expanded_bounds(x_coords, y_coords, D, d):
#     # 根据公式计算新的边界
#     x_min = math.floor((min(x_coords) - D) / d) * d
#     x_max = math.floor((max(x_coords) + D) / d) * d
#     y_min = math.floor((min(y_coords) - D) / d) * d
#     y_max = math.floor((max(y_coords) + D) / d) * d
#     return x_min, y_min, x_max, y_max
#
#
# def calculate_DBM_expanded_bounds(x_coords, y_coords, D, d):
#     x_min = math.floor((min(x_coords) - D) / d) * d
#     x_max = math.floor(((max(x_coords) + D) / d) + 1) * d
#     y_min = math.floor((min(y_coords) - D) / d) * d
#     y_max = math.floor(((max(y_coords) + D) / d) + 1) * d
#     return x_min, y_min, x_max, y_max
#
#
# # 扩展多边形并保存新的 Shapefile
# def process_shapefile(input_shp, output_shp, D, d, flag):
#     # 读取输入 Shapefile
#     gdf = gpd.read_file(input_shp)
#
#     expanded_geometries = []
#
#     for idx, geom in gdf.iterrows():
#         # 获取原始多边形的外包矩形边界,不是最小外接，最小外接用Bounds
#         # x_coords = [p[0] for p in geom['geometry'].exterior.coords]
#         # y_coords = [p[1] for p in geom['geometry'].exterior.coords]
#
#         x_coords = [p[0] for p in geom['geometry'].exterior.coords[:-1]]  # 去掉最后一个点,起止点相同
#         y_coords = [p[1] for p in geom['geometry'].exterior.coords[:-1]]  # 去掉最后一个点,起止点相同
#
#         # 打印矩形点数和坐标
#         # print(f"矩形 {idx + 1}:")
#         # print(f"点数: {len(geom['geometry'].exterior.coords)}")
#         # print("点坐标:")
#         # print(f"x_coords: {x_coords}")
#         # print(f"y_coords: {y_coords}")
#         # print("---")
#
#         # 根据公式计算扩展后的矩形边界
#         if flag == 'DEM':
#             x_min, y_min, x_max, y_max = calculate_DEM_expanded_bounds(x_coords, y_coords, D, d)
#         elif flag == 'DBM':
#             x_min, y_min, x_max, y_max = calculate_DBM_expanded_bounds(x_coords, y_coords, D, d)
#
#         # 创建扩展后的矩形
#         expanded_polygon = Polygon([
#             (x_min, y_min),  # 左下角
#             (x_min, y_max),  # 左上角
#             (x_max, y_max),  # 右上角
#             (x_max, y_min)  # 右下角
#         ])
#
#         expanded_geometries.append(expanded_polygon)
#
#     # 创建新的 GeoDataFrame 保存扩展后的多边形
#     gdf['geometry'] = expanded_geometries
#     gdf.to_file(output_shp)
#     print(f"扩展后的 Shapefile 已保存到：{output_shp}")


# 输入和输出Shapefile路径
# if __name__ == '__main__':
#     input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok.shp"  #
#     output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok-2mDEM格网.shp"
#     D = 100
#     d = 2
#     process_shapefile(input_shp, output_shp, D, d,'DEM')
#
#     input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部.shp"  #
#     output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部-2mDEM格网.shp"
#     D = 100
#     d = 2
#     process_shapefile(input_shp, output_shp, D, d, 'DEM')
#
#     input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok.shp"  #
#     output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok-10mDEM格网.shp"
#     D = 100
#     d = 10
#     process_shapefile(input_shp, output_shp, D, d, 'DEM')
#
#     input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部.shp"  #
#     output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部-10mDEM格网.shp"
#     D = 100
#     d = 10
#     process_shapefile(input_shp, output_shp, D, d, 'DEM')
#
#
#
#    # DBM
#     input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok.shp"  #
#     output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone40全部ok-10mDBM格网.shp"
#     D = 100
#     d = 10
#     process_shapefile(input_shp, output_shp, D, d,'DBM')
#
#
#     input_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部.shp"  #
#     output_shp = r"D:\ren\code\python-shapefile-operate-develop\提交\图幅外扩\图框zone41全部-10mDBM格网.shp"
#     D = 100
#     d = 10
#     process_shapefile(input_shp, output_shp, D, d, 'DBM')

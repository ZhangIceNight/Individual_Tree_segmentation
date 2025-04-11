import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
gdal.UseExceptions()

def calculate_CHM(points, resolution=0.5):
    """
    计算点云数据的冠层高度模型(CHM)
    
    参数:
        points: numpy数组,包含点云xyz坐标
        resolution: CHM的空间分辨率,默认0.5m
    
    返回:
        chm: 计算得到的CHM数组
        geotransform: 地理变换参数元组(x_min, resolution, 0, y_max, 0, -resolution)
    """
    # 获取点云范围
    x_min, x_max = np.min(points[:,0]), np.max(points[:,0])
    y_min, y_max = np.min(points[:,1]), np.max(points[:,1])
    
    # 计算网格大小
    cols = int((x_max - x_min) / resolution) + 1
    rows = int((y_max - y_min) / resolution) + 1
    
    # 初始化CHM矩阵
    chm = np.zeros((rows, cols))
    
    # 将点云数据映射到网格
    for p in points:
        col = int((p[0] - x_min) / resolution)
        row = int((y_max - p[1]) / resolution)
        if 0 <= row < rows and 0 <= col < cols:
            chm[row, col] = max(chm[row, col], p[2])
            
    # 生成地理变换参数
    geotransform = (x_min, resolution, 0, y_max, 0, -resolution)
    
    return chm, geotransform

def save_CHM(CHM_array, geotransform, savepath=None):
    """
    将CHM保存为GeoTIFF文件
    
    参数:
        CHM_array: CHM数组
        geotransform: 地理变换参数
        savepath: 保存文件的完整路径,默认为None时使用当前目录和时间戳命名
    """
    # 如果未指定保存路径,使用默认路径和文件名
    if savepath is None:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        savepath = f'CHM_{timestamp}.tif'
        
    # 创建GeoTIFF文件
    driver = gdal.GetDriverByName('GTiff')
    rows, cols = CHM_array.shape
    dataset = driver.Create(savepath, cols, rows, 1, gdal.GDT_Float32)
    
    # 设置地理变换参数
    dataset.SetGeoTransform(geotransform)
    
    # 写入数据
    band = dataset.GetRasterBand(1)
    band.WriteArray(CHM_array)
    
    # 清理资源
    dataset = None


def load_CHMasArray(CHM_filepath):
    dataset = gdal.Open(CHM_filepath)
    CHM_array = dataset.ReadAsArray()
    return CHM_array

def load_CHM(CHM_filepath):
    dataset = gdal.Open(CHM_filepath)
    return dataset

def vis_CHM_with_plt(CHM_filepath, savepath, title_, cmap_='gray'):
    chm = load_CHMasArray(CHM_filepath=CHM_filepath)
    # projection = chm.GetProjection()
    # geotransform = chm.GetGeoTransform
    # print(projection)
    # print(geotransform)
    plt.imshow(chm, cmap=cmap_) #viridis, gray 
    plt.colorbar(label='Elevation (m)')
    plt.title(title_)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.savefig(savepath)
    plt.show()

def show_CHM_information(CHM_filepath):
    chm = load_CHM(CHM_filepath=CHM_filepath)
    projection = chm.GetProjection()
    geotransform = chm.GetGeoTransform
    print(projection)
    print(geotransform)
    print(chm)

def save_CHM_from_pcd(pcd, CHM_savepath):
    chm, geotransform = calculate_CHM(pcd)
    save_CHM(CHM_array=chm, geotransform=geotransform, savepath=CHM_savepath)

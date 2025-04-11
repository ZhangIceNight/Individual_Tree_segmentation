import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    from VNSC import VoxelNystromSC
    import mahotas
    from osgeo import gdal
    import gc
    import os
    return VoxelNystromSC, gc, gdal, mahotas, np, os


@app.cell
def _(mahotas, np):
    ####################################### CHM局部最大值检测 #######################
    def localmaxima(img, d, ws): 
        """
        检测冠层高度模型(CHM)中的局部最大值
        参数:
            img: CHM图像数据
            d: 空间分辨率
            ws: 窗口大小(默认3m)
        返回:
            n_spots: 检测到的局部最大值数量
        """
        threshed = (img > ws)  # 阈值处理
        img *= threshed       # 将低于阈值的像素值置为0
        bc = np.ones((int(ws/d), int(ws/d)))  # 创建结构元素
        maxima = mahotas.morph.regmax(img, Bc=bc)  # 检测局部最大值
        spots, n_spots = mahotas.label(maxima)  # 标记连通区域
        return n_spots
    return (localmaxima,)


@app.cell
def _(os):
    ############################################ 主函数 ##############################################
    path = os.getcwd()  # 获取当前工作目录
    # 创建结果文件夹
    isExists = os.path.exists(path+'\\results')
    if not isExists:
        os.mkdir('results')
    return isExists, path


@app.cell
def _(os, path):
    # 获取目录中的所有文件和文件夹名称
    files = os.listdir(path)
    # 查找CHM文件(.tif格式)
    for file in files:
        if os.path.splitext(file)[1] == '.tif':  
            CHM_name = file
            break
    print(CHM_name)
    return CHM_name, file, files


@app.cell
def _(files, np, os):
    for txtfile in files:
        if os.path.splitext(txtfile)[1] == '.txt':
            print('开始处理:', txtfile)
            X = np.loadtxt(txtfile)  # 加载点云数据
            Z = X[:,2]  # 提取高度值
            # 筛选高度大于2.5m的点
            id0 = []
            for ii in range(0, len(Z)):
                if Z[ii] > 2.5:
                    id0.extend([ii])
            X = X[id0,:]
            
    return X, Z, id0, ii, txtfile


@app.cell
def _(Z):
    Z
    return


app._unparsable_cell(
    r"""
            ###################读取并处理CHM数据##################
            img = gdal.Open(CHM_name)
            im_width = img.RasterXSize    # 获取栅格数据的宽度
            im_height = img.RasterYSize   # 获取栅格数据的高度
            im_geotrans = img.GetGeoTransform()  # 获取仿射变换参数
            x0 = im_geotrans[0]  # 左上角x坐标
            y1 = im_geotrans[3]  # 左上角y坐标
            d = im_geotrans[1]   # 空间分辨率
            
            # 计算点云数据的边界范围
            xi = int((X[np.lexsort([X[:,0]])[0],0]-x0)/d)  # 最小x
            xj = int((X[np.lexsort([-X[:,0]])[0],0]-x0)/d) # 最大x
            dx = xj-xi                                     
            yi = int((y1-X[np.lexsort([X[:,1]])[0],1])/d)  # 最小y
            yj = int((y1-X[np.lexsort([-X[:,1]])[0],1])/d) # 最大y
            dy = yj-yi
            
            # 确保边界在图像范围内
            xl = max(xi,0)  
            xr = max(min(xj,im_width),0)
            yt = max(yj,0)
            yb = max(min(yi,im_height),0)
        
            # 读取指定范围的CHM数据
            im_data = img.ReadAsArray(xl,yt,xr-xl,yb-yt) 
            # 检测局部最大值
            nmax = localmaxima(im_data,d,3) 
            # 释放内存
            del img,im_data
            gc.collect()  
        
            # 设置聚类数量上限(为局部最大值的1.5倍)
            gap = nmax*1.5
            XX = X[:,:3]       
            # 执行Nyström谱聚类
            VoxelNystromSC(XX, file.split('.')[0], int(gap), path)  

    """,
    name="_"
)


@app.cell
def _(VoxelNystromSC, gc, gdal, localmaxima, np, os, path):
    # 遍历目录寻找输入文件
    for root, dirs, files in os.walk(path):
        # 查找CHM文件(.tif格式)
        for file in files:
            if os.path.splitext(file)[1] == '.tif':  
                CHM_name = file
                break  
        # 处理点云数据文件(.txt格式)
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                print('开始处理:', file)
                X = np.loadtxt(file)  # 加载点云数据
                Z = X[:,2]  # 提取高度值
                # 筛选高度大于2.5m的点
                id0 = []
                for ii in range(0, len(Z)):
                    if Z[ii] > 2.5:
                       id0.extend([ii])
                X = X[id0,:]
            
                ###################读取并处理CHM数据##################
                img = gdal.Open(CHM_name)
                im_width = img.RasterXSize    # 获取栅格数据的宽度
                im_height = img.RasterYSize   # 获取栅格数据的高度
                im_geotrans = img.GetGeoTransform()  # 获取仿射变换参数
                x0 = im_geotrans[0]  # 左上角x坐标
                y1 = im_geotrans[3]  # 左上角y坐标
                d = im_geotrans[1]   # 空间分辨率
            
                # 计算点云数据的边界范围
                xi = int((X[np.lexsort([X[:,0]])[0],0]-x0)/d)  # 最小x
                xj = int((X[np.lexsort([-X[:,0]])[0],0]-x0)/d) # 最大x
                dx = xj-xi                                     
                yi = int((y1-X[np.lexsort([X[:,1]])[0],1])/d)  # 最小y
                yj = int((y1-X[np.lexsort([-X[:,1]])[0],1])/d) # 最大y
                dy = yj-yi
            
                # 确保边界在图像范围内
                xl = max(xi,0)  
                xr = max(min(xj,im_width),0)
                yt = max(yj,0)
                yb = max(min(yi,im_height),0)
            
                # 读取指定范围的CHM数据
                im_data = img.ReadAsArray(xl,yt,xr-xl,yb-yt) 
                # 检测局部最大值
                nmax = localmaxima(im_data,d,3) 
                # 释放内存
                del img,im_data
                gc.collect()  
            
                # 设置聚类数量上限(为局部最大值的1.5倍)
                gap = nmax*1.5
                XX = X[:,:3]       
                # 执行Nyström谱聚类
                VoxelNystromSC(XX, file.split('.')[0], int(gap), path)  


    return (
        CHM_name,
        X,
        XX,
        Z,
        d,
        dirs,
        dx,
        dy,
        file,
        files,
        gap,
        id0,
        ii,
        im_data,
        im_geotrans,
        im_height,
        im_width,
        img,
        nmax,
        root,
        x0,
        xi,
        xj,
        xl,
        xr,
        y1,
        yb,
        yi,
        yj,
        yt,
    )


if __name__ == "__main__":
    app.run()

# 基于Nystrӧm的谱聚类
该代码是基于K近邻采样(KNNS)方法的Nystrӧm谱聚类的实现(Pang等, 2021)。它旨在使用机载LiDAR点云数据进行单木分割。

# 使用代码时请引用:
Yong Pang, Weiwei Wang, Liming Du, Zhongjun Zhang, Xiaojun Liang, Yongning Li, Zuyuan Wang (2021) Nystrӧm-based spectral clustering using airborne LiDAR point cloud data for individual tree segmentation, International Journal of Digital Earth

# 代码文件:
'segmentation.py': 主函数,包括从冠层高度模型(CHM)中提取局部最大值;
'VNSC.py': 算法的其他功能,包括均值漂移体素化、相似度图构建、KNNS采样、特征分解、k-means聚类,以及单木参数的计算和写入。

# 关键参数:
使用代码时,用户可以根据具体数据特征调整局部最大值窗口、gap(最终聚类数量的上限)、knn(相似度图中k近邻的数量)和均值漂移方法中的分位数值。目前,局部最大值窗口值为3m×3m,gap值定义为从CHM检测到的局部最大值的1.5倍。参数knn可以根据数据特征定义为常数值(代码中为40),或通过它与体素数量之间的关系来确定。均值漂移方法中分位数的默认设置是点云的平均密度。更多细节可以在Pang等(2021)中找到。

# 测试数据:
'ALS_pointclouds.txt': 点云数据;
'ALS_CHM.tif': 点云数据的CHM;
'Reference_tree.csv': 用于算法验证的实地测量数据。位置使用差分GNSS测量。该文件中每棵树的树高是通过回归估计获得的。

# 输出:
'Data_seg.csv': 每个点的坐标(x, y, z)以及分割后的聚类标签;
'Parameter.csv': 基于Pang等(2021)中描述的计算方法得到的单木参数(树木ID、位置X、位置Y、树冠、树高)。

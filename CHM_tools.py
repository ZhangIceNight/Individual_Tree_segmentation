import numpy as np

# 数据的基本统计信息，如最小值、最大值、均值等
min_elevation = np.min(elevation_data)
max_elevation = np.max(elevation_data)
mean_elevation = np.mean(elevation_data)
print(f"Minimum Elevation: {min_elevation} m")

print(f"Maximum Elevation: {max_elevation} m")

print(f"Mean Elevation: {mean_elevation} m")


#过滤和分析，例如，提取特定范围内的高程区域
# 提取高于1000米的区域
high_elevation_area = elevation_data > 1000
# 计算高于1000米区域的比例
high_elevation_ratio = np.sum(high_elevation_area) / elevation_data.size


print(f"Proportion of Area Above 1000m: {high_elevation_ratio:.2%}")

# 基于现有DEM生成新的数据，例如将高程值进行平滑处理。

from scipy.ndimage import gaussian_filter

# 对DEM数据进行高斯平滑

smoothed_elevation_data = gaussian_filter(elevation_data, sigma=1)


# 显示平滑后的DEM数据

plt.imshow(smoothed_elevation_data, cmap='terrain')


plt.colorbar(label='Elevation (m)')


plt.title('Smoothed DEM Visualization')


plt.xlabel('X Coordinate')


plt.ylabel('Y Coordinate')


plt.show()
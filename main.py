import os 
import numpy as np
from load_points import read_point_cloud_from_txt
from CHM_calculate import calculate_CHM, load_CHM, load_CHMasArray, convertCHM2PNG, save_CHM
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # load raw point clouds to np array
    pct_file_path = 'ALS_pointclouds.txt'
    pct = read_point_cloud_from_txt(pct_file_path, delimiter=' ')
    pct = np.array(pct)
    
    # # calculate CHM
    # chm, geotransform = calculate_CHM(pct)
    # new_CHM_savepath = 'new_CHM.tif'
    # save_CHM(CHM_array=chm, geotransform=geotransform, savepath=new_CHM_savepath)
    # convertCHM2PNG(CHM_filepath=new_CHM_savepath, savepath='./new_CHM.png')

    # convert old CHM
    old_CHM_filepath = 'ALS_CHM.tif'
    # convertCHM2PNG(CHM_filepath=old_CHM_filepath, savepath='./old_CHM.png')
    chm = load_CHMasArray(CHM_filepath=old_CHM_filepath)
    # projection = chm.GetProjection()
    # geotransform = chm.GetGeoTransform
    # print(projection)
    # print(geotransform)
    plt.imshow(chm, cmap='terrain') #viridis, gray 
    plt.colorbar(label='Elevation (m)')
    plt.title('CHM Visualization')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.show()
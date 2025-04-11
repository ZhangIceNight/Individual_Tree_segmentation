import os 
import numpy as np
from load_points import read_point_cloud_from_txt
from CHM_calculate import calculate_CHM, load_CHM, load_CHMasArray, \
save_CHM, save_CHM_from_pcd, vis_CHM_with_plt, show_CHM_information
import matplotlib.pyplot as plt



if __name__ == '__main__':
    # load raw point clouds to np array
    pcd_file_path = 'ALS_pointclouds.txt'
    pcd = read_point_cloud_from_txt(pcd_file_path, delimiter=' ')
    pcd = np.array(pcd)
    save_CHM_from_pcd(pcd=pcd, CHM_savepath='new_CHM.tif')

    # # vis old CHM
    old_CHM_filepath = 'ALS_CHM.tif'
    # savepath_ = old_CHM_filepath.split('.')[0] + '_old_vis.png'
    # vis_CHM_with_plt(CHM_filepath=old_CHM_filepath, savepath=savepath_, title_='old_CHM')
    # # vis new CHM
    new_CHM_filepath = 'new_CHM.tif'
    # new_savepath_ = new_CHM_filepath.split('.')[0] + '_new_vis.png'
    # vis_CHM_with_plt(CHM_filepath=new_CHM_filepath, savepath=new_savepath_, title_='new_CHM')

    # compare two CHM
    # show_CHM_information(CHM_filepath=old_CHM_filepath)
    # print('-'*20)
    show_CHM_information(CHM_filepath=new_CHM_filepath)
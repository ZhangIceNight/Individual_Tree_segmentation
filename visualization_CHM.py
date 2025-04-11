import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium")


@app.cell
def _():
    return


@app.cell
def _():
    import os 
    import numpy as np
    from load_points import read_point_cloud_from_txt
    from CHM_calculate import calculate_CHM, load_CHM, load_CHMasArray, convertCHM2PNG, save_CHM
    import matplotlib.pyplot as plt
    return (
        calculate_CHM,
        convertCHM2PNG,
        load_CHM,
        load_CHMasArray,
        np,
        os,
        plt,
        read_point_cloud_from_txt,
        save_CHM,
    )


@app.cell
def _(np, read_point_cloud_from_txt):
    # load raw point clouds to np array
    pct_file_path = 'ALS_pointclouds.txt'
    pct = read_point_cloud_from_txt(pct_file_path, delimiter=' ')
    pct = np.array(pct)
    return pct, pct_file_path


@app.cell
def _(calculate_CHM, pct, save_CHM):
    # # calculate CHM
    chm, geotransform = calculate_CHM(pct)
    new_CHM_savepath = 'new_CHM.tif'
    save_CHM(CHM_array=chm, geotransform=geotransform, savepath=new_CHM_savepath)
    # convertCHM2PNG(CHM_filepath=new_CHM_savepath, savepath='./new_CHM.png')
    return chm, geotransform, new_CHM_savepath


@app.cell
def _(load_CHMasArray, plt):
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
        print(chm)
    return (vis_CHM_with_plt,)


@app.cell
def _(vis_CHM_with_plt):
    # convert old CHM

    old_CHM_filepath = 'ALS_CHM.tif'
    savepath_ = old_CHM_filepath.split('.')[0] + '_old_vis.png'
    vis_CHM_with_plt(CHM_filepath=old_CHM_filepath, savepath=savepath_, title_='old_CHM')
    return old_CHM_filepath, savepath_


@app.cell
def _(vis_CHM_with_plt):
    # vis new CHM
    new_CHM_filepath = 'new_CHM.tif'
    new_savepath_ = new_CHM_filepath.split('.')[0] + '_new_vis.png'
    vis_CHM_with_plt(CHM_filepath=new_CHM_filepath, savepath=new_savepath_, title_='new_CHM')
    return new_CHM_filepath, new_savepath_


@app.cell
def _(new_savepath_):
    new_savepath_
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

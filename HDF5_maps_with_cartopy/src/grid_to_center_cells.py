import numpy as np


def lonlat_grid_to_center_cells(lon_grd, lat_grd):
    
    n_lines = lon_grd.shape[0]
    n_columns = lon_grd.shape[1]

    lon_cen = np.zeros((n_lines-1, n_columns-1))
    lat_cen = np.zeros((n_lines-1, n_columns-1))

    for i in range(0,n_lines-1):
        lon_i = lon_grd[i]
        lat_i = lat_grd[i]
        lon_i1 = lon_grd[i+1]
        lat_i1 = lat_grd[i+1]

        for j in range(0,n_columns-1):
            XSW = lon_i[j]
            YSW = lat_i[j]
            XSE = lon_i[j+1]
            YSE = lat_i[j+1]
            XNE = lon_i1[j+1]
            YNE = lat_i1[j+1]
            XNW = lon_i1[j]
            YNW = lat_i1[j]

            lon_cen[i][j] = (XSW + XSE + XNE + XNW) / 4.0
            lat_cen[i][j]= (YSW + YSE + YNE + YNW) / 4.0
    
    return (lon_cen, lat_cen)

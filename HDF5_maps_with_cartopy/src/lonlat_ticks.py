import numpy as np

def ticks_definer(lons_grd, lats_grd, interval):

    i = interval

    d = '\N{DEGREE SIGN}'

    xmin = np.min(lons_grd)
    xmax = np.max(lons_grd)

    ymin = np.min(lats_grd)
    ymax = np.max(lats_grd)

    xticks = []
    yticks = []
    xticklabels = []
    yticklabels = []

    dec_n = len(str(i)) - 2

    x = round(xmin-i, dec_n-1)
    y = round(ymin-i, dec_n-1)

    while True:
        if xmin <= x <= xmax:
            xticks.append(round(x, dec_n))
        elif x > xmax:
            break
        x += i

    while True:
        if ymin <= y <= ymax:
            yticks.append(round(y, dec_n))
        elif y > ymax:
            break
        y += i

    for x in xticks:
        if x < 0:
            card = 'W'
            x = x * -1
        elif x >= 0:
            card = 'E'
        xticklabels.append(str(x).ljust(dec_n+2,'0')+d+card)

    for y in yticks:
        if y < 0:
            card = 'S'
            y = y * -1
        elif y >= 0:
            card = 'N'
        yticklabels.append(str(y).ljust(dec_n+3,'0')+d+card)

    return xticks, yticks, xticklabels, yticklabels

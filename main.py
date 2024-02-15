from fileinput import filename
from numpy import dtype
import numpy
from pandas import DataFrame, read_excel
import os.path
import math

# import pyproj
from pyproj import CRS
from pprint import pprint
from pyproj import Transformer

wgs84 = CRS.from_string("EPSG:4326")
utm48n = CRS.from_string("EPSG:32648")

wgs84_to_utm48 = Transformer.from_crs(wgs84, utm48n)
utm48_to_wgs84 = Transformer.from_crs(utm48n, wgs84)

dt = [crs.to_wkt(pretty=True) for crs in [wgs84, utm48n]]

# pprint(dt)



DIR = r"E:\RC\16 июня 2016 работа\Data " \
    r"(D)\Mazaeva disk D 2020\Articles 2021август\taylor " \
    r"and francis\revision\Rassvet 2"

DIR = "./"


def convert(filexls,
            filecsv=None,
            sheetname="Лист1",
            azimuthbase=0,
#            clockwise=True,
            basealt=None):

    if filecsv is None:
        filecsv = filexls
    # filexls = os.path.join(DIR, filexls)
    # filecsv = os.path.join(DIR, filecsv)
    filexls = filexls + ".xls"
    filecsv = filecsv + ".csv"
    coords = read_excel(filexls, sheet_name=sheetname)
    lat = coords.lat[0]
    lon = coords.lon[0]
    n = coords.n[0]
    assert (int(n) == 0), "Reference point name is not '0'"
    ref_x, ref_y = wgs84_to_utm48.transform(lat, lon)
    print("Reference point coords: x={} y={}".format(ref_x, ref_y))

    if basealt is None:
        try:
            basealt = int(coords.basealt[0])
        except AttributeError:
            basealt = 470

    print("Found the following columns:")
    print(list(coords.columns))
    coords.drop(columns=['lat', 'lon'])

    x = coords.x.to_numpy(dtype=float)
    y = coords.y.to_numpy(dtype=float)
    z = coords.z.to_numpy(dtype=float)

    # d = numpy.sqrt(x**2 + y**2)
    # # a = numpy.arctan(x / y)
    # l = len(d)
    # ay = numpy.array([0.0]*l)
    # ax = numpy.array([math.pi/2]*l)
    # ax = numpy.degrees(ax) + azimuthbase
    # ay = numpy.degrees(ay) + azimuthbase
    # if clockwise:
    #     ax = -ax
    #     ay = -ay
    ux = coords.x + ref_x
    uy = coords.y + ref_y
    lat, lon = utm48_to_wgs84.transform(ux, uy)
    c = DataFrame({
        "nW": coords.n,
        "n" : list(range(len(coords.n))),
        "utm48_x": ux,
        "utm48_y": uy,
        'x': coords.x,
        "y": coords.y,
        "z": coords.z,
        "lat": lat,
        "lon": lon,
        'zabs' : coords.z + basealt
    })
    # # ind = DataFrame({'d': d, 'a': a})
    # g = pyproj.Geod(ellps='WGS84')
    # # print(len(ax), len(d), l)
    # _lon = numpy.array([lon] * l)
    # _lat = numpy.array([lat] * l)
    # _x = [_lon, _lat, ax, x]
    # # print([len(x) for x in _])
    # lox, lax, bax = g.fwd(*_x)
    # _y = [lox, lax, ay, y]
    # lo, la, ba = g.fwd(*_y)
    # r = DataFrame({
    #     'n': coords.n,
    #     'lat': la,
    #     'lon': lo,
    #     'z' : coords.z + basealt
    # })
    r = c
    # print(r)
    r.to_csv(filecsv)
    return r


if __name__ == "__main__":
    import sys
    import os.path
    if len(sys.argv)>1:
        fn = sys.argv[1] # File name of an Excel file at the first parameter
        root, ext = os.path.splitext(fn)
        if ext != ".xls":
            print("Error: the tool processes only XLS-files to CSV")
            quit()
        convert(root)
    else:
        convert("rassv(2008)")

# https://gis.stackexchange.com/questions/178201/calculate-the-distance-between-two-coordinates-wgs84-in-etrs89

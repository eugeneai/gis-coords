from fileinput import filename
from numpy import dtype
import numpy
from pandas import DataFrame, read_excel
import os.path
import math

import pyproj

DIR = r"E:\RC\16 июня 2016 работа\Data " \
    r"(D)\Mazaeva disk D 2020\Articles 2021август\taylor " \
    r"and francis\revision\Rassvet 2"

DIR = "./"


def convert(filexls,
            filecsv=None,
            sheetname="Лист1",
            azimuthbase=0,
            clockwise=True):

    if filecsv is None:
        filecsv = filexls
    filexls = os.path.join(DIR, filexls)
    filecsv = os.path.join(DIR, filexls)
    filexls = filexls + ".xls"
    filecsv = filecsv + ".csv"
    coords = read_excel(filexls, sheet_name=sheetname)
    lat = coords.lat[0]
    lon = coords.lon[0]
    print(coords.columns)
    coords.drop(columns=['lat', 'lon'])
    x = coords.x.to_numpy(dtype=float)
    y = coords.y.to_numpy(dtype=float)
    d = numpy.sqrt(x**2 + x**2)
    a = numpy.arctan(x / y)
    a[a == numpy.nan] = 0.0
    a = numpy.degrees(a) + azimuthbase
    if not clockwise:
        a = -a
    c = DataFrame({
        'x': coords.x,
        "y": coords.y,
        "z": coords.z,
        'd': d,
        'a': a
    })
    ind = DataFrame({'d': d, 'a': a})
    g = pyproj.Geod(ellps='WGS84')
    l = len(a)
    print(len(a), len(d), l)
    _lon = numpy.array([lon] * l)
    _lat = numpy.array([lat] * l)
    _ = [_lon, _lat, a, d]
    print([len(x) for x in _])
    lo, la, ba = g.fwd(*_)
    r = DataFrame({
        'n': coords.n,
        'lat': la,
        'lon': lo,
    })
    print(r)
    r.to_csv(filecsv)
    return r


if __name__ == "__main__":
    convert("rassv(2008)")

# https://gis.stackexchange.com/questions/178201/calculate-the-distance-between-two-coordinates-wgs84-in-etrs89

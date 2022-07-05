from fileinput import filename
from pandas import DataFrame, read_excel
import os.path

DIR = r"E:\RC\16 июня 2016 работа\Data " \
    r"(D)\Mazaeva disk D 2020\Articles 2021август\taylor " \
    r"and francis\revision\Rassvet 2"

DIR = "./"


def convert(filexls,
        filecsv = None, 
        sheetname="Лист1"):

    if filecsv is None:
        filecsv = filexls
    filexls = os.path.join(DIR, filexls)
    filecsv = os.path.join(DIR, filexls)
    filexls = filexls + ".xls"
    filecsv = filecsv + ".csv"
    coords = read_excel(filexls,
        sheet_name=sheetname)  
    lat = coords.lat[0]
    lon = coords.lon[0]
    print(coords.columns)
    coords.drop(columns = ['lat', 'lon'])
    c = DataFrame({
        'x': coords.x,
        "y": coords.y,
        "z": coords.z
    })
    print(c)

if __name__=="__main__":
    convert("rassv(2008)")

# https://gis.stackexchange.com/questions/178201/calculate-the-distance-between-two-coordinates-wgs84-in-etrs89

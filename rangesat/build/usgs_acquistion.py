from typing import AnyStr
from lsru import Espa, Usgs
from datetime import datetime

import os
import shutil

from os.path import join as _join
from os.path import split as _split
from os.path import exists as _exists

import shapefile
import pyproj

_thisdir = os.path.dirname(__file__)

from rangesat.all_your_base import wgs84_proj4, wkt_2_proj4

def place_order(bbox,
            t0: datetime,
            tend: datetime,
            max_cloud_cover=40,
            landsat_num=8,
            verbose=False):
    """


        collections = {4: 'LANDSAT_TM_C1',
                       5: 'LANDSAT_TM_C1',
                       7: 'LANDSAT_ETM_C1',
                       8: 'LANDSAT_8_C1'}

    :param bbox: left, bottom, right, top
    :param t0: datetime object
    :param tend: datetime object
    :return:
    """

    assert landsat_num in [4, 5, 7, 8]

    if landsat_num == 4:
        collection = 'LANDSAT_TM_C1'
    elif landsat_num == 5:
        collection = 'LANDSAT_TM_C1'
    elif landsat_num == 7:
        collection = 'LANDSAT_ETM_C1'
    else:
        collection = 'LANDSAT_8_C1'

    # Instantiate Usgs class and login
    usgs = Usgs(conf='/home/weppdev/.lsru')
    usgs.login()

    # Instantiate Espa class
    espa = Espa(conf='/home/weppdev/.lsru')

    # Query the Usgs api to find scene intersecting with the spatio-temporal window
    scene_list = usgs.search(collection=collection,
                             bbox=bbox,
                             begin=t0,
                             end=tend,
                             max_cloud_cover=max_cloud_cover)

    assert len(scene_list) > 0

    print(scene_list)

    # Extract Landsat scene ids for each hit from the metadata
    scene_list = [x['displayId'] for x in scene_list]

    products = espa.get_available_products(scene_list[0])
    print(landsat_num, products)
    if landsat_num == 4:
        products = products['tm5_collection']['products']
    elif landsat_num == 5:
        products = products['tm5_collection']['products']
    elif landsat_num == 7:
        products = products['etm7_collection']['products']
    else:
        products = products['olitirs8_collection']['products']

    print(landsat_num, products)

    # Place order (full scenes, no reprojection, sr and pixel_qa)
#    order = espa.order(scene_list=scene_list, products=products, extent=bbox)
#    print(order.orderid)


if __name__ == "__main__":
    shp = '/home/weppdev/PycharmProjects/rangesat/rangesat/test/data/RCRanch_Spatial/RockCreek_pasturesWGS'

    sf = shapefile.Reader(shp)
    bbox = sf.bbox
    src_wkt = open(shp + '.prj').read()
    src_proj4 = wkt_2_proj4(src_wkt)

    src_proj = pyproj.Proj(src_proj4)
    dst_proj = pyproj.Proj(wgs84_proj4)
    _bbox = [pyproj.transform(src_proj, dst_proj, bbox[0], bbox[1]),
             pyproj.transform(src_proj, dst_proj, bbox[2], bbox[3])]
    _bbox = [_bbox[0][0], _bbox[0][1], _bbox[1][0], _bbox[1][1]]
    print(_bbox)

    for landsat_num in [4, 5, 7, 8]:
        place_order(bbox=_bbox,
                    t0=datetime(1984, 1, 1),
                    tend=datetime(2017, 12, 31),
                    landsat_num=landsat_num)

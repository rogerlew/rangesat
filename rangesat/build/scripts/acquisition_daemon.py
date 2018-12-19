from typing import AnyStr
from lsru import Espa, Usgs
from datetime import datetime

import os
import shutil
import time

from os.path import join as _join
from os.path import split as _split
from os.path import exists as _exists

_thisdir = os.path.dirname(__file__)


if __name__ == "__main__":

    espa = Espa(conf='/home/weppdev/.lsru')

    while 1:
        for order in espa.orders:
            print('%s: %s' % (order.orderid, order.status))

            if order.is_complete:
                wd = _join(_thisdir, 'data', 'landsat', order.orderid)

                if _exists(wd):
                    continue

                os.mkdir(wd)
                print('downloading')
                order.download_all_complete(wd)


        time.sleep(30)
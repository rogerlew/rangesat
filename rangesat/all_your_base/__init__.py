from osgeo import osr

wgs84_proj4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'


def wkt_2_proj4(wkt_text):

    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt_text)
    proj4 = srs.ExportToProj4().strip()
    return proj4
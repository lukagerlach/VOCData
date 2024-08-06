from geoalchemy2 import WKBElement, WKTElement
from geoalchemy2.shape import to_shape
from geojson_pydantic import Point
from shapely import wkt
from shapely.geometry import shape


def geojson_to_geometry(geo_location: Point | None) -> WKTElement | None:
    """
    Convert GeoJSON to PostGIS Geometry (WKTElement).
    This is needed to transform pydantic GEOJson Objects into \
    WKTElement objects, to store them in the database.
    Use before writing data from api into postgis db.

    :param geo_location: Single GeoJSON object or list of GeoJSON objects.
    :type geo_location: Point
    :return: PostGIS Geometry (WKTElement) or list of WKTElement objects.
    :rtype: WKTElement
    """
    if geo_location is not None:
        return wkt.dumps(shape(geo_location))

    return None


def geometry_to_geojson(geometry: WKBElement | None) -> Point | None:
    """
    Convert a PostGIS Geometry (WKBElement) to a GeoJSON Point.
    This is needed to transform WKBElement objects into \
    pydantic GEOJson Objects, to read them from the database.
    Use after retrieving data from db to return to api.

    :param geometry: A PostGIS Geometry (WKBElement) object.
    :type geometry: WKBElement
    :return: if location is given: A GeoJSON Point object. Else None.
    :rtype: Point
    """

    if geometry is not None:
        geom_shape = to_shape(geometry)
        return Point(**geom_shape.__geo_interface__)

    return None

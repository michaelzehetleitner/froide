import os
import sys
import types

from django.db import models


def patch_gis():
    """Patch django.contrib.gis modules if GDAL is not used."""
    use_gdal_env = os.environ.get("FROIDE_USE_GDAL")
    if use_gdal_env and use_gdal_env.lower() not in {"0", "false", "no"}:
        return False

    try:
        from django.contrib.gis.db import models as geomodels  # noqa: F401
        return False
    except Exception:
        pass

    fields_mod = types.ModuleType("django.contrib.gis.db.models.fields")

    class GeoJSONField(models.JSONField):
        def __init__(self, *args, geography=False, **kwargs):
            kwargs.pop("geography", None)
            super().__init__(*args, **kwargs)

    class PointField(GeoJSONField):
        pass

    class MultiPolygonField(GeoJSONField):
        pass

    fields_mod.GeometryField = GeoJSONField
    fields_mod.PointField = PointField
    fields_mod.MultiPolygonField = MultiPolygonField

    db_models = types.ModuleType("django.contrib.gis.db.models")
    db_models.fields = fields_mod
    db_models.GeometryField = GeoJSONField
    db_models.PointField = PointField
    db_models.MultiPolygonField = MultiPolygonField

    geoip_mod = types.ModuleType("django.contrib.gis.geoip2")

    def GeoIP2(*args, **kwargs):
        raise ImportError("GeoIP2 requires GDAL")

    geoip_mod.GeoIP2 = GeoIP2

    geos_mod = types.ModuleType("django.contrib.gis.geos")

    class Point(tuple):
        def __new__(cls, x=0, y=0, **kwargs):
            return tuple.__new__(cls, (x, y))

    class MultiPolygon(list):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)

    geos_mod.Point = Point
    geos_mod.MultiPolygon = MultiPolygon

    admin_mod = types.ModuleType("django.contrib.gis.admin")
    admin_mod.GISModelAdmin = type("GISModelAdmin", (), {})

    gis_mod = types.ModuleType("django.contrib.gis")
    gis_mod.db = db_models
    gis_mod.geoip2 = geoip_mod
    gis_mod.geos = geos_mod
    gis_mod.admin = admin_mod

    sys.modules["django.contrib.gis"] = gis_mod
    sys.modules["django.contrib.gis.db"] = db_models
    sys.modules["django.contrib.gis.db.models"] = db_models
    sys.modules["django.contrib.gis.db.models.fields"] = fields_mod
    sys.modules["django.contrib.gis.geoip2"] = geoip_mod
    sys.modules["django.contrib.gis.geos"] = geos_mod
    sys.modules["django.contrib.gis.admin"] = admin_mod

    return True

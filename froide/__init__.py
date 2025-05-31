from .celery import app as celery_app
from .gis_patch import patch_gis

patch_gis()

__all__ = ("celery_app",)

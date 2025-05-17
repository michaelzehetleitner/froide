from django.conf import settings
from django.db import migrations


def add_law(apps, schema_editor):
    FoiLaw = apps.get_model("publicbody", "FoiLaw")
    PublicBody = apps.get_model("publicbody", "PublicBody")
    Site = apps.get_model("sites", "Site")

    site = Site.objects.get(id=settings.SITE_ID)

    law, created = FoiLaw.objects.get_or_create(
        pk=10001,
        slug="art-15-dsgvo",
        defaults={
            "name": "Art. 15 DSGVO",
            "site": site,
            "max_response_time": 30,
            "max_response_time_unit": "day",
        },
    )

    if not created:
        return

    pbs = PublicBody.objects.filter(name__icontains="Kultusministerium")
    pbs = pbs | PublicBody.objects.filter(name__icontains="schule")
    pbs = pbs | PublicBody.objects.filter(classification__slug__iexact="school")
    for pb in pbs.distinct():
        pb.laws.add(law)


def remove_law(apps, schema_editor):
    FoiLaw = apps.get_model("publicbody", "FoiLaw")
    PublicBody = apps.get_model("publicbody", "PublicBody")
    try:
        law = FoiLaw.objects.get(slug="art-15-dsgvo")
    except FoiLaw.DoesNotExist:
        return

    for pb in PublicBody.objects.filter(laws=law):
        pb.laws.remove(law)

    law.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("publicbody", "0050_alter_publicbody_email"),
    ]

    operations = [
        migrations.RunPython(add_law, remove_law),
    ]

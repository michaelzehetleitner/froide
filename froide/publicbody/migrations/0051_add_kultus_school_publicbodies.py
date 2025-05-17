from django.db import migrations


def create_kultus_school_pbs(apps, schema_editor):
    Jurisdiction = apps.get_model("publicbody", "Jurisdiction")
    FoiLaw = apps.get_model("publicbody", "FoiLaw")
    PublicBody = apps.get_model("publicbody", "PublicBody")
    Site = apps.get_model("sites", "Site")

    site = Site.objects.get(pk=1)

    jur, _ = Jurisdiction.objects.get_or_create(
        slug="edu",
        defaults={
            "name": "Education Jurisdiction",
            "description": "",
            "rank": 1,
            "hidden": False,
        },
    )

    law, _ = FoiLaw.objects.get_or_create(
        slug="dsgvo",
        defaults={
            "name": "Datenschutz-Grundverordnung",
            "jurisdiction": jur,
            "priority": 1,
            "site": site,
        },
    )

    km, _ = PublicBody.objects.get_or_create(
        slug="kultusministerium",
        defaults={
            "name": "Kultusministerium",
            "email": "poststelle@kultus.example.com",
            "url": "https://www.kultus.example.com",
            "jurisdiction": jur,
            "site": site,
        },
    )
    km.laws.add(law)

    for slug, name in [
        ("schule-1", "Muster-Schule 1"),
        ("schule-2", "Muster-Schule 2"),
    ]:
        pb, _ = PublicBody.objects.get_or_create(
            slug=slug,
            defaults={
                "name": name,
                "email": f"info@{slug}.example.com",
                "jurisdiction": jur,
                "site": site,
            },
        )
        pb.laws.add(law)


def delete_kultus_school_pbs(apps, schema_editor):
    PublicBody = apps.get_model("publicbody", "PublicBody")
    FoiLaw = apps.get_model("publicbody", "FoiLaw")
    Jurisdiction = apps.get_model("publicbody", "Jurisdiction")

    PublicBody.objects.filter(slug__in=["kultusministerium", "schule-1", "schule-2"]).delete()
    FoiLaw.objects.filter(slug="dsgvo").delete()
    Jurisdiction.objects.filter(slug="edu").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("publicbody", "0050_alter_publicbody_email"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(create_kultus_school_pbs, delete_kultus_school_pbs),
    ]

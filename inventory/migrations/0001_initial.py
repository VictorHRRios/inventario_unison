# Generated by Django 4.2 on 2023-11-15 00:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("name", models.CharField(max_length=255)),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("papeleria", "Papelería"),
                            ("limpieza", "Limpieza"),
                            ("plomeria", "Plomería"),
                            ("electricidad", "Electricidad"),
                        ],
                        max_length=20,
                    ),
                ),
                ("description", models.TextField()),
                (
                    "unit_type",
                    models.CharField(
                        choices=[
                            ("paquete", "Paquete"),
                            ("block", "Block"),
                            ("individual", "Individual"),
                            ("caja", "Caja"),
                        ],
                        max_length=20,
                    ),
                ),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("stock", models.IntegerField(default=0)),
                ("low_stock_threshold", models.IntegerField(default=10)),
                ("unison", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(default=django.utils.timezone.now)),
                (
                    "movement",
                    models.CharField(
                        choices=[("entrada", "Entrada"), ("salida", "Salida")],
                        max_length=10,
                    ),
                ),
                ("reason", models.TextField(blank=True, null=True)),
                ("items", models.JSONField(blank=True, default=list)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-12 17:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0007_listing_date_alter_bid_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="is_closed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
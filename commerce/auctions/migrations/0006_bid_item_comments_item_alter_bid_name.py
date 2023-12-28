# Generated by Django 4.2.7 on 2023-11-11 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0005_watchlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="item",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="itembid",
                to="auctions.listing",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="comments",
            name="item",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="itemcomment",
                to="auctions.listing",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bid",
            name="name",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="thebidder",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
# Generated by Django 4.2.13 on 2024-08-29 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iihmrapp', '0003_trn_tbl_hh_consent_form'),
    ]

    operations = [
        migrations.AddField(
            model_name='trn_tbl_health_problem',
            name='fld_other_problem',
            field=models.TextField(null=True),
        ),
    ]

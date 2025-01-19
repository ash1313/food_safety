# Generated by Django 5.1.5 on 2025-01-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodSafetyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BSSH_NM', models.CharField(max_length=255)),
                ('INDUTY_CD_NM', models.CharField(max_length=255)),
                ('LCNS_NO', models.CharField(max_length=255)),
                ('TELNO', models.CharField(max_length=255)),
                ('SITE_ADDR', models.CharField(max_length=255)),
                ('CHNG_DT', models.DateField()),
                ('CHNG_BF_CN', models.TextField()),
                ('CHNG_AF_CN', models.TextField()),
                ('CHNG_PRVNS', models.TextField()),
            ],
        ),
    ]

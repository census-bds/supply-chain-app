# Generated by Django 3.2.15 on 2023-01-19 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scip', '0012_auto_20221201_1921'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geoid_value', models.CharField(default='', max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='country',
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='county',
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='fips_code',
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='geo_id',
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='port',
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='state',
        ),
        migrations.RemoveField(
            model_name='geographydetail',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='geographydetail',
            name='geo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scip.geoid'),
        ),
    ]

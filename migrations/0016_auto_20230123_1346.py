# Generated by Django 3.2.15 on 2023-01-23 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scip', '0015_geoid_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geoid',
            name='port',
        ),
        migrations.RemoveField(
            model_name='geoid',
            name='state',
        ),
        migrations.AddField(
            model_name='geoid',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scip.geographylevel'),
        ),
        migrations.AlterField(
            model_name='foreigntrade',
            name='geography',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scip.geoid'),
        ),
        migrations.DeleteModel(
            name='GeographyDetail',
        ),
    ]
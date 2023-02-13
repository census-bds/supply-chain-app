# Generated by Django 3.2.15 on 2022-12-01 16:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scip', '0010_auto_20221123_1945'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCodeArchive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(default='', max_length=255)),
                ('product_code', models.CharField(default='', max_length=255)),
                ('description', models.TextField(default='')),
                ('flag', models.CharField(default='', max_length=255)),
                ('active', models.BooleanField(default=False)),
                ('year', models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(9999)])),
                ('desc2_4', models.TextField(default='', null=True)),
                ('descript_L', models.TextField(default='', null=True)),
                ('product_code_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scip.productcodedetail')),
            ],
        ),
        migrations.RenameField(
            model_name='productcode',
            old_name='active_description',
            new_name='description',
        ),
        migrations.AddField(
            model_name='productcode',
            name='flag',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='ProductCodeHistory',
        ),
    ]
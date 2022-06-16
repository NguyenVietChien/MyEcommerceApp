# Generated by Django 4.0.4 on 2022-04-29 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_name', models.TextField(primary_key=True, serialize=False)),
                ('product_price', models.IntegerField()),
                ('product_link', models.TextField()),
                ('rating_point', models.FloatField()),
                ('total_comments', models.IntegerField()),
                ('rating_5_star', models.IntegerField()),
                ('rating_4_star', models.IntegerField()),
                ('rating_3_star', models.IntegerField()),
                ('rating_2_star', models.IntegerField()),
                ('rating_1_star', models.IntegerField()),
                ('platform', models.TextField()),
            ],
            options={
                'db_table': 'myecommerce_tb',
            },
        ),
    ]

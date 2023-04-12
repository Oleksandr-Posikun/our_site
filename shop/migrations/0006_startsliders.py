# Generated by Django 4.2 on 2023-04-10 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_productpopular_img_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StartSliders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_slider', models.CharField(max_length=50)),
                ('position_text', models.CharField(max_length=50)),
                ('active', models.CharField(max_length=7)),
                ('img', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.image')),
            ],
        ),
    ]

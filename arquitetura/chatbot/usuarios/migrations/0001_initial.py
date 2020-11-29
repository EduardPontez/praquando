# Generated by Django 2.2.5 on 2020-11-29 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('active', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
    ]

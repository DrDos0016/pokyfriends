# Generated by Django 4.2.9 on 2024-01-30 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Category Title', max_length=100)),
                ('slug', models.CharField(editable=False, help_text='Category Slug', max_length=100)),
            ],
        ),
    ]

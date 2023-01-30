# Generated by Django 4.1.5 on 2023-01-30 15:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EccommerceStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100, unique=True)),
                ('main_url', models.CharField(max_length=100, unique=True)),
                ('api_url', models.URLField(blank=True, max_length=255)),
                ('module_name', models.CharField(blank=True, max_length=50)),
                ('class_name', models.CharField(blank=True, max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StoreExtraField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_data', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
                ('parrent_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.eccommercestore')),
            ],
        ),
        migrations.CreateModel(
            name='LocalStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('scraped_id', models.IntegerField(null=True)),
                ('url', models.URLField(blank=True, max_length=255)),
                ('api_url', models.URLField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
                ('parrent_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.eccommercestore')),
            ],
        ),
    ]

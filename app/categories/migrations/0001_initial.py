# Generated by Django 4.1.5 on 2023-01-28 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255, unique=True)),
                ('api_url', models.URLField(blank=True, max_length=255)),
                ('scraped_id', models.IntegerField(null=True)),
                ('meta_title', models.CharField(blank=True, max_length=255)),
                ('category_path', models.CharField(blank=True, max_length=50)),
                ('category_level', models.IntegerField(null=True)),
                ('children_category_count', models.IntegerField(null=True)),
                ('product_count', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
                ('parrent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category')),
                ('parrent_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.eccommercestore')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryExtraField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_data', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
                ('parrent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
            ],
        ),
    ]

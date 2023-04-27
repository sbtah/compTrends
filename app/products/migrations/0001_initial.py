# Generated by Django 4.2 on 2023-04-26 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('url', models.URLField(db_index=True, max_length=255, unique=True)),
                ('scraped_id', models.IntegerField(db_index=True, unique=True)),
                ('type_id', models.CharField(blank=True, max_length=100)),
                ('api_url', models.URLField(blank=True, max_length=255)),
                ('short_description', models.TextField(blank=True)),
                ('sku', models.CharField(blank=True, max_length=50)),
                ('ean', models.CharField(blank=True, max_length=50)),
                ('brand_name', models.CharField(blank=True, max_length=50)),
                ('promotion', models.BooleanField(default=False)),
                ('default_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('promo_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('unit_type', models.CharField(blank=True, max_length=10)),
                ('conversion', models.CharField(blank=True, max_length=10)),
                ('conversion_unit', models.CharField(blank=True, max_length=10)),
                ('qty_per_package', models.IntegerField(null=True)),
                ('tax_rate', models.CharField(blank=True, max_length=10)),
                ('parrent_category_from_path', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
                ('parrent_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='categories.category')),
                ('parrent_store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.eccommercestore')),
            ],
        ),
        migrations.CreateModel(
            name='ProductLocalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parrent_product_scraped_id', models.IntegerField()),
                ('local_store_name', models.CharField(max_length=255)),
                ('local_store_scraped_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('type_id', models.CharField(blank=True, max_length=100)),
                ('quantity', models.IntegerField(null=True)),
                ('stock_status', models.IntegerField(null=True)),
                ('availability', models.CharField(blank=True, max_length=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField()),
                ('parrent_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
            options={
                'verbose_name_plural': 'Product Local Data',
            },
        ),
        migrations.CreateModel(
            name='ProductExtraField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_data', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('last_scrape', models.DateTimeField(blank=True, null=True)),
                ('parrent_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='productlocaldata',
            constraint=models.UniqueConstraint(fields=('parrent_product', 'local_store_name', 'last_scrape'), name='Unique ProductLocalData'),
        ),
    ]

# Generated by Django 3.0.8 on 2020-08-02 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='MLAlgorithm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=4000)),
                ('owner', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('version', models.CharField(max_length=100)),
                ('parent_endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='endpoints.Endpoint')),
            ],
        ),
        migrations.CreateModel(
            name='MLRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=1000)),
                ('feedback', models.CharField(blank=True, max_length=1000, null=True)),
                ('input_data', models.CharField(max_length=1000)),
                ('full_response', models.CharField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_mlalgorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='endpoints.MLAlgorithm')),
            ],
        ),
        migrations.CreateModel(
            name='MLAlgorithmStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('active', models.BooleanField()),
                ('created_by', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_mlalgorithm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statuses', to='endpoints.MLAlgorithm')),
            ],
        ),
    ]

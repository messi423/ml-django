# Generated by Django 3.0.8 on 2020-08-04 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('endpoints', '0003_auto_20200804_0607'),
    ]

    operations = [
        migrations.CreateModel(
            name='ABTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_by', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('summary', models.CharField(max_length=500)),
                ('parent_mlalgorithm_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_mlalgorithm_1', to='endpoints.MLAlgorithm')),
                ('parent_mlalgorithm_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_mlalgorithm_2', to='endpoints.MLAlgorithm')),
            ],
        ),
    ]

# Generated by Django 5.0.2 on 2024-03-27 16:41

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, max_length=36, primary_key=True, serialize=False)),
                ('digital_watermarking_id', models.CharField(max_length=36)),
                ('title', models.CharField(max_length=36)),
                ('path', models.CharField(max_length=36)),
                ('digital_watermarking', models.BooleanField(blank=True, default=False)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'VIDEO',
            },
        ),
    ]

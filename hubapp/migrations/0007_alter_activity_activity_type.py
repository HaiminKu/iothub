# Generated by Django 3.2.7 on 2021-12-05 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubapp', '0006_alter_activity_activity_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('Follower', 'Follower'), ('Following', 'Following'), ('Add', 'Add'), ('Edit', 'Edit'), ('Delete', 'Delete')], max_length=20),
        ),
    ]

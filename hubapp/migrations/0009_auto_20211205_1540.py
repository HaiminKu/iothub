# Generated by Django 3.2.7 on 2021-12-05 20:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hubapp', '0008_auto_20211205_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profile_character',
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Not to say', 'Not to say')], default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 4.2 on 2025-03-13 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0002_admin_user_employee_user_manager_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='password',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='password',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='password',
        ),
    ]

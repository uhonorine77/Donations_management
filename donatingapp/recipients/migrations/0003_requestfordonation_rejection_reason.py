# Generated by Django 5.1.2 on 2024-11-30 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipients', '0002_requestfordonation_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestfordonation',
            name='rejection_reason',
            field=models.CharField(blank=True, choices=[('Not Necessary', 'Not Necessary'), ('Not Feasible', 'Not Feasible'), ('High Amount', 'High Amount')], max_length=255, null=True),
        ),
    ]
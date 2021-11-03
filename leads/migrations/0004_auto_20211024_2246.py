# Generated by Django 3.1.1 on 2021-10-24 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0003_auto_20211024_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leads', to='leads.category'),
        ),
    ]

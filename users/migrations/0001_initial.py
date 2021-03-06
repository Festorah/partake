# Generated by Django 3.2 on 2021-05-19 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('branch_operations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.png', upload_to='profile_pics')),
                ('address', models.TextField(default='You should update your address here...could be anywhere in the world')),
                ('position', models.CharField(blank=True, choices=[('Member', 'Member'), ('Steward', 'Steward'), ('Pastor', 'Pastor')], max_length=250)),
                ('dashboard_pass_1', models.CharField(blank=True, default='glory', max_length=10)),
                ('dashboard_pass_2', models.CharField(blank=True, default='peace', max_length=10)),
                ('church_branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='branch_operations.churchbranch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

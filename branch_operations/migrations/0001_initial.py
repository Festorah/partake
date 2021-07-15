# Generated by Django 3.2 on 2021-05-19 00:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChurchBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('pass_1', models.CharField(blank=True, max_length=10)),
                ('pass_2', models.CharField(blank=True, max_length=10)),
                ('pastor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAttendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('pastor', models.IntegerField()),
                ('men', models.IntegerField()),
                ('women', models.IntegerField()),
                ('brothers', models.IntegerField()),
                ('sisters', models.IntegerField()),
                ('teenagers', models.IntegerField()),
                ('children', models.IntegerField()),
                ('first_timers', models.IntegerField()),
                ('total', models.IntegerField()),
                ('pastors_comments', models.TextField(blank=True, default='')),
                ('dashboard_pass_1', models.CharField(blank=True, max_length=10)),
                ('church_branch', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='branch_operations.churchbranch')),
            ],
        ),
        migrations.CreateModel(
            name='FirstTimer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('address', models.TextField(default='address!')),
                ('follow_up', models.CharField(max_length=50)),
                ('report', models.TextField(blank=True, default='')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('occupation', models.CharField(blank=True, max_length=50)),
                ('church_branch', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='branch_operations.churchbranch')),
            ],
        ),
        migrations.CreateModel(
            name='Convert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('salvation_date', models.DateTimeField()),
                ('address', models.TextField(default='Come all things are Ready. Jesus is Lord!')),
                ('discipler', models.CharField(max_length=50)),
                ('report', models.TextField(blank=True, default='')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('occupation', models.CharField(blank=True, max_length=50)),
                ('church_branch', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='branch_operations.churchbranch')),
            ],
        ),
    ]

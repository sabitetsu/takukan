# Generated by Django 3.2.8 on 2021-12-18 06:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('userID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=100)),
                ('profile', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='TakuModel',
            fields=[
                ('takuID', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('charaURL', models.CharField(max_length=300)),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.usermodel')),
            ],
        ),
        migrations.CreateModel(
            name='TakuMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.CharField(max_length=100)),
                ('takuID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.takumodel')),
            ],
        ),
        migrations.CreateModel(
            name='TakuDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('takuID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedule.takumodel')),
            ],
        ),
    ]

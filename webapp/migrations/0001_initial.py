# Generated by Django 3.0.10 on 2021-03-18 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(default='CODE', max_length=10, unique=True)),
                ('course_name', models.CharField(default='Name', max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty_name', models.CharField(default='Name', max_length=200)),
                ('faculty_code', models.CharField(default='CODE', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Lecture_type', models.CharField(default='TH', max_length=100)),
                ('Lecture_type_ff', models.CharField(default='Theory', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='room_no',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='table1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part1', models.PositiveIntegerField(default=1, null=True)),
                ('sem1', models.PositiveIntegerField(default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acad_year', models.CharField(default='2019-20', max_length=100)),
                ('show', models.BooleanField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='table2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday'), ('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday')], default='MONDAY', max_length=100, null=True)),
                ('start_time', models.TimeField(null=True)),
                ('hours', models.PositiveIntegerField(default=1, null=True)),
                ('minutes', models.PositiveIntegerField(default=0, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('paper_name', models.CharField(default='Subject', max_length=100)),
                ('Lecture_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Lecture')),
                ('choose', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.table1')),
                ('faculty_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.faculty')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.room_no')),
                ('section_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.section')),
            ],
        ),
        migrations.AddField(
            model_name='table1',
            name='acad_year1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.year'),
        ),
        migrations.AddField(
            model_name='table1',
            name='course_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Course'),
        ),
    ]

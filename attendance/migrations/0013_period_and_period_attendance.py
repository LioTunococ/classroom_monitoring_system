from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('order', models.PositiveIntegerField(default=1)),
                ('half', models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], default='AM', max_length=2)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periods', to='attendance.schoolyear')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='period',
            unique_together={('school_year', 'name')},
        ),
        migrations.CreateModel(
            name='AttendancePeriodRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent'), ('L', 'Late'), ('E', 'Excused')], default='P', max_length=1)),
                ('time_in', models.TimeField(blank=True, null=True)),
                ('remarks', models.CharField(blank=True, max_length=255)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='period_attendance', to='attendance.enrollment')),
                ('period', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.period')),
            ],
            options={
                'ordering': ['-date', 'period__order', 'enrollment__student__last_name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='attendanceperiodrecord',
            unique_together={('enrollment', 'date', 'period')},
        ),
    ]


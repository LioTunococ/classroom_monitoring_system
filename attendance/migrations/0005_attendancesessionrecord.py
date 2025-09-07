from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0004_student_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceSessionRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("session", models.CharField(choices=[("AM", "AM"), ("PM", "PM")], max_length=2)),
                ("status", models.CharField(choices=[("P", "Present"), ("A", "Absent"), ("L", "Late"), ("E", "Excused")], default="P", max_length=1)),
                ("remarks", models.CharField(blank=True, max_length=255)),
                ("enrollment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_sessions", to="attendance.enrollment")),
            ],
            options={
                "ordering": ["-date", "session", "enrollment__student__last_name"],
                "unique_together": {("enrollment", "date", "session")},
            },
        ),
    ]


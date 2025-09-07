from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0007_delete_attendancerecord"),
    ]

    operations = [
        migrations.CreateModel(
            name="NonSchoolDay",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("kind", models.CharField(choices=[("HOL", "Holiday"), ("SUS", "Class Suspension")], default="HOL", max_length=3)),
                ("title", models.CharField(max_length=150)),
                ("notes", models.CharField(blank=True, max_length=255)),
                ("school_year", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="non_school_days", to="attendance.schoolyear")),
            ],
            options={
                "ordering": ["-date"],
                "unique_together": {("school_year", "date")},
            },
        ),
        migrations.AddIndex(
            model_name="nonschoolday",
            index=models.Index(fields=["school_year", "date"], name="idx_nsd_sy_date"),
        ),
        migrations.AddIndex(
            model_name="nonschoolday",
            index=models.Index(fields=["date"], name="idx_nsd_date"),
        ),
    ]


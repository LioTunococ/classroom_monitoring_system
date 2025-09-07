from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0006_attendancesessionrecord_indexes"),
    ]

    operations = [
        migrations.DeleteModel(
            name="AttendanceRecord",
        ),
    ]


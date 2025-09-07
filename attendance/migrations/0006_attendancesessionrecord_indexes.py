from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0005_attendancesessionrecord"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="attendancesessionrecord",
            index=models.Index(fields=["enrollment", "date"], name="idx_asr_enr_date"),
        ),
        migrations.AddIndex(
            model_name="attendancesessionrecord",
            index=models.Index(fields=["date", "session"], name="idx_asr_date_sess"),
        ),
        migrations.AddIndex(
            model_name="attendancesessionrecord",
            index=models.Index(fields=["date"], name="idx_asr_date"),
        ),
    ]

